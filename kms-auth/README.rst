HTTP Auth with Google KMS
=========================

Staying entirely within the Google ecosystem for eg. server-to-server
communication is very adequately handled by the builtin Google primitives such
as verification of service accounts (or, in some cases, even some very cool
implicit authorization, such as how a specific header being received by a GAE
app can verify that the `request came from GAE Cron`_).

One noticeablebly missing point, though, is in client-server communications.
There's a few partial solutions to some use-cases, but none of them really
allow for the fine-grained control that I want to specify. For example, Cloud
Run methods have a single role (``roles/run.invoker``) which can be assigned to
a user/group/serviceaccount/whatever to globally allow or revoke their
permissions to invoke any Cloud Run services within a project. You can go
through and add this role to user-service pairs, which allows that user global
invocation access to an entire service, but what if we want to go more granular
than that, ie. allow some users access to some routes within a service rather
than just having a global on-off switch?

This is an experiment in using `Cloud KMS`_ as a shared authority in order to
create route and method level permissioning for arbitrary use-cases. The demo
code is written for Cloud Run, but with very minor modifications this would
for any API hosted anywhere, not just on Cloud Run on Google Cloud Platform.

My code is divided into three sections:

- ``server.py`` for the logic which would be deployed the the Cloud Run
  service. The parts which would need to change for non-Cloud Run or non-GCP
  deployments are commented.

- ``client.py`` for the logic which would be run on the client side.

- ``configuration.tf`` for the resources which must be defined within GCP, eg.
  the IAM policies and such.

If you want to test this out, you can get this running on Cloud Run with:

.. code-block:: console

    $ gcloud builds submit --tag gcr.io/PROJECT-ID/kms-auth-demo
    $ gcloud beta run deploy --image gcr.io/PROJECT-ID/kms-auth-demo

Design Decisions
----------------

To reduce scope, I've done this work in my languages and frameworks of choice.
Calling out a few specifics:

- Everything is written in asyncio-style Python. That means Python 3.6+. All of
  this could be done synchronously as well, or even in Python 2.

- I'm using `gcloud-aio-kms`_ to communicate with Cloud KMS. Google has some
  official alternatives: the appengine v1 libraries and the `google-cloud-kms`_
  library. The former is appengine-only and the later does not support asyncio.
  What can I say? I like writing async code. Disclaimer: gcloud-aio-* is an
  open-source product from my team at Dialpad.

- All configuration is specified as Terraform schemas. I think having
  declarative infrastructure is a no-brainer, but that's not to say all of this
  could not be done directly in the GCP UI.

.. _Cloud KMS: https://cloud.google.com/kms/
.. _gcloud-aio-kms: https://pypi.org/project/gcloud-aio-kms/
.. _google-cloud-kms: https://pypi.org/project/google-cloud-kms/
.. _request came from GAE Cron: https://cloud.google.com/appengine/docs/standard/python/config/cron#securing_urls_for_cron
