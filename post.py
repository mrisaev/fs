# POST request template to restAPI

import ssl, urllib2, base64
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
values = """<?xml version="1.0" standalone="yes"?>
<Node xmlns="http://schemas.domanin.com/schema">

</Node>
"""
request = urllib2.Request('https://localhost:9699/REST', values)
base64string = base64.b64encode('%s:%s' % ('domain\\User', 'PASSWORD'))
request.add_header("Authorization", "Basic %s" % base64string)
try:
    result = urllib2.urlopen(request, context=ctx)
    x = result.read()
    print x
except urllib2.HTTPError as e:
    print e.read()