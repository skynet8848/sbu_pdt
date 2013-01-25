from __future__ import division
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Capacity
from models import Testbed
from models import Modulelist
from models import Testcase
from models import TestcaseList
from models import TestcaseSummary
from models import TestcaseForm
from models import Version
from models import Mode
import datetime
import operator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
import re
import commands

def submit_option(request):
    version_list=[]
    mode_list=[]
    testbed_list=[]
    for item in Version.objects.all():
        version_list.append(item.version_number)    
    for item in Mode.objects.all():
        mode_list.append(item.mode_name)
    for item in Testbed.objects.all():
        testbed_list.append(item.Testbed_Number)    
    if request.method == 'POST':
        url=request.META.get('HTTP_REFERER',"/")
        server_ip=url.split('/')[2]
        version=request.POST["Version_Number"]
        mode=request.POST["Mode"]
        testbed=request.POST["Testbed_Number"]
        category=request.POST["Category"]
        return HttpResponseRedirect('http://%s/submit_result/%s_%s_%s_%s_All' % (server_ip,testbed,mode,version,category))
    else:
        return render_to_response("submit_option.html", {
            "version_list": version_list,
            "mode_list": mode_list,
            "testbed_list": testbed_list,
        })
def submit(request):
    if request.method == 'POST':
        url=request.META.get('HTTP_REFERER',"/")
        option_list=url.split('/')[4].split('_')
	server_ip=url.split('/')[2]
        testbed_number=option_list[0]
        mode=option_list[1]
        version=option_list[2]
        category_all=option_list[3]
        category_list=option_list[3].split('+')
        for category in category_list:
            
            module_list=TestcaseList.objects.filter(Mode="%s" % mode,Category="%s" % category,Version="%s" % version,Testbed_Number="%s" % testbed_number).distinct().order_by('Module')
            for temp in module_list:
                comments = request.POST['%s_comments' % temp.Module]
                result = request.POST['%s_result' % temp.Module]
                execution = request.POST['%s_execution' % temp.Module]
                blocker = request.POST['%s_blocker' % temp.Module]
                #if form.is_valid():
                #testbed=form.cleaned_data['Result']
                item=TestcaseList.objects.get(Module="%s" % temp.Module,Category="%s" % category,Mode="%s" % mode,Version="%s" % version,Testbed_Number="%s" % testbed_number)
                item.Comments=comments
                item.Result=int(result)
                item.Execution=int(execution)
                item.Blocker_PRs=blocker
                item.save()
        return HttpResponseRedirect('http://%s/result/%s_%s_%s_%s_All' % (server_ip,testbed_number,mode,version,category_all))
        #html = "<html><body>It is %s.</body></html>" % option_list
        #return HttpResponse(html)
    else:
        form = TestcaseForm()     
    return render_to_response('message.html', {
            'form': form,
        })

def testbed_search(request):
    query = request.GET.get('q','')
    para_list=request.GET.lists()
    if query:
        if len(para_list)>1:
            option_list=para_list[1][1]
            predicates=[]
            for item in option_list:
                if (item=='Testbed_Owner'):
                    predicates.append(('%s__username__icontains' % item, '%s' % query))
                else:
                    predicates.append(('%s__icontains' % item, '%s' % query))
            q_list=[Q(x) for x in predicates]
            results = Testbed.objects.filter(reduce(operator.or_, q_list)).distinct().order_by('Index_Number')
            option=string.join(option_list,' or ')
        else:
            #qset = (
            #Q(Testbed_Number__icontains=query) |
            #Q(Testbed_Name__icontains=query) |
            #Q(Testbed_Owner__username__icontains=query) |
            #Q(Platform__icontains=query) |
            #Q(Test_Tools_Information_Chassis__icontains=query)  
            #)
            #results = Testbed.objects.filter(qset).distinct().order_by('Index_Number')
            option_list=['Testbed_Number','Testbed_Name','Testbed_Owner__username','Testbed_Purpose','Platform','Test_Tools_Information_Chassis']
            predicates=[]
            for item in option_list:
                predicates.append(('%s__icontains' % item, '%s' % query))
            q_list=[Q(x) for x in predicates]
            results = Testbed.objects.filter(reduce(operator.or_, q_list)).distinct().order_by('Index_Number')
            option="All" 
    else:
        results = []
        option="All"
    results_all= Testbed.objects.all().order_by('Index_Number')
    #if results:
    #    for item in results:
    #            if re.search(r'10.208.85.123', item.Testbed_Location):
    #                if item.Control_Information:
    #                    ip=item.Control_Information.split('/')[0]
    #                    #(status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    #                    output="12.3"
    #                    if re.search(r'Timeout', output):
    #                        item.Testbed_Version = "N/A1"
    #                    else:
    #                        item.Testbed_Version = "12.3"
    #                else:
    #                    item.Testbed_Version = "N/A2"
    #            else:
    #                item.Testbed_Version = "N/A3"
    #            item.save()
    #if results_all:
    #    for item in results_all:
    #            if re.search(r'10.208.85.123', item.Testbed_Location):
    #                if item.Control_Information:
    #                    ip=item.Control_Information.split('/')[0]
    #                    #(status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    #                    output="12.3"
    #                    if re.search(r'Timeout', output):
    #                        item.Testbed_Version = "N/A1"
    #                    else:
    #                        item.Testbed_Version = "12.3"
    #                else:
    #                    item.Testbed_Version = "N/A2"
    #            else:
    #                item.Testbed_Version = "N/A3"
    #            item.save() 
    results_len=str(len(results))
    results_all_len=str(len(results_all))
    return render_to_response("testbed_search.html", {
        "results_len": results_len, 
        "results_all_len": results_all_len,
        "results": results,
        "results_all": results_all,
        "query": query,
        "option": option,
    })

