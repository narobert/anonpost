from django.conf.urls import patterns, include, url

urlpatterns = patterns(

    'blog.views',

    (r'getCommentsW$', 'getCommentsW'),
    (r'getCommentsP$', 'getCommentsP'),
    (r'getLikesW$', 'getLikesW'),
    (r'getLikesP$', 'getLikesP'),

)
