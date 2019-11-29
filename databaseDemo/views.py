from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *


def index(request):
    return render(request, 'base.html')
    # return HttpResponse(
    #     "Hello! Welcome to databaseDemo for methylation-sequencing project."
    # )


class ClinicalInfoViewSet(viewsets.ModelViewSet):
    queryset = ClinicalInfo.objects.all()
    serializer_class = ClinicalInfoSerializer


class ExtractInfoViewSet(viewsets.ModelViewSet):
    queryset = ExtractInfo.objects.all()
    serializer_class = ExtractInfoSerializer


class DNAUsageRecordInfoViewSet(viewsets.ModelViewSet):
    queryset = DNAUsageRecordInfo.objects.all()
    serializer_class = DNAUsageRecordInfoSerializer


class LibraryInfoViewSet(viewsets.ModelViewSet):
    queryset = LibraryInfo.objects.all()
    serializer_class = LibraryInfoSerializer


class CaptureInfoViewSet(viewsets.ModelViewSet):
    queryset = CaptureInfo.objects.all()
    serializer_class = CaptureInfoSerializer


class PoolingInfoViewSet(viewsets.ModelViewSet):
    queryset = PoolingInfo.objects.all()
    serializer_class = PoolingInfoSerializer


class SequencingInfoViewSet(viewsets.ModelViewSet):
    queryset = SequencingInfo.objects.all()
    serializer_class = SequencingInfoSerializer


class QCInfoViewSet(viewsets.ModelViewSet):
    queryset = QCInfo.objects.all()
    serializer_class = QCInfoSerializer


def ClinicalInfo(request):
    return render(request, 'ClinicalInfo.html')


def DNAInventoryInfo(request):
    return render(request, 'DNAInventoryInfo.html')


def ExtractInfo(request):
    return render(request, 'ExtractInfo.html')


def DNAUsageRecordInfo(request):
    return render(request, 'DNAUsageRecordInfo.html')


def LibraryInfo(request):
    return render(request, 'LibraryInfo.html')


def CaptureInfo(request):
    return render(request, 'CaptureInfo.html')


def PoolingInfo(request):
    return render(request, 'PoolingInfo.html')


def SequencingInfo(request):
    return render(request, 'SequencingInfo.html')


def QCInfo(request):
    return render(request, 'QCInfo.html')
