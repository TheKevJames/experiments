import asyncio
import json
import time

import aiohttp
from gcloud.aio.kms import KMS
from gcloud.aio.kms import encode


# Our client code is pretty straightforward -- really we just need to create
# our authorization header by hitting the KMS server with the name of the
# resource we're accessing, then send that along in our request.
async def client_create_resource():
    # Similarly to the server side, on the client side we need to know the
    # project, service, and route we will be hitting, then encrypt the current
    # timestamp with those values in order to generate our token.
    project = 'my-gcp-project'
    service = 'my-api-service'

    async with aiohttp.ClientSession() as sess:
        kms = KMS(project, service, 'create-resource', session=sess)
        payload = json.dumps({'epoch': time.time()})
        token = await kms.encrypt(encode(payload))

        headers = {
            'Authorization': f'Bearer {token}',
        }

        # Note that Cloud Run gives us pretty opaque URLs by default. Out of
        # scope here is mapping a Custom Domain to your Cloud Run service, but
        # its worth noting that this could be used to avoid needing to know
        # many different pieces of information.
        #
        # For example, if you mapped all of your Cloud Run methods to something
        # like `my-api-service.my-gcp-project.my-domain.com`, you could
        # implicitly construct the URL for any resource rather than needing to
        # hardcode the ugly `{service}-{hash:0:10}-{zone}.a.run.app` domain.
        #
        # Google Docs: https://cloud.google.com/run/docs/mapping-custom-domains
        resp = await sess.post('https://{URL}/resource', headers=headers)
        resp.raise_for_status()
        assert (await resp.text()) == 'successfully created resource'


asyncio.run(client_create_resource())
