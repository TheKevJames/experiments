import typing

import numpy as np

from .params import GRAPHEME_TO_INDEX
from .params import INDEX_TO_PHONEME
from .params import MAX_LEN
from .session import GRAPH
from .session import SESSION


def predict(text: str) -> typing.List[str]:
    words = [w.lower() for w in text.split()]
    if len(words) > MAX_LEN:
        raise Exception(f'can not process >{MAX_LEN} words')

    x = np.zeros((len(words), MAX_LEN), np.int32)  # 0: <PAD>
    for i, w in enumerate(words):
        for j, g in enumerate((w + 'E')[:MAX_LEN]):
            x[i][j] = GRAPHEME_TO_INDEX.get(g, 2)  # 2: <UNK>

    # Auto-regressive inference
    preds = np.zeros((len(x), MAX_LEN), np.int32)
    for j in range(MAX_LEN):
        _preds = SESSION.run(GRAPH.preds, {GRAPH.x: x, GRAPH.y: preds})
        preds[:, j] = _preds[:, j]

    # convert to string
    phonemes = []
    for pred in preds:
        p = [INDEX_TO_PHONEME[idx] for idx in pred]
        if '<EOS>' in p:
            p = p[:p.index('<EOS>')]

        phonemes.append(p)

    return phonemes
