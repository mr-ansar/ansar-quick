# ansar-quick
A collection of modules intended to assist with learning how Ansar implements networking.
From the most basic listen-connect pair through to production-ready servers and networking
components.


listen-at-address.py --- connect-to-address.py

Clearest possible code that also manages to exchange some
messages.

greetings.py

listen-server.py --- connect-client.py

More robust implementation of client-server exchange including
protocol definition, configuration of addresses (i.e. therefore CLI
control) and retries.

flip.py

flip-listen-server.py --- flip-connect-client.py

Robust implementation of a slightly more real-world scenario. A device
that needs to be controlled over a network. The controller client connects
to the device server and sends control messages to the device.

There is an initial update from device to controller that provides the
current state and perhaps capabilities.

flip-publish-server.py -- flip-subscribe-client.py

Introduction of pub-sub approach to networking. Explain/demonstrate how
it comes togther in a GROUP. This create a starting point for subsequent
sections;

* GROUP - comes for free with $ ansar and homes.
* HOST - need the ansar/services directory-host
* LAN - need the ansar/services directory-lan
* WAN - need an ansar cloud account and directory

Continue with exactly the same client-server combo. Move the server (i.e.
the device) to another GROUP, then across the LAN to another host and then
lastly across the Internet to another site.

