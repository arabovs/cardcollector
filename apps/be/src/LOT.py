import json
from hashlib import sha256
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from os import environ


hashed = sha256("bPF7i3iMBs6GrsSUaaHTRnFhn25ZCHvI".encode("utf8")).hexdigest()

print(hashed)
def record_participation():
    req = Request(
         method="POST",
         url="https://scistarter.org/api/participation/hashed/"  + "?key=" + environ["SCISTARTER_API_KEY"],
         data=urlencode(
             {
                 "hashed": hashed,
                 "type": "classification",  # other options: 'collection', 'signup'
                 "duration": 31,  # Seconds the user spent participating, or an estimate
             }
         ).encode("utf8"),
     )

    r = urlopen(req)
    if r.status != 200:
        raise Exception(r.status, r.reason)
    return json.loads(r.read())

