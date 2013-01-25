#!/usr/local/bin/python
from regression.models import *
from django.contrib.auth.models import User
version="M2"
category="Individual+QC72+ISSU"
for item in Modulelist.objects.filter(version_number=Version.objects.get(version_number='%s' % version)):
    owner=TestcaseSummary.objects.filter(Testbed_Name=item.testbed_number,Version_Number=item.version_number)[0].Testbed_Owner
    TestcaseSummary(Category='%s' % category,Testbed_Name=item.testbed_number,Version_Number=item.version_number,Testbed_Mode=item.testbed_mode,Testbed_Owner=owner).save()
