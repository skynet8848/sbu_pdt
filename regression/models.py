from __future__ import division
from django.db import models
from django.contrib.auth.models import User
import commands
import re
import string
import datetime
from django import forms
from django.forms import ModelForm

class Testbed(models.Model):
    LOCATION_CHOICES = (
        ('10.155.34.126', 'US'),
        ('10.208.85.123', 'CN'),
    )
    PURPOSE_CHOICES = (
        ('Regression', 'Regression'),
        ('New Feature', 'New Feature'),
        ('Regression_M', 'Regression_M'),
    )
    PLATFORM_CHOICES = (
        ('SRX-100', 'SRX-100'),
        ('SRX-240', 'SRX-240'),
        ('SRX-1400', 'SRX-1400'),
        ('SRX-3400', 'SRX-3400'),
        ('SRX-3600', 'SRX-3600'),
        ('SRX-5600', 'SRX-5600'),
        ('SRX-5800', 'SRX-5800'),
        ('NS-5200', 'NS-5200'),
        ('ISG-2000', 'ISG-2000'),
    )
    Testbed_Number = models.CharField(max_length=40)
    Testbed_Name = models.CharField(max_length=40)
    #Testbed_Owner = models.CharField(max_length=40)
    Testbed_Owner = models.ForeignKey(User)
    Testbed_Version = models.CharField(max_length=100,editable=False, blank=True)
    #Index_Number = models.IntegerField()
    Index_Number = models.FloatField()
    Platform = models.CharField(max_length=40, choices=PLATFORM_CHOICES)
    Testbed_Location = models.CharField(max_length=40, choices=LOCATION_CHOICES)
    Testbed_Purpose = models.CharField(max_length=40, choices=PURPOSE_CHOICES)
    Access_Information = models.CharField(max_length=100)
    Control_Information = models.CharField(max_length=100)
    Test_Tools_Information_Chassis = models.TextField()
    Test_Tools_Information_GUI = models.TextField()
    Test_Tools_Information_Script = models.TextField()
    Configuration_File = models.TextField()
    JT_Test_Case = models.TextField()
    JT_Verification_Case = models.TextField()
    class Meta:
        verbose_name = "Test Bed Summary"  
        verbose_name_plural = "Test Bed Summary" 
    #def __unicode__(self):
    def __str__(self):
       return '%s(%s)' % (self.Testbed_Number, self.Testbed_Name)
       #return self.Testbed_Name
    #def save(self):
    #       if re.search(r'10.208.85.123', self.Testbed_Location):    
    #           if self.Control_Information:
    #               ip=self.Control_Information.split('/')[0]
    #               (status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    #               if re.search(r'Timeout', output):
    #                   self.Testbed_Version = "N/A0"
    #               else:
    #                   self.Testbed_Version = output
    #       else:
    #           self.Testbed_Version = "N/A4"
    #       super(Testbed, self).save()
    
class Capacity(models.Model):
    module_name = models.CharField(max_length=40)
    module_owner = models.ForeignKey(User)
    index_number = models.CharField(max_length=40)
    #index_number = models.IntegerField()
    capacity_number = models.TextField(blank=True)
    traffic_load = models.TextField(blank=True)
    session_number = models.TextField(blank=True)
    testbed_name = models.ManyToManyField(Testbed)
    release = models.CharField(max_length=40,blank=True)
    ip_schema = models.TextField(blank=True)
    class Meta:
        verbose_name = "Capacity Summary"  
        verbose_name_plural = "Capacity Summary"  
    #def __unicode__(self):
    def __str__(self):
      return '%s %s' % (self.index_number, self.module_name)
      #return self.module_name

class Mode(models.Model):
    mode_name = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Mode List"  
        verbose_name_plural = "Mode List" 
    #def __unicode__(self):
    def __str__(self):
      return self.mode_name

class Version(models.Model):
    version_number = models.CharField(max_length=40)
    class Meta:
        verbose_name = "Version List"  
        verbose_name_plural = "Version List" 
    #def __unicode__(self):
    def __str__(self):
      return self.version_number

