#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


import json
import os
import sys
import requests

import gigahub

if __name__ == "__main__":

    if (os.getenv("GIGAHUB_PASSWORD")) is None:
        raise SystemExit("error: no GIGAHUB_PASSWORD set")

    session, reply = gigahub.open_session(username="admin", password=os.getenv("GIGAHUB_PASSWORD"))

    # Request the URL for downloading logs
    action = {
        "id": 0,
        "method": "getVendorLogDownloadURI",
        "xpath": "Device/DeviceInfo/VendorLogFiles/VendorLogFile[@uid='1']",
    }
    session, reply = gigahub.send_session_request(session=session, actions=[action])
    uri = reply['actions'][0]['callbacks'][0]['parameters']['uri']

    # Now just do a plain HTTP get of the URI
    r = requests.get(os.getenv("GIGAHUB_URL") + uri)
    print(r.text)
