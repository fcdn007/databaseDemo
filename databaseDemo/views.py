from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *


def index(request):
    return render(request, 'base.html')
    # return HttpResponse(
    #     "Hello! Welcome to databaseDemo for methylation-sequencing project."
    # )


class ClinicalInfoViewSet(viewsets.ModelViewSet):
    queryset = ClinicalInfo.objects.all()
    # print("queryset.index:")
    # pprint(ClinicalInfo.objects.values_list('index', flat=True).order_by('index'))
    serializer_class = ClinicalInfoSerializer


class ExtractInfoViewSet(viewsets.ModelViewSet):
    queryset = ExtractInfo.objects.all()
    serializer_class = ExtractInfoSerializer


class DNAUsageRecordInfoViewSet(viewsets.ModelViewSet):
    queryset = DNAUsageRecordInfo.objects.all()
    serializer_class = DNAUsageRecordInfoSerializer


class DNAInventoryInfoViewSet(viewsets.ModelViewSet):
    queryset = DNAInventoryInfo.objects.all()
    serializer_class = DNAInventoryInfoSerializer


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


def ClinicalInfoV(request):
    return render(request, 'ClinicalInfo.html')


def DNAInventoryInfoV(request):
    return render(request, 'DNAInventoryInfo.html')


def ExtractInfoV(request):
    return render(request, 'ExtractInfo.html')


def DNAUsageRecordInfoV(request):
    return render(request, 'DNAUsageRecordInfo.html')


def DNAInventoryInfoV(request):
    return render(request, 'DNAInventoryInfo.html')


def LibraryInfoV(request):
    return render(request, 'LibraryInfo.html')


def CaptureInfoV(request):
    return render(request, 'CaptureInfo.html')


def PoolingInfoV(request):
    return render(request, 'PoolingInfo.html')


def SequencingInfoV(request):
    return render(request, 'SequencingInfo.html')


def QCInfoV(request):
    return render(request, 'QCInfo.html')