class Testcase(models.Model):
    CATEGORY_CHOICES = (
        ('Individual', 'Individual'),
        ('Individual+QC01', 'Individual+QC01'),
        ('Individual+QC08', 'Individual+QC08'),
        ('Individual+QC72+ISSU', 'Individual+QC72+ISSU'),
        ('Individual+QC08+QC72+ISSU', 'Individual+QC08+QC72+ISSU'),
        ('QC01', 'QC01'),
        ('QC08', 'QC08'),
        ('QC24', 'QC24'),
        ('QC72', 'QC72'),
    )
    Category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    Log_Date = models.DateTimeField(default=datetime.datetime.now)
    Testbed_Name = models.ForeignKey('Testbed')    
    #Testbed_Owner = models.ForeignKey(User)
    Testbed_Mode = models.ForeignKey('Mode')
    Version_Number = models.ForeignKey('Version')
    Testcase_Number = models.IntegerField(editable=False, default=1)
    Executed = models.IntegerField(editable=False, default=0)
    Passed = models.IntegerField(editable=False, default=0)
    Failed = models.IntegerField(editable=False, default=0)
    #Execute_Rate = models.CharField(max_length=10,editable=False, blank=True)
    #Pass_Rate = models.CharField(max_length=10,editable=False, blank=True)
    Execute_Rate = models.CharField(max_length=10,editable=False, default="0.00%")
    Pass_Rate = models.CharField(max_length=10,editable=False, default="0.00%", verbose_name="Pass Rate(T)")
    Executed_Pass_Rate = models.CharField(max_length=10,editable=False, default="0.00%", verbose_name="Pass Rate(E)")
    Blocker_PRs = models.TextField(blank=True)
    Comments = models.TextField(blank=True)
    class Meta:
        verbose_name = "Test Case"  
        verbose_name_plural = "Test Case"  
        #app_label = u"Test Cases"  
    def __str__(self):       
        return self.Category
    def save(self):
        Category_list = self.Category.split('+')
        testcase_list=[]
        temp="%s" % self.Testbed_Name
        for item in Category_list:
            testcase_list += TestcaseList.objects.filter(Testbed_Number=temp.split('(')[0],Mode=self.Testbed_Mode,Version=self.Version_Number,Category='%s' % item).distinct()
        self.Testcase_Number=0
        self.Executed=0
        self.Passed=0
        Comments_list=[]
        PR_list=[]
        for i in range(len(testcase_list)):
            self.Testcase_Number+=testcase_list[i].Weight
            self.Executed+=testcase_list[i].Execution
            self.Passed+=testcase_list[i].Result
            if testcase_list[i].Comments:
                Comments_list.append(testcase_list[i].Comments)
            if testcase_list[i].Blocker_PRs:
                PR_list.append(testcase_list[i].Blocker_PRs)
        #if self.Executed and self.Passed:
        self.Comments=string.join(Comments_list,'')
        self.Blocker_PRs=string.join(PR_list,'')
        self.Failed = self.Executed-self.Passed
        self.Execute_Rate = str("%3.2f%%" % ((self.Executed/self.Testcase_Number)*100))
        self.Pass_Rate = str("%3.2f%%" % ((self.Passed/self.Testcase_Number)*100))
        if self.Executed==0:
            self.Executed_Pass_Rate = "0.00%"
        else:
            self.Executed_Pass_Rate = str("%3.2f%%" % ((self.Passed/self.Executed)*100))
        super(Testcase, self).save()

class TestcaseList(models.Model):
    Testbed_Number = models.CharField(max_length=40, blank=True)
    #Testbed_Name = models.CharField(max_length=40, blank=True)
    Module = models.CharField(max_length=100, blank=True)
    Index = models.CharField(max_length=40,editable=False,blank=True)
    Category = models.CharField(max_length=100, blank=True)
    Mode = models.CharField(max_length=100, blank=True)
    Version = models.CharField(max_length=40, blank=True)
    Weight = models.IntegerField(default=1)
    Execution = models.IntegerField(default=0)
    Result = models.IntegerField(default=0)
    Blocker_PRs = models.TextField(blank=True)
    Comments = models.TextField(blank=True)
    class Meta:
        verbose_name = "Test Case List"  
        verbose_name_plural = "Test Case List"
    def __str__(self):       
        return self.Testbed_Number

class TestcaseForm(ModelForm):
    class Meta:
        model = TestcaseList
        filed = ("Module", "Version", "Resule")    
       
