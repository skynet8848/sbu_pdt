#!/usr/bin/python
import commands
import re
import sys
sys.path.append('/home/tester/tools/python/python_project')
from dut_list import DutList
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
import regression.models

def get_version(ip,slt_number):
    item=regression.models.Testbed.objects.get(Testbed_Number="%s" % slt_number)
    (status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    if re.search(r'Timeout', output):
        item.Testbed_Version = "N/A"
    else:
        item.Testbed_Version = output
    item.save()
    return output

def get_time_stamp():
    month = {"Jan"  : '01',
                 "Feb"  : '02',
                 "Mar"  : '03',
                 "Apr"  : '04',
                 "May"  : '05',
                 "Jun"  : '06',
                 "Jul"  : '07',
                 "Aug"  : '08',
                 "Sep"  : '09',
                 "Oct"  : '10',
                 "Nov"  : '11',
                 "Dec"  : '12',             
                 }
    date=commands.getstatusoutput('date')[1].split(' ')
    if not date[2]:
        time_stamp='%s-%s-%s %s' % (date[6],month[date[1]],date[3],date[4])
    else:
        time_stamp='%s-%s-%s %s' % (date[5],month[date[1]],date[2],date[3])
    return time_stamp

if __name__ == "__main__":
    logfile=open('version_get.log', 'a')
    for slt_number,ip in DutList.IpAddress.items():
        junos_version=get_version(ip,slt_number)
        logfile.write("%s The JUNOS version running on %s is: %s" % (get_time_stamp(),slt_number,junos_version))
        logfile.write("\n")
        print "%s The JUNOS version running on %s is: %s" % (get_time_stamp(),slt_number,junos_version)
    logfile.close()
        

