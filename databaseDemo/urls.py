"""databaseDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'ClinicalInfo', views.ClinicalInfoViewSet)
router.register(r'ExtractInfo', views.ExtractInfoViewSet)
router.register(r'DNAUsageRecordInfo', views.DNAUsageRecordInfoViewSet)
router.register(r'LibraryInfo', views.LibraryInfoViewSet)
router.register(r'CaptureInfo', views.CaptureInfoViewSet)
router.register(r'PoolingInfo', views.PoolingInfoViewSet)
router.register(r'SequencingInfo', views.SequencingInfoViewSet)
router.register(r'QCInfo', views.QCInfoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
                  path('home/', views.index, name='index'),
                  path('ClinicalInfo/', views.ClinicalInfo, name='ClinicalInfo'),
                  path('DNAInventoryInfo/', views.DNAInventoryInfo, name='DNAInventoryInfo'),
                  path('ExtractInfo/', views.ExtractInfo, name='ExtractInfo'),
                  path('DNAUsage/', views.DNAUsageRecordInfo, name='DNAUsageRecordInfo'),
                  path('LibraryInfo/', views.LibraryInfo, name='LibraryInfo'),
                  path('CaptureInfo/', views.CaptureInfo, name='CaptureInfo'),
                  path('PoolingInfo/', views.PoolingInfo, name='PoolingInfo'),
                  path('SequencingInfo/', views.SequencingInfo, name='SequencingInfo'),
                  path('QCInfo/', views.QCInfo, name='QCInfo'),
                  # for rest_framework
                  path('api/', include(router.urls)),
                  # for rest_framework auth
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