class Modulelist(models.Model):
    testbed_number = models.ForeignKey('Testbed')
    testbed_mode = models.ForeignKey('Mode')
    version_number = models.ForeignKey('Version')
    module_list = models.ManyToManyField(Capacity)
    class Meta:
        verbose_name = "Module List"  
        verbose_name_plural = "Module List"
    #def __unicode__(self):
    def __str__(self):
        #return '%s %s' % (self.testbed_number, self.module_list)
        return self.testbed_number.Testbed_Name
    def save(self):
        super(Modulelist, self).save()
        testcase_weight = {"Individual"   : '1',
                          "QC01"  : '1',
                          "QC08"  : '2',
                          "QC24"  : '3',
                          "QC72"  : '4',
                           }
        temp="%s" % self.testbed_number 
        for i in range(len(self.module_list.all())):
            for key, value in testcase_weight.items():
                if not TestcaseList.objects.filter(Testbed_Number=temp.split('(')[0],Mode=self.testbed_mode,Version=self.version_number,Module='%s_%s' % (self.module_list.all()[i],key)).distinct():
                    index_module='%s' % self.module_list.all()[i]
                    index_number=index_module.split()[0]
                    TestcaseList(Category="%s" % key,Weight="%s" % value,Version="%s" % self.version_number,Testbed_Number="%s" % temp.split('(')[0],Mode='%s' % self.testbed_mode,Module='%s_%s' % (self.module_list.all()[i],key),Index='%s' % index_number).save()
        #super(Modulelist, self).save()
        
class TestcaseSummary(models.Model):
    CATEGORY_CHOICES = (
        ('Individual', 'Individual'),
        ('Individual+QC01', 'Individual+QC01'),
        ('Individual+QC08', 'Individual+QC08'),
        ('Individual+QC72+ISSU', 'Individual+QC72+ISSU'),
        ('Individual+QC08+QC72+ISSU', 'Individual+QC08+QC72+ISSU'),
        ('Individual+QC08+QC72+ISSU', 'Individual+QC08++QC24+QC72+ISSU'),
        ('QC01', 'QC01'),
        ('QC08', 'QC08'),
        ('QC24', 'QC24'),
        ('QC72', 'QC72'),
    )
    Category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    Log_Date = models.DateTimeField(default=datetime.datetime.now)
    Testbed_Name = models.ForeignKey('Testbed')    
    Testbed_Owner = models.ForeignKey(User)
    Testbed_Mode = models.ForeignKey('Mode')
    Version_Number = models.ForeignKey('Version')
    Testcase_Number = models.IntegerField(editable=False, default=1)
    Executed = models.IntegerField(editable=False, default=0)
    Passed = models.IntegerField(editable=False, default=0)
    Failed = models.IntegerField(editable=False, default=0)
    #Execute_Rate = models.CharField(max_length=10,editable=False, blank=True)
    #Pass_Rate = models.CharField(max_length=10,editable=False, blank=True)
    Execute_Rate = models.CharField(max_length=10,editable=False, default="0.00%")
    Pass_Rate = models.CharField(max_length=10,editable=False, default="0.00%", verbose_name="Pass Rate(T)")
    Executed_Pass_Rate = models.CharField(max_length=10,editable=False, default="0.00%", verbose_name="Pass Rate(E)")
    Blocker_PRs = models.TextField(blank=True)
    Comments = models.TextField(blank=True)
    class Meta:
        verbose_name = "Test Case Summary"  
        verbose_name_plural = "Test Case Summary"  
        #app_label = u"Test Cases"  
    def __str__(self):       
        return self.Category
    def save(self):
        Category_list = self.Category.split('+')
        testcase_list=[]
        temp="%s" % self.Testbed_Name
        for item in Category_list:
            testcase_list += TestcaseList.objects.filter(Testbed_Number=temp.split('(')[0],Mode=self.Testbed_Mode,Version=self.Version_Number,Category='%s' % item).distinct()
        self.Testcase_Number=0
        self.Executed=0
        self.Passed=0
        Comments_list=[]
        PR_list=[]
        for i in range(len(testcase_list)):
            self.Testcase_Number+=testcase_list[i].Weight
            self.Executed+=testcase_list[i].Execution
            self.Passed+=testcase_list[i].Result
            if testcase_list[i].Comments:
                Comments_list.append(testcase_list[i].Comments)
            if testcase_list[i].Blocker_PRs:
                PR_list.append(testcase_list[i].Blocker_PRs)
        #if self.Executed and self.Passed:
        self.Comments=string.join(Comments_list,'')
        self.Blocker_PRs=string.join(PR_list,'')
        self.Failed = self.Executed-self.Passed
        self.Execute_Rate = str("%3.2f%%" % ((self.Executed/self.Testcase_Number)*100))
        self.Pass_Rate = str("%3.2f%%" % ((self.Passed/self.Testcase_Number)*100))
        if self.Executed==0:
            self.Executed_Pass_Rate = "0.00%"
        else:
            self.Executed_Pass_Rate = str("%3.2f%%" % ((self.Passed/self.Executed)*100))
        super(TestcaseSummary, self).save()


