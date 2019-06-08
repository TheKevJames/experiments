Tensorflow Optimization
=======================

This represents an experiment in eking out the absolute most performance from a
Tensorflow model as I possibly can get without modifying the model itself or
running on more than a single CPU.

We're starting with the `g2p_en`_ library, with the version released just prior
to their move from Tensorflow to NumPy (commit: 7caf9d69). Not encoded in this
initial commit are the following changes:

- some refactors for running in Python 3.x: relative imports, inheritence, etc
- removal of all training-specific code; we're only looking to optimize
  inference here
- CPU-only configuration; since I'm curious to see what the maximum performance
  we can get without a GPU

Usage
-----

.. code-block:: console

    $ docker build -t tfopt .
    $ docker run --rm -it tfopt python
    >>> import g2p
    >>> g2p.predict('aardvark')
    [['AA1', 'R', 'D', 'V', 'AA2', 'R', 'K']]

Profiling
---------

.. code-block:: console

    $ docker build -t tfopt .
    $ docker run --rm -it \
          --cpus=1 --memory=4G \
          -v $(pwd)/results:/results \
          tfopt python /src/profile.py

Optimizations
-------------

First off, let's get our initial values benchmarked.

.. image:: results/initial.png

Compile Tensorflow with AVX2 and FMA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Well, the first one is the easiest: Tensorflow even warns you about this one.

::

    Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA

Let's go ahead and do that; any more advanced instructions that Tensorflow can
make use of are bound to help us out.

.. code-block:: console

    $ docker build -t tensorflow:optimized tensorflow/
    $ docker run --rm -d --name tf tensorflow:optimized sleep 60
    $ docker cp tf:/pkg/tensorflow-1.13.1-cp37-cp37m-linux_x86_64.whl tensorflow/

Note that this process takes ages so I've committed a copy of the built wheel
and modified the ``Dockerfile`` to install from that wheel accordingly.

The new instructions sets give us a nice speedup of about 1.2x.

.. image:: results/avx2_and_fma.png

.. _g2p_en: https://github.com/Kyubyong/g2p/tree/7caf9d695b178c83f9c3d3e16c3f0a4f4d4d03a2
