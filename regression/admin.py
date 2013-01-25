from sbu_pdt.regression.models import Capacity
from sbu_pdt.regression.models import Modulelist
from sbu_pdt.regression.models import Testbed
from sbu_pdt.regression.models import Mode
from sbu_pdt.regression.models import Version
from sbu_pdt.regression.models import Testcase
from sbu_pdt.regression.models import TestcaseList
from sbu_pdt.regression.models import TestcaseSummary
from django.contrib import admin
import string
def get_module_list(self,obj):
    return '%s' % (obj.modulelist.module_list)

class CapacityAdmin(admin.ModelAdmin):
    def get_testbed_list(self,obj):
        testbed_list=obj.testbed_name.all()
        list=[]
        for i in range(len(testbed_list)):
            list.append(testbed_list[i].Testbed_Name)
        results=string.join(list,',')
        return '%s' % results
    get_testbed_list.short_description = 'Testbed List'
    list_display= ('index_number','module_name','capacity_number','traffic_load','session_number','release','module_owner','get_testbed_list','ip_schema')
    filter_horizontal=('testbed_name',)
    ordering= ('index_number',)
    search_fields= ('index_number','module_name','capacity_number','traffic_load','session_number','release','module_owner__username','testbed_name__Testbed_Name')
admin.site.register(Capacity, CapacityAdmin)

class TestbedAdmin(admin.ModelAdmin):
    list_display= ('Index_Number','Testbed_Number','Testbed_Name','Testbed_Owner','Platform','Testbed_Location','Testbed_Purpose','Testbed_Version','Access_Information','Control_Information','Test_Tools_Information_Chassis','Test_Tools_Information_GUI','Test_Tools_Information_Script','Configuration_File','JT_Test_Case','JT_Verification_Case',)
    ordering= ('Index_Number','Testbed_Number',)
    search_fields= ('Testbed_Number','Testbed_Name','Testbed_Owner__username','Testbed_Location','Testbed_Purpose','Control_Information','Test_Tools_Information_Chassis',)
admin.site.register(Testbed, TestbedAdmin)

class ModulelistAdmin(admin.ModelAdmin):
    def get_module_list(self,obj):
        module_list=obj.module_list.all()
        list=[]
        for i in range(len(module_list)):
            list.append(module_list[i].module_name)
        results=string.join(list,',')
        return '%s' % results
    get_module_list.short_description = 'Module List'
    ordering= ('id',)
    search_fields= ('testbed_number__Testbed_Number','testbed_mode__mode_name','version_number__version_number','module_list__module_name')
    list_display= ('testbed_number','testbed_mode','version_number','get_module_list')
    filter_horizontal=('module_list',)
admin.site.register(Modulelist, ModulelistAdmin)

class ModeAdmin(admin.ModelAdmin):
    ordering= ('mode_name',)
    list_display= ('mode_name',)
admin.site.register(Mode, ModeAdmin)

class VersionAdmin(admin.ModelAdmin):
    ordering= ('version_number',)
    list_display= ('version_number',)
admin.site.register(Version, VersionAdmin)

class TestcaseAdmin(admin.ModelAdmin):
    #ordering= ('Testbed_Mode__mode_name','Category')
    ordering= ('Category','Testbed_Mode__mode_name')
    search_fields= ('Category','Testbed_Name__Testbed_Number','Version_Number__version_number','Blocker_PRs','Comments','Testbed_Mode__mode_name')
    list_display= ('Category','Testbed_Name','Testbed_Mode','Version_Number','Testcase_Number','Executed','Passed','Failed','Execute_Rate','Pass_Rate','Executed_Pass_Rate','Log_Date','Blocker_PRs','Comments')
admin.site.register(Testcase, TestcaseAdmin)

class TestcaseListAdmin(admin.ModelAdmin):
    ordering= ('Module','Weight')
    search_fields= ('Testbed_Number','Module','Mode','Version','Weight','Execution','Result','Index','Blocker_PRs','Comments')
    list_display= ('Testbed_Number','Module','Category','Mode','Version','Weight','Execution','Result','Index','Blocker_PRs','Comments')
admin.site.register(TestcaseList, TestcaseListAdmin)

class TestcaseSummaryAdmin(admin.ModelAdmin):
    #ordering= ('Testbed_Mode__mode_name','Category')
    ordering= ('Category','Testbed_Mode__mode_name')
    search_fields= ('Category','Testbed_Name__Testbed_Number','Testbed_Owner__username','Version_Number__version_number','Blocker_PRs','Comments','Testbed_Mode__mode_name')
    list_display= ('Category','Testbed_Name','Testbed_Owner','Testbed_Mode','Version_Number','Testcase_Number','Executed','Passed','Failed','Execute_Rate','Pass_Rate','Executed_Pass_Rate','Log_Date','Blocker_PRs','Comments')
admin.site.register(TestcaseSummary, TestcaseSummaryAdmin)

