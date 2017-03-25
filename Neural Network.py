import tensorflow as tf



class Model:
    """
    Implementation of a seq2seq model.
    Architecture:
        Encoder/decoder
        2 LTSM layers
    """
    def __init__(self, args, textData):
        """
        Args:
            args: parameters of the model
            textData: the dataset object
        """
        print("Model creation...")

        self.textData = textData  # Keep a reference on the dataset
        self.args = args  # Keep track of the parameters of the model
        self.dtype = tf.float32

        # Placeholders
        self.encoderInputs  = None
        self.decoderInputs  = None  # Same that decoderTarget plus the <go>
        self.decoderTargets = None
        self.decoderWeights = None  # Adjust the learning to the target sentence size

        # Main operators
        self.lossFct = None
        self.optOp = None
        self.outputs = None  # Outputs of the network, list of probability for each words

        # Construct the graphs
        self.buildNetwork()


    def buildNetwork(self):
        print("ahda 3laya");
