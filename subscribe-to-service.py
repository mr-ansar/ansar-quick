# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2024 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''A mimimal async, directory client.

Functionally this is a repeat of connect-to-address, except this
version adopts the subscribe side of the publish/subscribe model to
make connections to services.

See listen-at-address.py/connect-to-address.py for more details.
'''
import ansar.connect as ar
from hello_welcome import *

# The subscriber object.
def subscribe_to_service(self, settings):
	client_name = settings.client_name

	# Declare interest in the service.
	listing = settings.listing
	ar.subscribe(self, listing)

	m = self.select(ar.Subscribed, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()

	m = self.select(ar.Available, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()
	server_address = self.return_address

	hello = Hello(my_name=client_name)
	self.send(hello, server_address)
	r = self.select(Welcome, ar.Cleared, ar.Dropped, ar.Stop, seconds=3.0)

	if isinstance(r, Welcome):			# Intended outcome.
		pass
	elif isinstance(r, (ar.Cleared, ar.Dropped)):
		return r
	elif isinstance(r, ar.Stop):
		return ar.Aborted()
	elif isinstance(r, ar.SelectTimer):
		return ar.TimedOut(r)

	return r	# Return the result of Enquiry.

ar.bind(subscribe_to_service)

# Configuration for this executable.
class Settings(object):
	def __init__(self, client_name=None, listing=None):
		self.client_name = client_name
		self.listing = listing

SETTINGS_SCHEMA = {
	'client_name': ar.Unicode(),
	'listing': ar.Unicode(),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(client_name='Gladys', listing='hello-welcome')

if __name__ == '__main__':
	ar.create_node(subscribe_to_service, factory_settings=factory_settings)
