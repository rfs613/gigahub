#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


import json
import os
import sys

import gigahub

if __name__ == "__main__":

    if (os.getenv("GIGAHUB_PASSWORD")) is None:
        raise SystemExit("error: no GIGAHUB_PASSWORD set")

    session, reply = gigahub.open_session(username="admin", password=os.getenv("GIGAHUB_PASSWORD"))

    # Things we can query:
    #
    # Device/IP/Interfaces/Interface[@uid='1']/     internal LAN, 192.168.2.x
    # Device/IP/Interfaces/Interface[@uid='2']/     external uplink
    # Device/IP/Interfaces/Interface[@uid='3']/     internal GUEST 192.168.5.1
    # Device/IP/Interfaces/Interface[@uid='4']/     ???
    # Device/IP/Interfaces/Interface[@uid='5']/     internal TV?? 10.0.0.1
    #
    # Device/Optical/Interfaces/Interface[@uid='1']/  Fibre port
    #
    # For each, suffix "Stat" gives status (up/down)
    # and suffix "Status" gives packet counts, IP addresses, etc.

    # External link status
    action = {
        "id": 0,
        "method": "getValue",
        "xpath": "Device/Optical/Interfaces/Interface[@uid='1']/Status",
        "options": {"nss": [{"name": "gtw", "uri": "http://sagemcom.com/gateway-data"}]},
    }
    session, reply = gigahub.send_session_request(session=session, actions=[action])
    print(reply['actions'][0]['callbacks'][0]['parameters']['value'])

    # External IP address
    action = {
        "id": 0,
        "method": "getValue",
        "xpath": "Device/IP/Interfaces/Interface[@uid='2']/IPv4Addresses/IPv4Address[@uid='1']",
        "options": {"nss": [{"name": "gtw", "uri": "http://sagemcom.com/gateway-data"}]},
    }
    session, reply = gigahub.send_session_request(session=session, actions=[action])
    print(reply['actions'][0]['callbacks'][0]['parameters']['value']['IPv4Address']['IPAddress'])
