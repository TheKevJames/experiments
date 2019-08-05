Dockerfiles as Bootable VMs in GCP
==================================

An experiment in transforming a Dockerfile into a bootable and fully
GCP-compatible custom VM image which can be used to spawn GCE instances with
full support for any and all standard GCE operations.

Usage
-----

Build, upload, and optimize the image with:

.. code-block:: console

    make bucket=my-gcs-bucket-for-vm-images

You'll probably want to modify the ``Dockerfile`` to be more than just an empty
Debian instance. If you install a whole bunch of stuff, you may need to bump
the size of the ``disk.img`` file (see ``./conf/configure.sh:10``)