def testbed_search_summary(request):
    query = request.GET.get('q','')
    para_list=request.GET.lists()
    if query:
        if len(para_list)>1:
            option_list=para_list[1][1]
            predicates=[]
            for item in option_list:
                if (item=='Testbed_Owner'):
                    predicates.append(('%s__username__icontains' % item, '%s' % query))
                else:
                    predicates.append(('%s__icontains' % item, '%s' % query))
            q_list=[Q(x) for x in predicates]
            results = Testbed.objects.filter(reduce(operator.or_, q_list)).distinct().order_by('Index_Number')
            option=string.join(option_list,' or ')
        else:
            #qset = (
            #Q(Testbed_Number__icontains=query) |
            #Q(Testbed_Name__icontains=query) |
            #Q(Testbed_Owner__username__icontains=query) |
            #Q(Platform__icontains=query) |
            #Q(Test_Tools_Information_Chassis__icontains=query)
            #)
            #results = Testbed.objects.filter(qset).distinct().order_by('Index_Number')
            option_list=['Testbed_Number','Testbed_Name','Testbed_Owner__username','Testbed_Purpose','Platform','Test_Tools_Information_Chassis']
            predicates=[]
            for item in option_list:
                predicates.append(('%s__icontains' % item, '%s' % query))
            q_list=[Q(x) for x in predicates]
            results = Testbed.objects.filter(reduce(operator.or_, q_list)).distinct().order_by('Index_Number')
            option="All"
    else:
        results = []
        option="All"
    results_all= Testbed.objects.all().order_by('Index_Number')
    #if results:
    #    for item in results:
    #            if re.search(r'10.208.85.123', item.Testbed_Location):
    #                if item.Control_Information:
    #                    ip=item.Control_Information.split('/')[0]
    #                    #(status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    #                    output="12.3"
    #                    if re.search(r'Timeout', output):
    #                        item.Testbed_Version = "N/A1"
    #                    else:
    #                        item.Testbed_Version = "12.3"
    #                else:
    #                    item.Testbed_Version = "N/A2"
    #            else:
    #                item.Testbed_Version = "N/A3"
    #            item.save()
    #if results_all:
    #    for item in results_all:
    #            if re.search(r'10.208.85.123', item.Testbed_Location):
    #                if item.Control_Information:
    #                    ip=item.Control_Information.split('/')[0]
    #                    #(status, output) = commands.getstatusoutput("snmpwalk -c public -v 1 -t 10 %s 1.3.6.1.2.1.1.1 | gawk '{print $12}'" % ip)
    #                    output="12.3"
    #                    if re.search(r'Timeout', output):
    #                        item.Testbed_Version = "N/A1"
    #                    else:
    #                        item.Testbed_Version = "12.3"
    #                else:
    #                    item.Testbed_Version = "N/A2"
    #            else:
    #                item.Testbed_Version = "N/A3"
    #            item.save()
    results_len=str(len(results))
    results_all_len=str(len(results_all))
    return render_to_response("testbed_search_summary.html", {
        "results_len": results_len,
        "results_all_len": results_all_len,
        "results": results,
        "results_all": results_all,
        "query": query,
        "option": option,
    })

def capacity_search(request):
    query = request.GET.get('q','')
    para_list=request.GET.lists()
    if query:
        if len(para_list)>1:
            option_list=para_list[1][1]
            predicates=[]
            for item in option_list:
                if (item=='module_owner'):
                    predicates.append(('%s__username__icontains' % item, '%s' % query))
                elif (item=='testbed_name'):
                    predicates.append(('%s__Testbed_Name__icontains' % item, '%s' % query))
                else:
                    predicates.append(('%s__icontains' % item, '%s' % query))
            q_list=[Q(x) for x in predicates]
            results = Capacity.objects.filter(reduce(operator.or_, q_list)).distinct().order_by('index_number')
            option=string.join(option_list,' or ') 
        else:
            #qset = (
            #Q(index_number__icontains=query) |
            #Q(module_name__icontains=query) |
            #Q(capacity_number__icontains=query) |
            #Q(traffic_load__icontains=query) |
            #Q(session_number__icontains=query) |
            #Q(module_owner__username__icontains=query) | 
            #Q(testbed_name__Testbed_Name__icontains=query) |
            #Q(release__icontains=query) 
            #)
            option_list=['index_number','module_name','capacity_number','traffic_load','session_number','module_owner__username','testbed_name__Testbed_Name','release']
            predicates=[]
            for item in option_list:
                predicates.append(('%s__icontains' % item, '%s' % query))
            q_list=[Q(x) for x in predicates]
            results = Capacity.objects.filter(reduce(operator.or_, q_list)).distinct().order_by('index_number')
            #results = Capacity.objects.filter(qset).distinct().order_by('index_number')
            option="All"
    else:
        results = []
        option="All"
    results_all= Capacity.objects.all().order_by('index_number')
    results_len=str(len(results))
    results_all_len=str(len(results_all))
    return render_to_response("capacity_search.html", {
        "results_len": results_len,
        "results_all_len": results_all_len,
        "results": results,
        "results_all": results_all,
        "query": query,
        "option": option,
    })

