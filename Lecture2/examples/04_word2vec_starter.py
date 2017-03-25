from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector

from process_data import process_data

VOCAB_SIZE = 50000
BATCH_SIZE = 128
EMBED_SIZE = 128 # dimension of the word embedding vectors
SKIP_WINDOW = 1 # the context window
NUM_SAMPLED = 64    # Number of negative examples to sample.
LEARNING_RATE = 1.0
NUM_TRAIN_STEPS = 10000
SKIP_STEP = 2000 # how many steps to skip before reporting the loss

def word2vec(batch_gen):
    """ Build the graph for word2vec model and train it """
    # Step 1: define the placeholders for input and output
    # center_words have to be int to work on embedding lookup

    X = tf.placeholder(tf.int32, shape=[BATCH_SIZE], name="x-placeholder")
    Y = tf.placeholder(tf.int32, shape=[BATCH_SIZE, 1], name="y-placeholder")

    # Step 2: define weights. In word2vec, it's actually the weights that we care about
    # vocab size x embed size
    # initialized to random uniform -1 to 1
    matrix = tf.Variable(tf.random_uniform([VOCAB_SIZE, EMBED_SIZE], -1.0, 1.0), name="matrix")

    # TOO DO

    # Step 3: define the inference
    # get the embed of input words using tf.nn.embedding_lookup
    embed = tf.nn.embedding_lookup(matrix, X, name='embed')

    # Step 4: construct variables for NCE loss
    # tf.nn.nce_loss(weights, biases, labels, inputs, num_sampled, num_classes, ...)
    # nce_weight (vocab size x embed size), intialized to truncated_normal stddev=1.0 / (EMBED_SIZE ** 0.5)
    # bias: vocab size, initialized to 0

    weights = tf.Variable(tf.truncated_normal([VOCAB_SIZE, EMBED_SIZE], stddev=1.0/(EMBED_SIZE ** 0.5)), name="weight")
    bias = tf.Variable(tf.zeros([VOCAB_SIZE]), name="bias")

    # define loss function to be NCE loss function
    # tf.nn.nce_loss(weights, biases, labels, inputs, num_sampled, num_classes, ...)
    # need to get the mean accross the batch

    nce_loss = tf.nn.nce_loss(weights=weights, biases=bias, labels=Y, inputs=embed, num_sampled=NUM_SAMPLED, num_classes=VOCAB_SIZE)
    loss = tf.reduce_mean(nce_loss)

    # Step 5: define optimizer
    
    optimizer = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        total_loss = 0.0 # we use this to calculate the average loss in the last SKIP_STEP steps
        writer = tf.summary.FileWriter('./my_graph/no_frills/', sess.graph)
        for index in xrange(NUM_TRAIN_STEPS):
            centers, targets = batch_gen.next()
            op, loss_batch = sess.run([optimizer, loss], feed_dict={X:centers, Y:targets})
            total_loss += loss_batch
            if (index + 1) % SKIP_STEP == 0:
                print('Average loss at step {}: {:5.1f}'.format(index, total_loss / SKIP_STEP))
                total_loss = 0.0
        writer.close()

def main():
    batch_gen = process_data(VOCAB_SIZE, BATCH_SIZE, SKIP_WINDOW)
    word2vec(batch_gen)

if __name__ == '__main__':
    main()