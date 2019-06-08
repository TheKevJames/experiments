import tensorflow as tf

from .params import GRAPHEMES
from .params import HIDDEN_UNITS
from .params import LR
from .params import MAX_LEN
from .params import PHONEMES


class Graph:
    def __init__(self) -> None:
        self.x = tf.placeholder(tf.int32, shape=(None, MAX_LEN),
                                name='grapheme')
        self.y = tf.placeholder(tf.int32, shape=(None, MAX_LEN),
                                name='phoneme')

        # Sequence lengths
        seqlens = tf.reduce_sum(tf.sign(self.x), -1)

        # Embedding
        inputs = tf.one_hot(self.x, len(GRAPHEMES))

        # Encoder: BiGRU
        cell_fw = tf.nn.rnn_cell.GRUCell(HIDDEN_UNITS)
        cell_bw = tf.nn.rnn_cell.GRUCell(HIDDEN_UNITS)
        outputs, _ = tf.nn.bidirectional_dynamic_rnn(
            cell_fw, cell_bw, inputs, seqlens, dtype=tf.float32)
        memory = tf.concat(outputs, -1)

        # Decoder : Attentional GRU
        decoder_inputs = tf.concat((tf.zeros_like((self.y[:, :1])),
                                    self.y[:, :-1]), -1)
        decoder_inputs = tf.one_hot(decoder_inputs, len(PHONEMES))
        attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(
            HIDDEN_UNITS, memory, seqlens)
        cell = tf.nn.rnn_cell.GRUCell(HIDDEN_UNITS)
        cell_with_attention = tf.contrib.seq2seq.AttentionWrapper(
            cell, attention_mechanism, HIDDEN_UNITS, alignment_history=True)
        outputs, _ = tf.nn.dynamic_rnn(cell_with_attention, decoder_inputs,
                                       dtype=tf.float32)  # ( N, T', 16)
        logits = tf.layers.dense(outputs, len(PHONEMES))
        self.preds = tf.to_int32(tf.argmax(logits, -1), name='preds')

        # Loss and training
        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,
                                                              labels=self.y)
        self.mean_loss = tf.reduce_mean(loss)
        self.global_step = tf.Variable(0, name='global_step', trainable=False)
        self.train_op = tf.train.AdamOptimizer(LR).minimize(
            self.mean_loss, global_step=self.global_step)