def module_list(request, para_list):
    [testbed_number,testbed_mode,version_number]=para_list.split('_')
    #qset = (
    #        Q(testbed_number__icontains=testbed_number) & 
    #        Q(testbed_mode__testbed_mode.mode_name__exect=testbed_mode) &
    #        Q(version_number__version_number__exect=version_number)
    #    )
    module_list=Modulelist.objects.filter(testbed_number__Testbed_Number=testbed_number,testbed_mode__mode_name=testbed_mode,version_number__version_number=version_number).distinct()[0].module_list.all()
    list=[]
    for i in range(len(module_list)):
        list.append(module_list[i].module_name)
        
    results=string.join(list,'/')
    capacity_list=[]
    queryset=Capacity.objects.all()
    for p in queryset:
        if p.module_name in list:
            capacity_list.append(p)
    #html = "<html><body>It is now %s %s %s %s.</body></html>" % (testbed_number,testbed_mode,version_number,capacity_list[0].traffic_load)
    #return HttpResponse(html)
    #for item in capacity_list:
    #    TestcaseList(Testbed_Name='%s' % testbed_number, Module='%s' % item.module_name, Mode='%s' % testbed_mode, Version='%s' % version_number).save()
    return render_to_response("testbed_mode.html", {
        "results": results,
        "capacity_list": capacity_list,
        "testbed_number": testbed_number,
        "testbed_mode": testbed_mode,
        "version_number": version_number,
    })

def module_coverage(request, para_list):
    [testbed_mode,version_number]=para_list.split('_')
    mode_list = {"IPv4"   : '1',
                 "LSYS"   : '2',
                 "L2"     : '3',
                 "IPv4v6" : '4',
                 }
    #qset = (
    #        Q(testbed_number__icontains=testbed_number) & 
    #        Q(testbed_mode__testbed_mode.mode_name__exect=testbed_mode) &
    #        Q(version_number__version_number__exect=version_number)
    #    )
    if (testbed_mode!="IPv4")&(testbed_mode!="IPv4v6") :
        module_list=Modulelist.objects.filter(testbed_mode__mode_name__icontains="%s" % testbed_mode,version_number__version_number=version_number).all()
    else:
        module_list=Modulelist.objects.filter(~Q(testbed_mode__mode_name__icontains="L2"),~Q(testbed_mode__mode_name__icontains="SRX"),~Q(testbed_mode__mode_name__icontains="LSYS"),testbed_mode__mode_name__icontains="-%s-" % testbed_mode,version_number__version_number=version_number).all()
    list=[]
    #for i in range(len(module_list)):
    #    list.append(module_list[i].module_name)
    # 
    #results=string.join(list,'/')
    capacity_list=[]
    if (testbed_mode=="IPv4v6"):
        qset = (
             Q(index_number__startswith="4.") |
             Q(index_number__startswith="1.") 
         )
        queryset=Capacity.objects.filter(qset).order_by("index_number").all()
    else: 
        queryset=Capacity.objects.filter(index_number__startswith="%s." % mode_list[testbed_mode]).order_by("index_number").all()
    for p in queryset:
        capacity_list.append(p.module_name)
        #if p.module_name in list:
        #    capacity_list.append(p)
    #temp_list=capacity_list
    capacity_dict={}
    for item in capacity_list:
        capacity_dict[item]=0
    module_list_dict={}
    for item in module_list:
        module_list_dict[item]=len(item.module_list.all())
    module_list_sorted=sorted(module_list_dict.iteritems(), key=lambda d:d[1], reverse=True)
    module_list=[]
    for item in module_list_sorted:
        module_list.append(item[0])
    for item in module_list:
        temp=item.testbed_number
        coverage="%3.2f%%" % ((len(item.module_list.all())/len(capacity_list))*100)
        temp_list=[str(temp)]+["%s(%s/%s)" % (str(coverage),str(len(item.module_list.all())),str(len(capacity_list)))]+['N']*len(capacity_list)
        list1=[]
        for temp in item.module_list.all(): 
            for i in range(len(capacity_list)):   
                #if "%s" % str(temp.module_name) == "%s" % str(capacity_list[i]):
                if temp.module_name == capacity_list[i]:
                    temp_list[i+2]="Y"
                    capacity_dict["%s" % capacity_list[i]]+=1
                
        
        #list.append(temp_list)
    capacity_list_sorted=sorted(capacity_dict.iteritems(), key=lambda d:d[1], reverse=True)
    capacity_list=[]
    for item in capacity_list_sorted:
        capacity_list.append(item[0])
    for item in module_list:
        temp=item.testbed_number
        coverage="%3.2f%%" % ((len(item.module_list.all())/len(capacity_list))*100)
        temp_list=[str(temp)]+["%s(%s/%s)" % (str(coverage),str(len(item.module_list.all())),str(len(capacity_list)))]+['N']*len(capacity_list)
        list1=[]
        for temp in item.module_list.all(): 
            for i in range(len(capacity_list)):   
                #if "%s" % str(temp.module_name) == "%s" % str(capacity_list[i]):
                if temp.module_name == capacity_list[i]:
                    temp_list[i+2]="Y"
                    capacity_dict["%s" % capacity_list[i]]+=1
        list.append(temp_list)
    total_valid=0
    for i in range(len(capacity_list_sorted)):
        if capacity_list_sorted[i][1]!=0:
            total_valid+=1
    coverage="%3.2f%%" % ((total_valid/len(capacity_list))*100)
    total_coverage=['Total Coverage']+["%s(%s/%s)" % (str(coverage),str(total_valid),str(len(capacity_list)))]+['N']*len(capacity_list)
    for i in range(len(capacity_list_sorted)):
        if capacity_list_sorted[i][1]!=0:
            total_coverage[i+2]="Y"
    #html = "<html><body>It is now %s.</body></html>" % module_list[0].module_list.all()[0].module_name
    #html = "<html><body>It is now %s.</body></html>" % list[0]
    #html = "<html><body>It is now %s.</body></html>" % list
    #return HttpResponse(html)
    
    colspan=len(capacity_list)+2
    return render_to_response("module_coverage.html", {
        "capacity_list": capacity_list,
        "testbed_mode": testbed_mode,
        "version_number": version_number,
        "colspan": colspan,
        "list": list,
        "total_coverage": total_coverage,
    })

