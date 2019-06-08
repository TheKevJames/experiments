import tensorflow as tf

from .graph import Graph
from .graph import MODEL_PATH


g = tf.Graph()
with g.as_default():
    with tf.device('/cpu:0'):
        GRAPH = Graph()
        saver = tf.train.Saver()

config = tf.ConfigProto(device_count={'CPU': 1, 'GPU': 0},
                        intra_op_parallelism_threads=1,
                        inter_op_parallelism_threads=1)

SESSION = tf.Session(graph=g, config=config)
saver.restore(SESSION, tf.train.latest_checkpoint(MODEL_PATH))
