`Sentry`_ Performance Impact Analysis
=====================================

`Latest Results`_

Usage
-----

.. code-block:: console

    $ python3 -m venv venv
    $ source venv/bin/activate

    $ python -m pip install raven

    $ export NUM_TESTS=10000
    $ export SENTRY_DSN="<FILL-ME-IN>"
    $ ./run.sh

.. _Latest Results: https://github.com/TheKevJames/experiments/tree/master/sentry-performance/results.txt
.. _Sentry: https://docs.sentry.io/clients/python/
