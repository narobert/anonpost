from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^bullpost/', include('bullpost.foo.urls')),
    url(r'^logout/', 'blog.views.logout', name='logout'),
    url(r'^login/', 'blog.views.login', name='login'),
    url(r'^register/', 'blog.views.register', name='register'),
    url(r'^myprofile/', 'blog.views.myprofile', name='myprofile'),
    url(r'^post/', 'blog.views.postwall', name='postwall'),
    url(r'^postto/(?P<username>[\w\-]+)/$', 'blog.views.postprofile', name='postprofile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', 'blog.views.profile', name='profile'),
    url(r'^view/(?P<id>[\w\-]+)/$', 'blog.views.click', name='click'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
