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
'''A mimimal async, directory service.

Functionally this is a repeat of listen-at-address, except this
version adopts the publish side of the publish/subscribe model to
make itself available to clients.

See listen-at-address.py for more details.
'''
import ansar.connect as ar


def publish_a_service(self, settings):
	'''Publish this object under the name stored in settings. Returns intervention.'''

	listing = settings.listing
	ar.publish(self, listing)
	m = self.select(ar.Published, ar.NotPublished, ar.Stop)
	if isinstance(m, ar.NotPublished):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	# Ready for inbound connections and requests.
	while True:
		m = self.select(ar.Delivered, ar.Enquiry, ar.Dropped, ar.Cleared, ar.Stop)
		if isinstance(m, ar.Delivered):
			self.console(f'Delivered to {m.agent_address}')
		elif isinstance(m, ar.Enquiry):
			self.reply(ar.Ack())			# Respond to Enquiry
		elif isinstance(m, ar.Dropped):
			self.console(f'Dropped {m.reason}')
		elif isinstance(m, ar.Cleared):
			self.console(f'Cleared')
		else:	# Control-c.
			return ar.Aborted()

ar.bind(publish_a_service)

# Configuration for this executable.
class Settings(object):
	def __init__(self, listing=None):
		self.listing = listing

SETTINGS_SCHEMA = {
	'listing': str,
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(listing='enquiry-ack')

# Entry point.
if __name__ == '__main__':
	ar.create_node(publish_a_service, factory_settings=factory_settings)
