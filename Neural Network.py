import tensorflow as tf

x = tf.constant(35, name='x')
y = tf.Variable(x + 5, name='y')

model = tf.initialize_all_variables()

sess = tf.Session()
sess.run(model)
print(sess.run(y))