def module_version(request, version_number):
    module=Modulelist.objects.all()
    module_list=Modulelist.objects.filter(version_number__version_number=version_number).all()[0].module_list.all()
    item_list=[]
    for item in module:
        for re in item.module_list.all():
           item_list.append(re.module_name)
    list=[]
    for i in range(len(module_list)):
        list.append(module_list[i].module_name)

    results=string.join(list,'/')
    html = "<html><body>It is now %s.</body></html>" % item_list
    return HttpResponse(html)
def testtools_search(request, testtools_name):
    if not re.findall("\(\d+\.\d+\.\d+\.\d+\)",testtools_name):
        testtools_name=testtools_name+"\(\d+\.\d+\.\d+\.\d+\)"
    else:
        testtools_name=testtools_name.replace('(','\(')
        testtools_name=testtools_name.replace(')','\)')
        testtools_name=testtools_name.replace('.','\.')
    testbed_list=Testbed.objects.all()
    #testbed_list=Testbed.objects.filter(Test_Tools_Information_Chassis=testtools_name).all()[0].module_list.all()
    #testbed_list=Testbed.objects.filter(Test_Tools_Information_Chassis=testtools_name).all()
    item_list=[]
    ixload_list=[]
    avalanche_list=[]
    ixexplorer_list=[]
    testnumber_list=[]
    for item in testbed_list:
        item_list.append(item.Test_Tools_Information_Chassis)
        if re.findall("%s:\d+/\d+\[\d+:\d+\]" % testtools_name,item.Test_Tools_Information_Chassis):
            for temp in (re.findall("%s:\d+/\d+\[\d+:\d+\]" % testtools_name,item.Test_Tools_Information_Chassis)):
                temp_list=["%s" % temp, "%s(%s)" % (item.Testbed_Number,item.Testbed_Name)]
                ixload_list.append(temp_list)
        #if re.findall("IxExplorer\(\d+\.\d+\.\d+\.\d+\):\d+/\d+\[\d+:\d+\]",item.Test_Tools_Information_Chassis):
        #    for temp in (re.findall("IxExplorer\(\d+\.\d+\.\d+\.\d+\):\d+/\d+\[\d+:\d+\]",item.Test_Tools_Information_Chassis)):
        #        temp_list=["%s" % temp, "%s" % item.Testbed_Number]
        #        ixexplorer_list.append(temp_list)
        #if re.findall("Avalanche\(\d+\.\d+\.\d+\.\d+\):\d+\[\d+\]",item.Test_Tools_Information_Chassis):
        #    for temp in (re.findall("Avalanche\(\d+\.\d+\.\d+\.\d+\):\d+\[\d+\]",item.Test_Tools_Information_Chassis)):
        #        temp_list=["%s" % temp, "%s" % item.Testbed_Number]
        #        avalanche_list.append(temp_list)
        
        #testnumber_list.append(item.Testbed_Number)
    #ixload_list = re.findall("IxLoad\(\d+\.\d+\.\d+\.\d+\):\d+/\d+\[\d+:\d+\]",item_list[0])
    #html = "<html><body>It is now %s.</body></html>" % ixload_list
    #return HttpResponse(html)
    ixload=[]
    ixload_all_list=[]
    ixload_active=[]
    ixload_list.sort()
    for item in ixload_list:
        ixload_active.append([re.findall("%s" % testtools_name,item[0])[0],re.findall("\d+/\d+",item[0])[0],item[1]])
        if not re.findall("%s:\d+/" % testtools_name,item[0])[0] in ixload:
            ixload.append(re.findall("%s:\d+/" % testtools_name,item[0])[0])
            max_slot,max_port=re.findall("\d+:\d+",item[0])[0].split(':')
            slot,port=re.findall("\d+/\d+",item[0])[0].split('/')
            rowspan=int(max_port)
            ixload_all=[]
            for port_num in range(int(max_port)):
                ixload_all.append([re.findall("%s" % testtools_name,item[0])[0],"%s/%s" % (slot,port_num+1),'Null',"%s" % rowspan])    
            ixload_all_list.append(ixload_all)
    for item in ixload_list:
        for j in range(len(ixload_all_list)):
            for i in range(len(ixload_all_list[j])):
                if re.findall("%s" % testtools_name,item[0])[0]==ixload_all_list[j][i][0] and re.findall("\d+/\d+",item[0])[0]==ixload_all_list[j][i][1]:
                    ixload_all_list[j][i][2]=item[1]
                    
    #html = "<html><body>It is now %s.</body></html>" % testtools_name
    #return HttpResponse(html)
    return render_to_response("testtools_search.html", {
        "ixload_all_list": ixload_all_list,
        "avalanche_list": avalanche_list,
        "ixexplorer_list": ixexplorer_list,
    })

