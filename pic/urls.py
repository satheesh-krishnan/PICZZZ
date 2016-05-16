from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from pic import views
import django
from pic.models import Photos

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
        url(r'^userhome/$',views.userhome,name="userhome"),
        url(r'^logout/$',views.user_logout,name="logout"),
        url(r'^media/(?P<path>.*)$',django.views.static.serve,{"document_root":settings.MEDIA_ROOT}),
        url(r'^youralbum/$',views.youralbum,name="youralbum"),
    url(r'display/(?P<path>.*)$',views.display,name="display"),
    url(r'followpic',views.followpic),
    url(r'^comments/$',views.comments),
    url(r'^loadcomments/$',views.loadcomments),
    url(r'^editcomment/$',views.editcomment),
    url(r'^accounts/(?P<path>.*)$',views.accounts),
    url(r'^followpeople/$',views.followpeople),
    url(r'^followingpeople/$',views.peopleufollow),
    url(r'^followingpics/$',views.picsufollow),
    url(r'^explore/$',views.explore),
    url(r'^about/$',views.about),
    )

