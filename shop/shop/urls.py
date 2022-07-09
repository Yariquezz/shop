
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('carts/', include('apps.carts.urls', namespace='carts')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('about/', include('apps.about.urls', namespace='about')),
    path('', include('apps.products.urls', namespace='products')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.accounts.views.handler404'
