import numpy as np
import tensorflow as tf


imageWidth = 100
imageHeight = 100
#content image
contentImage = tf.Variable(np.zeros([1, imageHeight, imageWidth, 3]), dtype = tf.float32)

#style image
styleImage = tf.Variable(np.zeros([1, imageHeight, imageWidth, 3]), dtype = tf.float32)

#filter
filter = tf.Variable(tf.random_uniform([5, 5, 3]), name = "filter")

#convolve size 96
convolved = tf.nn.conv2d()

#nonlinearity relu
nonlineared = tf.nn.relu(convolved)

#pooling size 48

#loss function

#optimizer

#fully connected
#？ fully connected will not run in a loop?
#?  if it's a classification, how to determine the bias' second dimension

weights = tf.Variable()
bias = tf.Variable()



with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #sess.run(filter)
    print "======================now it is "
    print filter
    #output