def testtools_search_all(request):
    testtools_name="\w+\(\d+\.\d+\.\d+\.\d+\)"
    testbed_list=Testbed.objects.all()
    #testbed_list=Testbed.objects.filter(Test_Tools_Information_Chassis=testtools_name).all()[0].module_list.all()
    #testbed_list=Testbed.objects.filter(Test_Tools_Information_Chassis=testtools_name).all()
    item_list=[]
    ixload_list=[]
    avalanche_list=[]
    ixexplorer_list=[]
    testnumber_list=[]
    for item in testbed_list:
        item_list.append(item.Test_Tools_Information_Chassis)
        if re.findall("%s:\d+/\d+\[\d+:\d+\]" % testtools_name,item.Test_Tools_Information_Chassis):
            for temp in (re.findall("%s:\d+/\d+\[\d+:\d+\]" % testtools_name,item.Test_Tools_Information_Chassis)):
                temp_list=["%s" % temp, "%s(%s)" % (item.Testbed_Number,item.Testbed_Name)]
                ixload_list.append(temp_list)
        #if re.findall("IxExplorer\(\d+\.\d+\.\d+\.\d+\):\d+/\d+\[\d+:\d+\]",item.Test_Tools_Information_Chassis):
        #    for temp in (re.findall("IxExplorer\(\d+\.\d+\.\d+\.\d+\):\d+/\d+\[\d+:\d+\]",item.Test_Tools_Information_Chassis)):
        #        temp_list=["%s" % temp, "%s" % item.Testbed_Number]
        #        ixexplorer_list.append(temp_list)
        #if re.findall("Avalanche\(\d+\.\d+\.\d+\.\d+\):\d+\[\d+\]",item.Test_Tools_Information_Chassis):
        #    for temp in (re.findall("Avalanche\(\d+\.\d+\.\d+\.\d+\):\d+\[\d+\]",item.Test_Tools_Information_Chassis)):
        #        temp_list=["%s" % temp, "%s" % item.Testbed_Number]
        #        avalanche_list.append(temp_list)

        #testnumber_list.append(item.Testbed_Number)
    #ixload_list = re.findall("IxLoad\(\d+\.\d+\.\d+\.\d+\):\d+/\d+\[\d+:\d+\]",item_list[0])
    #html = "<html><body>It is now %s.</body></html>" % ixload_list
    #return HttpResponse(html)
    ixload=[]
    ixload_all_list=[]
    ixload_active=[]
    ixload_list_sort=[]
    for item in ixload_list:
        if int(re.findall(":\d+/", item[0])[0].split(':')[1].split('/')[0])<10:
            temp_list=["%s" % item[0].replace(':%s/' % re.findall(":\d+/", item[0])[0].split(':')[1].split('/')[0],':0%s/' % re.findall(":\d+/", item[0])[0].split(':')[1].split('/')[0]),"%s" % item[1]]            
            ixload_list_sort.append(temp_list)   
        else:
            ixload_list_sort.append(item)
    ixload_list_sort.sort()  
    ixload_list=[]
    for item in ixload_list_sort:
        if re.findall(":0\d+/", item[0]):
            temp_list=["%s" % item[0].replace(':0%s/' % re.findall(":0\d+/", item[0])[0].split(':0')[1].split('/')[0],':%s/' % re.findall(":0\d+/", item[0])[0].split(':0')[1].split('/')[0]), "%s" % item[1]]
            ixload_list.append(temp_list)
        else:
            ixload_list.append(item)
    for item in ixload_list:
        ixload_active.append([re.findall("%s" % testtools_name,item[0])[0],re.findall("\d+/\d+",item[0])[0],item[1]])
        if not re.findall("%s:\d+/" % testtools_name,item[0])[0] in ixload:
            ixload.append(re.findall("%s:\d+/" % testtools_name,item[0])[0])
            max_slot,max_port=re.findall("\d+:\d+",item[0])[0].split(':')
            slot,port=re.findall("\d+/\d+",item[0])[0].split('/')
            rowspan=int(max_port)
            ixload_all=[]
            for port_num in range(int(max_port)):
                ixload_all.append([re.findall("%s" % testtools_name,item[0])[0],"%s/%s" % (slot,port_num+1),'Null',"%s" % rowspan])
            ixload_all_list.append(ixload_all)
    for item in ixload_list:
        for j in range(len(ixload_all_list)):
            for i in range(len(ixload_all_list[j])):
                if re.findall("%s" % testtools_name,item[0])[0]==ixload_all_list[j][i][0] and re.findall("\d+/\d+",item[0])[0]==ixload_all_list[j][i][1]:
                    ixload_all_list[j][i][2]=item[1]

    #html = "<html><body>It is now %s.</body></html>" % ixload_all_list
    #return HttpResponse(html)
    return render_to_response("testtools_search.html", {
        "ixload_all_list": ixload_all_list,
        "avalanche_list": avalanche_list,
        "ixexplorer_list": ixexplorer_list,
    })
    
