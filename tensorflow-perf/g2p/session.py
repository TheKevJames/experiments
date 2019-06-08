import os

import tensorflow as tf

from .graph import Graph


MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          'model', 'saved')


g = tf.Graph()
with g.as_default():
    with tf.device('/cpu:0'):
        GRAPH = Graph()

config = tf.ConfigProto(device_count={'CPU': 1, 'GPU': 0},
                        intra_op_parallelism_threads=1,
                        inter_op_parallelism_threads=1)

SESSION = tf.Session(graph=g, config=config)
tf.saved_model.load(SESSION, ['serve'], MODEL_PATH)
