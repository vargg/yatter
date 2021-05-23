from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    path(
        'auth/',
        include(
            'users.urls',
            namespace='users',
        ),
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls'),
    ),
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        '',
        include(
            'posts.urls',
            namespace='posts',
        ),
    ),
    path(
        'api/',
        include('api.urls')
    ),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'about/',
        include(
            'about.urls',
            namespace='about',
        ),
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += (
        path(
            "__debug__/",
            include(
                debug_toolbar.urls
            )
        ),
    )
