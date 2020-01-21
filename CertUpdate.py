import sys
import os
import getopt
import logging
import traceback

from WebService import *

#
# This script is used by the Certify The Web client to create TXT DNS records
# in the domain to verify ownership (https://docs.certifytheweb.com/docs/dns-scripting.html)
# It is for ClouDNS and implements their API (https://www.cloudns.net/wiki/article/59/)
#
def main(argv):
	webService = WebService()
	if len(argv) >= 4:
		# isolate just the domain name (input may be *.domain.com or something.domain.com)
		x = argv[2].split('.')
		domain = '%s.%s' % (x[len(x) - 2], x[len(x) - 1])
		key = argv[3].replace('.' + domain, '')
		try:
			if argv[1] == 'delete':
				webService.delete(domain, key)
				return

			if argv[1] == 'add':
				webService.add(domain, key, argv[4])
				return

		except:
			print('Operation failed\n%s' % traceback.format_exc())
			return

	print("Usage: CertUpdate add/delete domain key value")

#########################################
if __name__ == "__main__":
    main(sys.argv)

