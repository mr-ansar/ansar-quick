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
'''An enduring async, directory client.

Functionally this is a repeat of subscribe-to-service, except this
version persists across multiple subscriber-publisher sessions.

See publish-a-service.py/subscribe-to-service.py for more details.
'''
import ansar.connect as ar

def subscribe_to_service_continuous(self, settings):
	'''Subscribe to the name stored in settings. Make a request, expect a response and repeat.'''

	listing = settings.listing
	ar.subscribe(self, listing)
	m = self.select(ar.Subscribed, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()

	while True:
		m = self.select(ar.Available, ar.Ack, ar.T1, ar.Dropped, ar.Stop)
		if isinstance(m, ar.Available):				# Start of session, make first request.
			service_address = self.return_address
		elif isinstance(m, ar.Ack):					# Expected response. Pause.
			self.start(ar.T1, 1.0)
			continue
		elif isinstance(m, ar.T1):					# Continue.
			pass
		elif isinstance(m, ar.Dropped):				# End of session.
			continue
		else:
			return ar.Aborted()

		self.send(ar.Enquiry(), service_address)

ar.bind(subscribe_to_service_continuous)

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
	ar.create_node(subscribe_to_service_continuous, factory_settings=factory_settings)