def testcase_status(request, category_version):
    category=category_version.split('_')[0]
    version=category_version.split('_')[1]
    testbed_list=[]
    testcase_all_list=[]
    testcase_list=Testcase.objects.filter(Category=category,Version_Number__version_number=version).order_by("Log_Date").all()
    for item in testcase_list:
        if not "%s" % item.Testbed_Name in testbed_list:
            testbed_list.append("%s" % item.Testbed_Name)
        #temp_list=["%s" % item.Category,"%s" % item.Testbed_Name,"%s" % item.Testbed_Mode,"%s" % item.Version_Number,"%s" % item.Testcase_Number,"%s" % item.Executed,"%s" % item.Passed,"%s" % item.Failed,"%s" % item.Execute_Rate,"%s" % item.Pass_Rate,"%s" % item.Log_Date]
        #testcase_all_list.append(temp_list)
    testcase_latest_list=[]
    for temp in testbed_list:
        testbed_number=temp.split('(')[0]
        testcase_list=Testcase.objects.filter(Category=category,Version_Number__version_number=version,Testbed_Name__Testbed_Number=testbed_number).order_by("-Log_Date").all()
        testcase_all_list=[]
        for item in testcase_list:
            temp_list=["%s" % item.Category,"%s" % item.Testbed_Name,"%s" % item.Testbed_Mode,"%s" % item.Version_Number,"%s" % item.Testcase_Number,"%s" % item.Executed,"%s" % item.Passed,"%s" % item.Failed,"%s" % item.Execute_Rate,"%s" % item.Pass_Rate,"%s" % item.Log_Date]
            testcase_all_list.append(temp_list)
        testcase_latest_list.append(testcase_all_list[0])
    testcase_total=0
    executed_total=0
    passed_total=0
    failed_total=0
    executed_rate_total=0
    pass_rate_total=0
    for item in testcase_latest_list:
        testcase_total+=int(item[4])
        executed_total+=int(item[5])
        passed_total+=int(item[6]) 
    failed_total=executed_total-passed_total
    executed_rate_total=str("%3.2f%%" % ((executed_total/testcase_total)*100))
    pass_rate_total=str("%3.2f%%" % ((passed_total/testcase_total)*100))
    temp_list=["","","Total","","%s" % str(testcase_total),"%s" % str(executed_total),"%s" % str(passed_total),"%s" % str(failed_total),"%s" % executed_rate_total,"%s" % pass_rate_total,""]
    testcase_latest_list.append(temp_list)
    #html = "<html><body>It is now %s.</body></html>" % testcase_list
    #return HttpResponse(html)
    return render_to_response("testcase_status.html", {
        "testcase_latest_list": testcase_latest_list,
    })

def submit_result(request, para_list):
    if len(para_list.split('_'))==5:
        testbed_number=para_list.split('_')[0]
        mode=para_list.split('_')[1]
        version=para_list.split('_')[2]
        category=para_list.split('_')[3]
        category_list=category.split('+')
        result=para_list.split('_')[4]
        testcase_weight = {"Individual"   : '1',
                          "ISSU"  : '1',
                          "QC01"  : '1',
                          "QC08"  : '2',
                          "QC24"  : '3',
                          "QC72"  : '4',
                           }
        testcase_list=[]
        if result=='All':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Executed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item,Execution=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Passed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item,Result=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        else:
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item,Execution=testcase_weight['%s' % item],Result=0).order_by("Module").all()
                testcase_list+=item_list
        #html = "<html><body>It is now %s.</body></html>" % testcase_list[0].Testbed_Mode
        #return HttpResponse(html)
        return render_to_response("submit_result.html", {
            "testcase_list": testcase_list,
            "testbed_number": testbed_number,
            "mode": mode,
            "version": version,
            "result": result,
        })
    elif len(para_list.split('_'))==3:
        version=para_list.split('_')[0]
        category=para_list.split('_')[1]
        category_list=category.split('+')
        result=para_list.split('_')[2]
        testcase_weight = {"Individual"   : '1',
                          "ISSU"  : '1',
                          "QC01"  : '1',
                          "QC08"  : '2',
                          "QC24"  : '3',
                          "QC72"  : '4',
                           }
        testcase_list=[]
        if result=='All':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Executed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item,Execution=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Passed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item,Result=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        else:
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item,Execution=testcase_weight['%s' % item],Result=0).order_by("Module").all()
                testcase_list+=item_list
        #html = "<html><body>It is now %s.</body></html>" % testcase_list[0].Testbed_Mode
        #return HttpResponse(html)
        return render_to_response("submit_result.html", {
            "testcase_list": testcase_list,
            "version": version,
            "result": result,
        })
    else:
        PASS

