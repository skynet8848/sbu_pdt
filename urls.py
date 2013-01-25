from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib import flatpages
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sbu_pdt.views.home', name='home'),
    # url(r'^sbu_pdt/', include('sbu_pdt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^$', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^submit/', 'sbu_pdt.regression.views.submit_option'),
	url(r'^submit_result/(?P<para_list>.*)/$','sbu_pdt.regression.views.submit_result'),
    url(r'^message/', 'sbu_pdt.regression.views.submit'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/tester/tools/python/python_project/sbu_pdt/media'}),
    url(r'^testbed/$','sbu_pdt.regression.views.testbed_search'),
    url(r'^testbed_summary/$','sbu_pdt.regression.views.testbed_search_summary'),
    url(r'^module/$','sbu_pdt.regression.views.capacity_search'),
    url(r'^(?P<para_list>slt\d+-dut\d+_.*)/$','sbu_pdt.regression.views.module_list'),
    url(r'^coverage/(?P<para_list>.*)/$','sbu_pdt.regression.views.module_coverage'),
    #url(r'^(?P<para_list>.*)/$','sbu_pdt.regression.views.module_list'),
    url(r'^module/(?P<version_number>.*)/$','sbu_pdt.regression.views.module_version'),
    url(r'^testtools/(?P<testtools_name>.*)/$','sbu_pdt.regression.views.testtools_search'),
    url(r'^testtools/$','sbu_pdt.regression.views.testtools_search_all'),
    url(r'^testcases/(?P<category_version>.*)/$','sbu_pdt.regression.views.testcase_status'),
    url(r'^result/(?P<para_list>.*)/$','sbu_pdt.regression.views.testcase_result'),
    url(r'^summary/(?P<category_version>.*)/$','sbu_pdt.regression.views.testcase_summary'),
    url(r'^summary_external/(?P<category_version>.*)/$','sbu_pdt.regression.views.testcase_summary_external'),
    url(r'', include('django.contrib.flatpages.urls')),
)
