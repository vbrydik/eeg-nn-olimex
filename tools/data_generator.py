'''
Our data looks something like this:

frame | version | ch1 | ch2 | ch3 | ch4 | ch5 | ch6 | button_states
------|---------|-----|-----|-----|-----|-----|-----|--------------
ea    | 2       | 345 | 556 | 256 | 637 | 151 | 355 | 7
eb    | 2       | 545 | 566 | 906 | 426 | 724 | 315 | 7
ec    | 2       | 571 | 346 | 778 | 366 | 266 | 167 | 7
      |         |     |     |     |     |     |     |
 .... | ....... | ... | ... | ... | ... | ... | ... | ............
      |         |     |     |     |     |     |     |
ef    | 2       | 256 | 512 | 215 | 635 | 734 | 864 | 7


What we care actually care about is data in channels:

ch1 | ch2 | ch3 | ch4 | ch5 | ch6
----|-----|-----|-----|-----|-----
345 | 556 | 256 | 637 | 151 | 355
545 | 566 | 906 | 426 | 724 | 315
571 | 346 | 778 | 366 | 266 | 167
    |     |     |     |     |
... | ... | ... | ... | ... | ...
    |     |     |     |     |
256 | 512 | 215 | 635 | 734 | 864

(all the values should be between 0.0 and 1.0, not 0 and 65355)

So this data should correspond to some action or command.
This means that our featureset shoud look something like this:
(on the left of a list we have data that corresponds to ..
.. a label or more scpecifically one-hot value, whis means ..
.. that a certain command is activated)

featureset = [
    [[ch1, ch2, ch3, ch4, ch5, ch6], [0, 0, 0, 1, 0]],
    [[ch1, ch2, ch3, ch4, ch5, ch6], [0, 1, 0, 0, 0]],
    [[...], [...]],
    [[...], [...]],
     ...
]

'''

import numpy as np


def generate_random_train_data(n_of_data, n_inputs):
    fs = []

    for i in range(n_of_data):
        f = np.random.rand(n_inputs)
        f = list(f)
        fs.append(f)

    return fs