def testcase_result(request, para_list):
    if len(para_list.split('_'))==5:
        testbed_number=para_list.split('_')[0]
        mode=para_list.split('_')[1]
        version=para_list.split('_')[2]
        category=para_list.split('_')[3]
        category_list=category.split('+')
        result=para_list.split('_')[4]
        testcase_weight = {"Individual"   : '1',
                          "ISSU"  : '1',
                          "QC01"  : '1',
                          "QC08"  : '2',
                          "QC24"  : '3',
                          "QC72"  : '4',
                           }
        testcase_list=[]
        if result=='All':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Executed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item,Execution=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Passed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item,Result=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        else:
            for item in category_list:
                item_list=TestcaseList.objects.filter(Testbed_Number=testbed_number,Mode=mode,Version=version,Category=item,Execution=testcase_weight['%s' % item],Result=0).order_by("Module").all()
                testcase_list+=item_list
        #html = "<html><body>It is now %s.</body></html>" % testcase_list[0].Testbed_Mode
        #return HttpResponse(html)
        return render_to_response("testcase_result.html", {
            "testcase_list": testcase_list,
            "testbed_number": testbed_number,
            "mode": mode,
            "version": version,
            "result": result,
        })
    elif len(para_list.split('_'))==3:
        version=para_list.split('_')[0]
        category=para_list.split('_')[1]
        category_list=category.split('+')
        result=para_list.split('_')[2]
        testcase_weight = {"Individual"   : '1',
                          "ISSU"  : '1',
                          "QC01"  : '1',
                          "QC08"  : '2',
                          "QC24"  : '3',
                          "QC72"  : '4',
                           }
        testcase_list=[]
        if result=='All':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Executed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item,Execution=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        elif result=='Passed':
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item,Result=testcase_weight['%s' % item]).order_by("Module").all()
                testcase_list+=item_list
        else:
            for item in category_list:
                item_list=TestcaseList.objects.filter(Version=version,Category=item,Execution=testcase_weight['%s' % item],Result=0).order_by("Module").all()
                testcase_list+=item_list
        #html = "<html><body>It is now %s.</body></html>" % testcase_list[0].Testbed_Mode
        #return HttpResponse(html)
        return render_to_response("testcase_result.html", {
            "testcase_list": testcase_list,
            "version": version,
            "result": result,
        })
    else:
        PASS 

def testcase_summary(request, category_version):
    category=category_version.split('_')[0]
    version=category_version.split('_')[1]
    testbed_list=[]
    testcase_all_list=[]
    testcase_list=TestcaseSummary.objects.filter(Category=category,Version_Number__version_number=version).order_by("Log_Date").all()
    for item in testcase_list:
        if not "%s" % item.Testbed_Name in testbed_list:
            testbed_list.append("%s" % item.Testbed_Name)
        #temp_list=["%s" % item.Category,"%s" % item.Testbed_Name,"%s" % item.Testbed_Mode,"%s" % item.Version_Number,"%s" % item.Testcase_Number,"%s" % item.Executed,"%s" % item.Passed,"%s" % item.Failed,"%s" % item.Execute_Rate,"%s" % item.Pass_Rate,"%s" % item.Log_Date]
        #testcase_all_list.append(temp_list)
    testcase_latest_list=[]
    for temp in testbed_list:
        testbed_number=temp.split('(')[0]
        testcase_list=TestcaseSummary.objects.filter(Category=category,Version_Number__version_number=version,Testbed_Name__Testbed_Number=testbed_number).order_by("-Log_Date").all()
        testcase_all_list=[]
        for item in testcase_list:
            testbed="%s" % item.Testbed_Name
            testbed_number=testbed.split('(')[0]
            pr_list=item.Blocker_PRs.split()
            pr_number_list=[]
            for pr_item in pr_list:
                pr_number_list.append(pr_item.split('-')[1])
            temp_list=["%s" % item.Category,"%s" % item.Testbed_Name,"%s" % item.Testbed_Mode,"%s" % item.Version_Number,"%s" % item.Testcase_Number,"%s" % item.Executed,"%s" % item.Passed,"%s" % item.Failed,"%s" % item.Execute_Rate,"%s" % item.Pass_Rate,"%s" % item.Executed_Pass_Rate,"%s" % item.Log_Date,"%s" % testbed_number,pr_number_list,"%s" % item.Comments,"%s" % item.Testbed_Owner]
            testcase_all_list.append(temp_list)
        testcase_latest_list.append(testcase_all_list[0])
    testcase_total=0
    executed_total=0
    passed_total=0
    failed_total=0
    executed_rate_total=0
    pass_rate_total=0
    executed_pass_rate_total=0
    for item in testcase_latest_list:
        testcase_total+=int(item[4])
        executed_total+=int(item[5])
        passed_total+=int(item[6]) 
    failed_total=executed_total-passed_total
    executed_rate_total=str("%3.2f%%" % ((executed_total/testcase_total)*100))
    pass_rate_total=str("%3.2f%%" % ((passed_total/testcase_total)*100))
    if executed_total==0:
        executed_pass_rate_total="0.00%"
    else:
        executed_pass_rate_total=str("%3.2f%%" % ((passed_total/executed_total)*100))
    temp_list=["","","Total","","%s" % str(testcase_total),"%s" % str(executed_total),"%s" % str(passed_total),"%s" % str(failed_total),"%s" % executed_rate_total,"%s" % pass_rate_total,"%s" % executed_pass_rate_total,""]
    testcase_total_list=[]
    testcase_total_list.append(temp_list)
    #html = "<html><body>It is now %s.</body></html>" % testcase_latest_list[-1][12]
    #return HttpResponse(html)
    return render_to_response("testcase_summary.html", {
        "testcase_latest_list": testcase_latest_list,
        "testcase_total_list": testcase_total_list,
    })
