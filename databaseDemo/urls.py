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
from django.urls import path, include, re_path
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
router.register(r'UserInfo', views.UserInfoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    re_path(r'^(?P<re_model>\w+)Info/$', views.Main_model, name='Main_model'),
    path('Upload/', views.uploadV, name='upload'),
    path('AdvanceSearch/', views.AdvancedSearchV, name='AdvancedSearch'),
    path('Unique/', views.uniqueV, name='unique'),
    path('AdvanceUpload/', views.AdvanceUploadV, name='AdvanceUpload'),
    path('register/', views.RegisterV, name='register'),
    re_path(r'^active/(?P<token>.*)/$', views.ActiveV, name='active'),
    path('users/', include('django.contrib.auth.urls')),
    path('active_resend/', views.Active_resendV, name='active_resend'),
    path('User_info/', views.UserInfoV, name='user_info'),
    # for rest_framework
    path('api/', include(router.urls)),
    # for rest_framework auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # for modul excel downloading
    re_path(r'^download_excel/(?P<model>.*)/$', views.Download_excel, name='Download_excel'),
    re_path(r'^test/(?P<re_model>\w+)Info/$', views.Test_model, name='Test_model'),
    path('plot_data/', views.plotDataV, name='plot_data')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Added at 20170428 开发环境下，如果注释掉，无法正确加载静态文件
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
