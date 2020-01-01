import sys
import os
import getopt
import logging

from WebService import *

#
# This script is used by the Certify The Web client to create TXT DNS records
# in the domain to verify ownership (https://docs.certifytheweb.com/docs/dns-scripting.html)
# It is for ClouDNS and implements their API (https://www.cloudns.net/wiki/article/59/)
#
def main(argv):
	webService = WebService()
	if len(argv) >= 3:
		key = argv[2].replace('.' + argv[1], '')
		try:
			webService.delete(argv[1], key)
			webService.add(argv[1], key, argv[3])
		except:
			print('Operation failed\n%s' % traceback.format_exc())
	else:
		print("Usage: CertUpdate domain key value")

#########################################
if __name__ == "__main__":
    main(sys.argv)

