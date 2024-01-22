import json
import os
import time
import urllib.request

import aiohttp
import sanic
from gcloud.aio.kms import decode
from gcloud.aio.kms import KMS
from sanic.exceptions import Unauthorized
from sanic.request import Request
from sanic.response import HTTPResponse


# In order for a client to make a request, it must know the target GCP project,
# API service, and API route, and be listed as a KMS encryptor for that
# combination. For human-used APIs, that means giving that access to either
# individual users or their groups, depending on our usage.
#
# Similarly, any server must know its own project, its own name, and all the
# routes which it provides, and be listed as a KMS decrypter for all those
# combinations.

# On Cloud Run or most any GCP service, you can use their metadata server to
# get your current project name. Note that some services may make this easier
# for you by automatically setting an environment variable. Outside of GCP, you
# would need to set the name of the GCP project which would be used for shared
# authentication.
API_PROJECT = urllib.request.urlopen(
    urllib.request.Request('http://metadata.google.internal/'
                           'computeMetadata/v1/project/project-id',
                           headers={'Metadata-Flavor': 'Google'})
).read().decode()

# On Cloud Run, this is set for you automatically based on the name of your
# service. Other GCP services set their name in different environment variables
# (or not at all) -- in that case, you'd likely want to hardcode this to the
# pre-shared name of your API.
API_SERVICE = os.environ['K_SERVICE']

# Any token which is re-used after `n` seconds is denied as a replay attack.
# Note that this does *not* solve user expiry, since a user could have
# theoretically generated infinitely many future-ready tokens before their
# access was revoked. We'll solve that later on with key rotation.
#
# This should be as small as possible while still being above the expected time
# to:
# - create a request
# - send a request
# - receive a request
# - process the headers
TOKEN_TTL = 10.


# I like Sanic, but really the exact web framework you use is irrelevant here.
# The only requirement for this solution is that you're able to read headers.
# Any boilerplate such as running or configuring Sanic has been omitted for
# brevity.
app = sanic.Sanic()


# This is a demo of the helper function used on the server side of things (eg.
# within Cloud Run) in order to verify incoming requests. You'd want to call
# this immediately when a new request is received (or build it as a decorator,
# or whatever you're preferred style is).
async def verify_auth(route: str, headers: dict) -> None:
    kind, token = headers.get('Authorization', 'no auth').split()
    if kind != 'Bearer':
        raise Unauthorized('invalid token type', scheme='Bearer')

    # Use the shared secret to decrypt. Homefully we can generate this from a
    # single source of truth, ie. the name of the method, or the URL, or
    # something like that. Maybe the `Location` header?
    async with aiohttp.ClientSession() as sess:
        kms = KMS(API_PROJECT, API_SERVICE, route, session=sess)
        try:
            # If we can't decrypt the token, we know it was not encrypted with
            # the referenced KMS key, eg. the request was made by someone who
            # does not have access to the secret associated with this
            # project/service/route/method.
            payload = decode(await kms.decrypt(token))
        except Exception:
            raise Unauthorized('access denied', scheme='Bearer')

    # Checking this value let's us avoid replay attacks, eg. by making sure
    # someone who intercepted a token can not use it for their own requests
    # later.
    if json.loads(payload).get('epoch', 0) < time.time() - TOKEN_TTL:
        raise Unauthorized('token expired', scheme='Bearer')

    # At the point, we've proven that the request has been generated recently
    # by a valid user who is whitelisted for accessing this endpoint.
    return


# Since most (all?) web frameworks allow you to handle different methods on
# different routes independently, this solution implicitly lets you associate
# different permission levels with different route/method combinations.
#
# Your service would likely have many routes, which have been omitted for
# brevity.
@app.route('/resource', methods=['POST'])  # type: ignore
async def create_resource(request: Request) -> HTTPResponse:
    # If you want to be really fancy, here, you could generate the `route` name
    # from your API docs, or from your function name, or something like that.
    await verify_auth('create-resource', request.headers)

    # business logic goes here

    return HTTPResponse('successfully created resource', status=200)


# Ok, I lied, here's a bit more Sanic boilerplate for launching the API
# according to the Cloud Run config (ie. `$PORT`). Nothing to see here...
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
