"""
Model to predict the next sentence given an input sequence
To create the model, you need only to call 
"self.model = Model(self.args, self.textData)"
as:
self.model: the model instance in the whole work
self.textdata: can be got through "self.textData = TextData(self.args)"
"""
import tensorflow as tf

"""
Single layer perceptron algorithm implementation
Project input tensor on the output dimension
"""
class ProjectionOp:

    def __init__(self, shape, scope = None, dtype = None):
        """
        Args:
            shape: a tuple (input dim, output dim)
            scope (str): encapsulate variables
            dtype: the weights type
        """
        assert len(shape) == 2

        self.scope = scope

        # Projection on the keyboard
        with tf.variable_scope('weights_' + self.scope):
            self.W = tf.get_variable('weights', shape, dtype=dtype)
            self.b = tf.get_variable('bias', shape[1], initializer=tf.constant_initializer(), dtype=dtype)

    def getWeights(self):
        """ 
        Convenience method for some tf arguments
        """
        return self.W, self.b

    # the equation of the classifier itself.
    def __call__(self, X):
        """ Project the output of the decoder into the vocabulary space
        Args:
            X (tf.Tensor): input value
        """
        with tf.name_scope(self.scope):
            return tf.matmul(X, self.W) + self.b


"""
Implementation of a seq2seq model.
Architecture:
Encoder/decoder
2 LTSM layers
"""
class Model:
   
    def __init__(self, args, textData):
        """
        Args:
            args: parameters of the model
            textData: the dataset object in the format of ....
        """
        self.textData = textData  # Keep a reference on the dataset
        self.args = args  # Keep track of the parameters of the model
        self.dtype = tf.float32

        # Placeholders
        self.encoderInputs = None
        self.decoderInputs = None  # Same that decoderTarget plus the <go>
        self.decoderTargets = None
        self.decoderWeights = None  # Adjust the learning to the target sentence size

        # Main operators
        self.lossFct = None
        self.optOp = None
        self.outputs = None  # Outputs of the network, list of probability for each words

        self.outputProjection = None

        # Construct the graphs
        self.buildNetwork()

    
    #To normalize the given dataset.
    def sampledSoftmax(self, labels, inputs):
        labels = tf.reshape(labels, [-1, 1])  # Add one dimension (nb of true classes, here 1)

        # We need to compute the sampled_softmax_loss using 32bit floats to
        # avoid numerical instabilities.
        localWt = tf.cast(tf.transpose(self.outputProjection.W), tf.float32)
        localB = tf.cast(self.outputProjection.b, tf.float32)
        localInputs = tf.cast(inputs, tf.float32)

        return tf.cast(tf.nn.sampled_softmax_loss(localWt,  # Should have shape [num_classes, dim]
                localB,
                labels,
                localInputs,
                self.args.softmaxSamples,  # The number of classes to randomly sample per batch
                self.textData.getVocabularySize()),  # The number of classes
            self.dtype)


    def create_rnn_cell():
        encoDecoCell = tf.contrib.rnn.BasicLSTMCell(# Or GRUCell, LSTMCell(args.hiddenSize)
            self.args.hiddenSize,)
        if not self.args.test:  # TODO: Should use a placeholder instead
            encoDecoCell = tf.contrib.rnn.DropoutWrapper(encoDecoCell,
                input_keep_prob=1.0,
                output_keep_prob=self.args.dropout)
        return encoDecoCell

    def buildNetwork(self):
        """ 
        Create the computational graph
        """
        # Parameters of sampled softmax (needed for attention mechanism and a large vocabulary size)
        outputProjection = None
        # Sampled softmax only makes sense if we sample less than vocabulary size.
        if 0 < self.args.softmaxSamples < self.textData.getVocabularySize():
            outputProjection = ProjectionOp(
                (self.args.hiddenSize, self.textData.getVocabularySize()), 
                scope='softmax_projection', dtype=self.dtype
            )

