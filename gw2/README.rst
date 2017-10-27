GW2 Scripts
===========

crafting.py
-----------

Find recipes you have unlocked for which grabbing the ingredients on the TP and
selling the end result will earn you a profit.

.. code-block:: console

    $ export GW2_ACCESS_TOKEN=xxxx
    $ python3 -m pip install -r requirements.txt
    $ python3 crafting.py

fractals.py
-----------

Calculates average Fractal Encryption return rates from TP.

.. code-block:: console

    $ python3 -m pip install -r requirements.txt
    $ python3 fractals.py
    Data collected from 127 Fractal Encryptions

    Lowest Return: 21s 88b
    Average Return: 48s 76b
    Highest Return: 1g 36s 18b

    Deeply Discounted Key + box: 43s 27b
    Discounted Key + box: 48s 67b
    Key + box: 53s 27b
