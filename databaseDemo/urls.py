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
router.register(r'DNAInventoryInfo', views.DNAInventoryInfoViewSet)
router.register(r'LibraryInfo', views.LibraryInfoViewSet)
router.register(r'CaptureInfo', views.CaptureInfoViewSet)
router.register(r'PoolingInfo', views.PoolingInfoViewSet)
router.register(r'SequencingInfo', views.SequencingInfoViewSet)
router.register(r'QCInfo', views.QCInfoViewSet)


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('home/', views.index, name='index'),
                  path('ClinicalInfo/', views.ClinicalInfoV, name='ClinicalInfo'),
                  path('ExtractInfo/', views.ExtractInfoV, name='ExtractInfo'),
                  path('DNAUsage/', views.DNAUsageRecordInfoV, name='DNAUsageRecordInfo'),
                  path('DNAInventoryInfo/', views.DNAInventoryInfoV, name='DNAInventoryInfo'),
                  path('LibraryInfo/', views.LibraryInfoV, name='LibraryInfo'),
                  path('CaptureInfo/', views.CaptureInfoV, name='CaptureInfo'),
                  path('PoolingInfo/', views.PoolingInfoV, name='PoolingInfo'),
                  path('SequencingInfo/', views.SequencingInfoV, name='SequencingInfo'),
                  path('QCInfo/', views.QCInfoV, name='QCInfo'),
                  # for rest_framework
                  path('api/', include(router.urls)),
                  # for rest_framework auth
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
