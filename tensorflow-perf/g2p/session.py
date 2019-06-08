import os

import tensorflow as tf


MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          'model', 'optimized_model.pb')


g = tf.Graph()
with tf.gfile.GFile(MODEL_PATH, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

with g.as_default():
    tf.import_graph_def(graph_def, name='prefix')

config = tf.ConfigProto(device_count={'CPU': 1, 'GPU': 0},
                        intra_op_parallelism_threads=1,
                        inter_op_parallelism_threads=1)

SESSION = tf.Session(graph=g, config=config)


class GRAPH:
    x = g.get_tensor_by_name('prefix/grapheme:0')
    y = g.get_tensor_by_name('prefix/phoneme:0')
    preds = g.get_tensor_by_name('prefix/preds:0')
