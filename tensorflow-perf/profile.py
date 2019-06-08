from g2p import predict


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


for case in CASES:
    for _ in range(ITERATIONS):
        predict(case)
