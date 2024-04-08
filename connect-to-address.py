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
'''A mimimal async, network client.

The client for the server in listen-at-address.py.
'''
import ansar.connect as ar

def connect_to_address(self, settings):
	'''Connect to host and port stored in settings. Make a request. Returns confirmation or why it failed.'''

	ipp = ar.HostPort(settings.host, settings.port)		# Where to expect the service.
	ar.connect(self, ipp)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.NotConnected):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()
	server_address = self.return_address	# Where the Connected message came from.

	# Ready to make request.
	r = self.ask(ar.Enquiry(),				# A request.
		(ar.Ack, ar.Abandoned, ar.Stop),	# Possible response or external event.
		server_address,						# Where to send the request.
		seconds=3.0)						# Expected quality-of-service.

	if isinstance(r, ar.Ack):			# Intended outcome.
		pass
	elif isinstance(r, ar.Abandoned):
		return r
	elif isinstance(r, ar.Stop):
		return ar.Aborted()
	elif isinstance(r, ar.SelectTimer):
		return ar.TimedOut(r)

	return r	# Return the result of Enquiry.

ar.bind(connect_to_address)

#
#
class Settings(object):
	def __init__(self, host=None, port=None):
		self.host = host
		self.port = port

SETTINGS_SCHEMA = {
	'host': str,
	'port': int,
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

factory_settings = Settings(host='127.0.0.1', port=32011)

if __name__ == '__main__':
	ar.create_object(connect_to_address, factory_settings=factory_settings)
