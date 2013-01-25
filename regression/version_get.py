#!/usr/bin/python
import commands
import re
import sys
sys.path.append('/home/tester/tools/python/python_project')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "sbu_pdt.settings"
from models import Testbed
from dut_list import DutList

def get_version(ip,slt_number):
    item=Testbed.objects.filter(Testbed_Number="%s" % slt_number)
    (status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    if re.search(r'Timeout', output):
        item.Testbed_Version = "N/A"
    else:
        item.Testbed_Version = output
    item.save()
    return output

if __name__ == "__main__":
    for slt_number,ip in DutList.IpAddress.item():
        version=get_version(ip,slt_number)
        print "The JUNOS version running on %s is: %s" % (slt_number,version)
    
        

