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

The client for the server in publish-a-service.py.
'''
import ansar.connect as ar

def subscribe_to_service(self, settings):
	'''Subscribe to the name stored in settings. Make a request. Returns confirmation or why it failed.'''

	listing = settings.listing
	ar.subscribe(self, listing)
	m = self.select(ar.Subscribed, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()

	m = self.select(ar.Available, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()
	server_address = self.return_address

	# Ready to make request.
	r = self.ask(ar.Enquiry(),			# A request.
		(ar.Ack, ar.Dropped, ar.Stop),	# Possible response or external event.
		server_address,					# Where to send the request.
		seconds=3.0)					# Expected quality-of-service.

	if isinstance(r, ar.Ack):			# Intended outcome.
		pass
	elif isinstance(r, ar.Dropped):
		return r
	elif isinstance(r, ar.Stop):
		return ar.Aborted()
	elif isinstance(r, ar.SelectTimer):
		return ar.TimedOut(r)

	return r	# Return the result of Enquiry.

ar.bind(subscribe_to_service)

#
#
class Settings(object):
	def __init__(self, listing=None):
		self.listing = listing

SETTINGS_SCHEMA = {
	'listing': str,
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(listing='enquiry-ack')

if __name__ == '__main__':
	ar.create_node(subscribe_to_service, factory_settings=factory_settings)
