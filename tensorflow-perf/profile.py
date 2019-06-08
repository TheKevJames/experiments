import json
import timeit

import matplotlib.pyplot as plt


CASE_NAME = 'MKL single thread OMP'
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

ITERATIONS = 10


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


speedups = [i[1] / c[1]
            for i, c in zip(results['initial'], results[CASE_NAME])]
print(f'Speedups: {[round(x, 2) for x in speedups]}')
print(f'Speedup (mean): {round(sum(speedups) / len(speedups), 3)}')

with open(f'/results/raw.json', 'w') as f:
    f.write(json.dumps(results, sort_keys=True, indent=4) + '\n')


for case, values in results.items():
    if case in {'MKL', 'MKL single thread'}:
        continue
    plt.plot([v[0] for v in values], [v[1] for v in values], label=case)

plt.xlabel('input word count')
plt.ylabel('time in milliseconds')
plt.grid(True)
plt.legend()

plt.savefig(f'/results/{CASE_NAME.lower().replace(" ", "_")}.png')
plt.close()
