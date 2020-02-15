Google Pub/Sub Performance Testing
==================================

The goal of this experiment is to determine the expected throughput of
Google's Pub/Sub with varying publish rates and varying collection periods.

Note that all tests and results make use of the `google-cloud-pubsub`_ Python
library. I'm not doing much in the way of heavy lifting outside of however the
library itself works, but YMMV with other libraries and/or other languages. My
gut tells me the library performance, at least, should be pretty comparable as
the `gRPC benchmarking framework`_'s
`latest runs <https://performance-dot-grpc-testing.appspot.com/explore?dashboard=5652536396611584>`_
show variances in the order of ~500us between implementations (statistically
irrelevant to our results). The language runtime itself, and especially the
concurrency model, is certainly likely to have a larger effect.

.. contents:: :local:

Conclusions
-----------

There are a few things that I think the below `Results`_ point to:

* ``PublisherClient`` batch settings are very relevant. I didn't play too much
  with these values, but given the spread between the pre-publish timestamps
  and the timestamps attached when Pub/Sub receives the message, its clear
  that there can be some large delays introduced by batching. In a production
  environment, you'll almost certainly want to tune your `BatchSettings`_ for
  your expected usecase -- ``max_messages`` and ``max_latency`` look
  especially relevant.

* The spin up time doesn't seem to be all that great -- as a general rule, the
  longer the tests continued (or the more recent a previous test run was), the
  better the performance. This is not really news, as the
  `Pub/Sub Architecture`_ explains this (as well as explaining why the
  performance characteristics have higher variance at lower throughputs), but
  is worth keeping in mind, especially when designing systems with heavy
  levels of volume surges.

    * Corollary: note that my results don't show all that much in the way of
      added latency at low throughputs. There's a bit, but much less than I
      was expecting given how frequently I'd heard that this was an issue for
      Pub/Sub.

* The 99th percentile in the below results was often not that great -- but I
  do want to mention that (**purely subjectively**) it felt like the 99th was
  always much better in cases where I immediately re-ran test cases rather
  than pausing a bit between them; to me, that implies there's a definite
  corrolation between the 99th percentile and the spin up time I already
  mentioned above. Results may be better than they appear?

And, less relevantly:

* ``numpy`` continues to be a library that I'm regularly annoyed to work with:
  in this case because it caused annoying-to-debug multiprocessing issues and
  because it was very slow: I spent more time waiting for ``numpy`` to build a
  ``numpy.array`` from my 5m test results than I actually did running the
  tests. Getting `statistics.quantiles`_ in Python 3.8 will be nice!

Usage
-----

.. code-block:: console

    ./run.py [--rate=<rate>] [--duration=<duration>]

Note that I used ``numpy`` rather than ``statistics.quantiles``, so for OSX
users you may have to set the following env var to make ``numpy`` play nicely
with multiprocessing:

.. code-block:: console

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

Results
-------

Note that results here are not a strict source of truth: order of execution,
delay (or lack thereof) between test runs, and other black-box sources of
variance on Google's side seems to cause results to vary fairly significantly
between runs.

The "from Process" statistics, eg. counted from the perspective of a timestamp
attached in the publisher, generally show off the batching semantics of the
``PublisherClient`` and account for overhead such as network latency between
the publisher and the Pub/Sub servers.

The "from Server" statistics are relative to the publish time attached by
Pub/Sub, ie. the time at which they received the message.

Given a productionized publisher should be expected to tweak its batch
settings for its expected use-case, its probably not unreasonable to assume
real-world results will be somewhere between these two sets of stats.

TODO: provide comparison implementations for:

* `Synchronous Subscriptions <https://cloud.google.com/pubsub/docs/pull#synchronous_pull>`_
* `Streaming Pull <https://cloud.google.com/pubsub/docs/pull#streamingpull>`_

Async Subscriber
^^^^^^^^^^^^^^^^

The "Async Subscriber" is
`this one <https://cloud.google.com/pubsub/docs/pull#asynchronous-pull>`_,
ie. the one that calls ``pubsub_v1.SubscriberClient().subscribe()``.

Rate: 10/s
~~~~~~~~~~

::

    Total Items: 10x10 => 100

    Mean from Process: 4.8794
    50th from Process: 4.9594
    75th from Process: 6.9613
    85th from Process: 7.8099
    95th from Process: 9.6609
    99th from Process: 9.6614

    Mean from Server: 3.5990
    50th from Server: 4.3644
    75th from Server: 4.7589
    85th from Server: 4.9864
    95th from Server: 5.1170
    99th from Server: 5.1176

::

    Total Items: 10x60 => 600

    Mean from Process: 0.2261
    50th from Process: 0.0669
    75th from Process: 0.0804
    85th from Process: 0.0991
    95th from Process: 0.9215
    99th from Process: 4.0086

    Mean from Server: 0.0816
    50th from Server: 0.0480
    75th from Server: 0.0542
    85th from Server: 0.0656
    95th from Server: 0.4482
    99th from Server: 0.6230

::

    Total Items: 10x300 => 3000

    Mean from Process: 0.2456
    50th from Process: 0.0735
    75th from Process: 0.0900
    85th from Process: 0.1070
    95th from Process: 0.1679
    99th from Process: 6.2751

    Mean from Server: 0.0745
    50th from Server: 0.0545
    75th from Server: 0.0673
    85th from Server: 0.0742
    95th from Server: 0.1010
    99th from Server: 0.6445

