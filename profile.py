import json
import timeit

import matplotlib.pyplot as plt


CASE_NAME = 'initial'
CASES = [
    'aardvark',
    'tasty applesauce',
    # TODO: 3-5
    'Three toed sloths are penultimate animals',
    'Note to self compile against my cpu',
    # TODO: 8-9
    'My name is Kevin James and aardvarks are the best',
    # TODO: 11-14
    'I bet this graph is not going to be roughly anywhere close to sub linear',
    # TODO: 16-19
    ('This is a twenty word sentence which I am using to ensure we can '
     'test to the maximum batch size'),
]

ITERATIONS = 1


with open(f'/results/raw.json', 'r') as f:
    results = json.loads(f.read())

results[CASE_NAME] = []
for case in CASES:
    times = timeit.repeat(
        stmt='predict(text)',
        setup='from g2p import predict',
        globals={'text': case},
        number=ITERATIONS,
        repeat=3)
    time = round(min(times) / float(ITERATIONS) * 1e3, 2)
    results[CASE_NAME].append((len(case.split()), time))

with open(f'/results/raw.json', 'w') as f:
    f.write(json.dumps(results))


for case, values in results.items():
    plt.plot([v[0] for v in values], [v[1] for v in values], label=case)
    plt.xlabel('input word count')
    plt.ylabel('time in milliseconds')
    plt.grid(True)
    plt.legend()

    plt.savefig(f'/results/{CASE_NAME.lower().replace(" ", "_")}.png')
    plt.close()