def testcase_summary_external(request, category_version):
    category=category_version.split('_')[0]
    version=category_version.split('_')[1]
    testbed_list=[]
    testcase_all_list=[]
    testcase_list=TestcaseSummary.objects.filter(Category=category,Version_Number__version_number=version).order_by("Log_Date").all()
    for item in testcase_list:
        if not "%s" % item.Testbed_Name in testbed_list:
            testbed_list.append("%s" % item.Testbed_Name)
        #temp_list=["%s" % item.Category,"%s" % item.Testbed_Name,"%s" % item.Testbed_Mode,"%s" % item.Version_Number,"%s" % item.Testcase_Number,"%s" % item.Executed,"%s" % item.Passed,"%s" % item.Failed,"%s" % item.Execute_Rate,"%s" % item.Pass_Rate,"%s" % item.Log_Date]
        #testcase_all_list.append(temp_list)
    testcase_latest_list=[]
    for temp in testbed_list:
        testbed_number=temp.split('(')[0]
        testcase_list=TestcaseSummary.objects.filter(Category=category,Version_Number__version_number=version,Testbed_Name__Testbed_Number=testbed_number).order_by("-Log_Date").all()
        testcase_all_list=[]
        for item in testcase_list:
            testbed="%s" % item.Testbed_Name
            testbed_number=testbed.split('(')[0]
            external_total=TestcaseSummary.objects.filter(Category="Individual+QC72+ISSU",Version_Number__version_number=item.Version_Number,Testbed_Mode__mode_name=item.Testbed_Mode,Testbed_Name__Testbed_Number=testbed_number).order_by("-Log_Date").all()[0].Testcase_Number
            external_executed_rate_total=str("%3.2f%%" % ((int(item.Executed)/int(external_total))*100))
            external_pass_rate_total=str("%3.2f%%" % ((int(item.Passed)/int(external_total))*100))
            if int(item.Executed)==0:
                external_executed_pass_rate_total="0.00%"
            else:
                external_executed_pass_rate_total=str("%3.2f%%" % ((int(item.Passed)/int(item.Executed))*100))
            pr_list=item.Blocker_PRs.split()
            pr_number_list=[]
            for pr_item in pr_list:
                pr_number_list.append(pr_item.split('-')[1])
            temp_list=["%s" % item.Category,"%s" % item.Testbed_Name,"%s" % item.Testbed_Mode,"%s" % item.Version_Number,"%s" % external_total,"%s" % item.Executed,"%s" % item.Passed,"%s" % item.Failed,"%s" % external_executed_rate_total,"%s" % external_pass_rate_total,"%s" % external_executed_pass_rate_total,"%s" % item.Log_Date,"%s" % testbed_number,pr_number_list,"%s" % item.Comments]
            testcase_all_list.append(temp_list)
        testcase_latest_list.append(testcase_all_list[0])
    testcase_total=0
    executed_total=0
    passed_total=0
    failed_total=0
    executed_rate_total=0
    pass_rate_total=0
    executed_pass_rate_total=0
    external_total=0
    for item in testcase_latest_list:
        external_total=TestcaseSummary.objects.filter(Category="Individual+QC72+ISSU",Version_Number__version_number=item[3],Testbed_Mode__mode_name=item[2],Testbed_Name__Testbed_Number=item[1].split('(')[0]).order_by("-Log_Date").all()[0].Testcase_Number
        testcase_total+=int(external_total)
        #testcase_total+=int(item[4])
        executed_total+=int(item[5])
        passed_total+=int(item[6]) 
    failed_total=executed_total-passed_total
    executed_rate_total=str("%3.2f%%" % ((executed_total/testcase_total)*100))
    pass_rate_total=str("%3.2f%%" % ((passed_total/testcase_total)*100))
    if executed_total==0:
        executed_pass_rate_total="0.00%"
    else:
        executed_pass_rate_total=str("%3.2f%%" % ((passed_total/executed_total)*100))
    temp_list=["","","Total","","%s" % str(testcase_total),"%s" % str(executed_total),"%s" % str(passed_total),"%s" % str(failed_total),"%s" % executed_rate_total,"%s" % pass_rate_total,"%s" % executed_pass_rate_total,""]
    testcase_total_list=[]
    testcase_total_list.append(temp_list)
    #html = "<html><body>It is now %s.</body></html>" % external_total
    #return HttpResponse(html)
    return render_to_response("testcase_summary_external.html", {
        "testcase_latest_list": testcase_latest_list,
        "testcase_total_list": testcase_total_list,
        "version": version,
    })
# Create your views here.