Rate: 100/s
~~~~~~~~~~~

::

    Total Items: 100x10 => 1000

    Mean from Process: 1.1065
    50th from Process: 0.2493
    75th from Process: 2.1334
    85th from Process: 3.2622
    95th from Process: 3.8862
    99th from Process: 3.8902

    Mean from Server: 0.3381
    50th from Server: 0.2211
    75th from Server: 0.5210
    85th from Server: 0.7468
    95th from Server: 0.8356
    99th from Server: 0.8422

::

    Total Items: 100x60 => 6000

    Mean from Process: 0.9516
    50th from Process: 0.1064
    75th from Process: 0.1352
    85th from Process: 1.1488
    95th from Process: 6.6633
    99th from Process: 9.2076

    Mean from Server: 0.7147
    50th from Server: 0.0808
    75th from Server: 0.1007
    85th from Server: 1.1049
    95th from Server: 4.9100
    99th from Server: 5.0716

::

    Total Items: 100x60 => 6000

    Mean from Process: 0.3300
    50th from Process: 0.1181
    75th from Process: 0.1428
    85th from Process: 0.1500
    95th from Process: 1.6126
    99th from Process: 4.5259

    Mean from Server: 0.2032
    50th from Server: 0.0965
    75th from Server: 0.1110
    85th from Server: 0.1208
    95th from Server: 1.3546
    99th from Server: 1.6254

::

    Total Items: 100x300 => 30000

    Mean from Process: 0.1432
    50th from Process: 0.0979
    75th from Process: 0.1142
    85th from Process: 0.1242
    95th from Process: 0.1651
    99th from Process: 1.1669

    Mean from Server: 0.0970
    50th from Server: 0.0785
    75th from Server: 0.0927
    85th from Server: 0.0996
    95th from Server: 0.1248
    99th from Server: 0.7094

Rate: 1000/s
~~~~~~~~~~~~

::

    Total Items: 1000x10 => 10000

    Mean from Process: 2.1968
    50th from Process: 1.9043
    75th from Process: 3.0548
    85th from Process: 4.1311
    95th from Process: 5.1865
    99th from Process: 5.9655

    Mean from Server: 1.3679
    50th from Server: 1.2536
    75th from Server: 2.1498
    85th from Server: 2.4120
    95th from Server: 2.6666
    99th from Server: 2.8426

::

    Total Items: 1000x60 => 60000

    Mean from Process: 1.7741
    50th from Process: 0.3044
    75th from Process: 2.1688
    85th from Process: 3.7565
    95th from Process: 9.0168
    99th from Process: 12.0917

    Mean from Server: 1.0438
    50th from Server: 0.2566
    75th from Server: 1.7887
    85th from Server: 2.7374
    95th from Server: 3.9753
    99th from Server: 4.8532

::

    Total Items: 1000x60 => 60000

    Mean from Process: 0.5101
    50th from Process: 0.2784
    75th from Process: 0.3373
    85th from Process: 0.3781
    95th from Process: 1.9329
    99th from Process: 5.3234

    Mean from Server: 0.3450
    50th from Server: 0.2402
    75th from Server: 0.2934
    85th from Server: 0.3253
    95th from Server: 1.3535
    99th from Server: 1.9025

::

    Total Items: 1000x300 => 300000

    Mean from Process: 0.4057
    50th from Process: 0.2886
    75th from Process: 0.3400
    85th from Process: 0.3704
    95th from Process: 0.7481
    99th from Process: 3.3340

    Mean from Server: 0.3275
    50th from Server: 0.2411
    75th from Server: 0.2952
    85th from Server: 0.3272
    95th from Server: 0.6975
    99th from Server: 2.6061

::

    Total Items: 1000x300 => 300000

    Mean from Process: 0.5645
    50th from Process: 0.2608
    75th from Process: 0.3127
    85th from Process: 0.3488
    95th from Process: 2.6298
    99th from Process: 7.4899

    Mean from Server: 0.4782
    50th from Server: 0.2173
    75th from Server: 0.2671
    85th from Server: 0.3000
    95th from Server: 2.4839
    99th from Server: 6.2401

::

    Total Items: 1000x900 => 900000

    Mean from Process: 0.3493
    50th from Process: 0.2903
    75th from Process: 0.3361
    85th from Process: 0.3602
    95th from Process: 0.5771
    99th from Process: 2.4595

    Mean from Server: 0.2932
    50th from Server: 0.2445
    75th from Server: 0.2935
    85th from Server: 0.3167
    95th from Server: 0.4540
    99th from Server: 2.1082

.. _BatchSettings: https://googleapis.dev/python/pubsub/latest/publisher/index.html#batching
.. _Pub/Sub Architecture: https://cloud.google.com/pubsub/architecture
.. _google-cloud-pubsub: https://pypi.org/project/google-cloud-pubsub/
.. _statistics.quantiles: https://docs.python.org/3/library/statistics.html#statistics.quantiles
.. _gRPC benchmarking framework: https://grpc.io/docs/guides/benchmarking/
