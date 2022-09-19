"""cerebroDigital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from notasPensamiento import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('.*/(.*.css)$', serve),
    # path('.*/(.*.js)$', serve),
    path('bibliografia', views.bibliografia),
    path('nuevos_items', views.nuevos_items),
    path('procesar_txt', views.procesar_txt),
    path('editar_extracto/<int:id>', views.editar_extracto),
    path('eliminar_referencia/<int:id>', views.eliminar_referencia),
    path('eliminar_extracto/<int:id>', views.eliminar_extracto),
    path('nuevo_biblio', views.nuevo_biblio),
    path('procesar_nuevo_biblio', views.procesar_biblio),
    path('', views.bibliografia),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
