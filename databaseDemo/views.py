from pprint import pprint

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from .forms import FileUploadModelForm
from .serializers import *

FILECOLUMN_TO_FIELD = {
    'normal': {
        'ClinicalInfo': {
            '样本编号': 'sample_id',
            '姓名': 'name',
            '性别': 'gender',
            '年龄': 'age',
            '住院号': 'patientId',
            '癌种': 'category',
            '分期': 'stage',
            '诊断': 'diagnose',
            '诊断备注': 'diagnose_others',
            '采样日期': 'sampling_date',
            '离心日期': 'centrifugation_date',
            '医院编号': 'hospital',
            '科室': 'department',
            '血浆管数': 'plasma_num',
            '癌旁组织': 'adjacent_mucosa_num',
            '癌组织': 'cancer_tissue_num',
            '白细胞': 'WBC_num',
            '粪便': 'stool_num',
            '寄送日期': 'send_date',
            '备注': 'others',
        },
        'ExtractInfo': {
            'DNA提取编号': 'dna_id',
            '提取日期': 'extract_date',
            '样本类型': 'sample_type',
            '样本体积': 'sample_volume',
            '提取方法': 'extract_method',
            '浓度': 'dna_con',
            '体积': 'dna_vol',
            '备注': 'others'
        },
        'DNAUsageRecordInfo': {
            '使用日期': 'LB_date',
            '使用量': 'mass',
            '用途': 'usage',
            '建库编号(如有)': 'singleLB_id',
            '备注': 'others'
        },
        'DNAInventoryInfo': {
            'DNA提取总量': 'totalM',
            '成功建库使用量': 'successM',
            '失败建库使用量': 'failM',
            '科研项目使用量': 'researchM',
            '其他使用量': 'othersM',
            '剩余量': 'remainM'
        },
        'LibraryInfo': {
            '建库编号': 'singleLB_id',
            '样本标签': 'label',
            '文库名': 'singleLB_name',
            'index列表': 'barcodes',
            '建库日期': 'LB_date',
            '建库方法': 'LB_method',
            '起始量': 'mass',
            'PCR循环数': 'pcr_cycles',
            '文库浓度': 'LB_con',
            '文库体积': 'LB_vol',
            '操作人': 'operator',
            '备注': 'others'
        },
        'CaptureInfo': {
            'pooling号': 'poolingLB_id',
            '杂交日期': 'hybrid_date',
            '杂交探针': 'probes',
            '杂交时间': 'hybrid_hours',
            'PostPCR循环数': 'postpcr_cycles',
            'PostPCR浓度': 'postpcr_con',
            '洗脱体积': 'elution_vol',
            '备注': 'others'
        },
        'PoolingInfo': {
            '文库编号': 'singleLB_Pooling_id',
            'pooling比例': 'pooling_ratio',
            '取样': 'mass',
            '体积': 'volume',
            '备注': 'others'
        },
        'SequencingInfo': {
            '测序编号': 'sequencing_id',
            '测序类型': 'sequencing_type',
            '上机时间': 'start_time',
            '下机时间': 'end_time',
            '机器号': 'machine_id',
            '芯片号': 'chip_id',
            '备注': 'others'
        },
        'QCInfo': {
            'Sample': 'QC_id',
            'Data_Size(Gb)': 'data_size_gb_field',
            'Clean_Rate(%)': 'clean_rate_field',
            'R1_Q20': 'r1_q20',
            'R2_Q20': 'r2_q20',
            'R1_Q30': 'r1_q30',
            'R2_Q30': 'r2_q30',
            'GC_Content': 'gc_content',
            'BS_conversion_rate(lambda_DNA)': 'bs_conversion_rate_lambda_dna_field',
            'BS_conversion_rate(CHH)': 'bs_conversion_rate_chh_field',
            'BS_conversion_rate(CHG)': 'bs_conversion_rate_chg_field',
            'Uniquely_Paired_Mapping_Rate': 'uniquely_paired_mapping_rate',
            'Mismatch_and_InDel_Rate': 'mismatch_and_indel_rate',
            'Mode_Fragment_Length(bp)': 'mode_fragment_length_bp_field',
            'Genome_Duplication_Rate': 'genome_duplication_rate',
            'Genome_Depth(X)': 'genome_depth_x_field',
            'Genome_Dedupped_Depth(X)': 'genome_dedupped_depth_x_field',
            'Genome_Coverage': 'genome_coverage',
            'Genome_4X_CpG_Depth(X)': 'genome_4x_cpg_depth_x_field',
            'Genome_4X_CpG_Coverage': 'genome_4x_cpg_coverage',
            'Genome_4X_CpG_methylation_level': 'genome_4x_cpg_methylation_level',
            'Panel_4X_CpG_Depth(X)': 'panel_4x_cpg_depth_x_field',
            'Panel_4X_CpG_Coverage': 'panel_4x_cpg_coverage',
            'Panel_4X_CpG_methylation_level': 'panel_4x_cpg_methylation_level',
            'Panel_Ontarget_Rate(region)': 'panel_ontarget_rate_region_field',
            'Panel_Duplication_Rate(region)': 'panel_duplication_rate_region_field',
            'Panel_Depth(site,X)': 'panel_depth_site_x_field',
            'Panel_Dedupped_Depth(site,X)': 'panel_dedupped_depth_site_x_field',
            'Panel_Coverage(site,1X)': 'panel_coverage_site_1x_field',
            'Panel_Coverage(site,10X)': 'panel_coverage_site_10x_field',
            'Panel_Coverage(site,20X)': 'panel_coverage_site_20x_field',
            'Panel_Coverage(site,50X)': 'panel_coverage_site_50x_field',
            'Panel_Coverage(site,100X)': 'panel_coverage_site_100x_field',
            'Panel_Uniformity(site,>20%mean)': 'panel_uniformity_site_20_mean_field',
            'Strand_balance(F)': 'strand_balance_f_field',
            'Strand_balance(R)': 'strand_balance_r_field',
            'GC_bin_depth_ratio': 'gc_bin_depth_ratio',
            '备注': 'others'
        },
        'UploadFile': {
            '上传文件': 'uploadFile',
            '项目': 'uploadUrl',
            '上传者': 'uploadOperator'
        }
    },
    'foreign': {
        'ExtractInfo': {
            '样本编号': 'sample_id'
        },
        'DNAUsageRecordInfo': {
            'DNA提取编号': 'dna_id',
            '样本编号': 'sample_id'
        },
        'DNAInventoryInfo': {
            'DNA提取编号': 'dna_id',
            '样本编号': 'sample_id'
        },
        'LibraryInfo': {
            'DNA提取编号': 'dna_id',
            '样本编号': 'sample_id'
        },
        'PoolingInfo': {
            '样本编号': 'sample_id',
            'DNA提取编号': 'dna_id',
            '建库编号': 'singleLB_id',
            'pooling号': 'poolingLB_id'
        },
        'SequencingInfo': {
            'pooling号': 'poolingLB_id'
        },
        'QCInfo': {
            '样本编号': 'sample_id',
            'DNA提取编号': 'dna_id',
            '建库编号': 'singleLB_id',
            'pooling号': 'poolingLB_id',
            '文库编号': 'singleLB_Pooling_id',
            '测序编号': 'sequencing_id'
        }
    }
}

FOREIGNKEY_TO_MODEL = {
    'sample_id': ClinicalInfo,
    'dna_id': ExtractInfo,
    'singleLB_id': LibraryInfo,
    'poolingLB_id': CaptureInfo,
    'singleLB_Pooling_id': PoolingInfo,
    'sequencing_id': SequencingInfo
}


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


def uploadV(request):
    # pprint(request)
    if request.method == "POST":
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        # print("form: %s" % form)

        if form.is_valid():
            # print("form.is_valid(): TRUE")
            uploadLine = form.save()
            # print('uploadLine.uploadUrl: %s' % uploadLine.uploadUrl)
            # print('uploadLine.uploadOperator: %s' % uploadLine.uploadOperator)
            # print('uploadLine.uploadFile: %s' % uploadLine.uploadFile)
            # print(uploadLine.uploadFile.path)
            # read file and add records to model
            total, add = save_records(uploadLine)
            return JsonResponse([{
                'done_msg': "Ok.", 'all_records': total, 'add_records': add
            }], safe=False)
        else:
            # print("form.is_valid(): FALSE")
            data = {'error_msg': "只允许上传以下格式文件：txt, csv and xlsx。"}
            return JsonResponse(data)
    return JsonResponse({'error_msg': '只接受POST请求。'})


def save_records(line):
    # 读取文件，进行数据清洗
    records = read_file(line.uploadUrl, line.uploadFile.path)
    cols = records.columns
    addlist = []
    for row in range(records.shape[0]):
        context = {}
        for col in cols:
            if col in FILECOLUMN_TO_FIELD['normal'][line.uploadUrl]:
                context[FILECOLUMN_TO_FIELD['normal'][line.uploadUrl][col]] = records[col][row]
            else:
                model_key = FILECOLUMN_TO_FIELD['foreign'][line.uploadUrl][col]
                obj_ = FOREIGNKEY_TO_MODEL[model_key].objects.get(**{model_key: records[col][row]})
                context[model_key] = obj_
        created = False
        if line.uploadUrl == 'ClinicalInfo':
            # 修改临床信息表
            _, created = ClinicalInfo.objects.update_or_create(
                sample_id=records[u'样本编号'][row], defaults={**context})

        elif line.uploadUrl == 'ExtractInfo':
            # 修改提取表
            _, created = ExtractInfo.objects.update_or_create(
                dna_id=records[u'DNA提取编号'][row], defaults={**context})
            # 修改库存表
            mass_ = float(records[u'浓度'][row]) * float(records[u'体积'][row])
            key_dna_id = ExtractInfo.objects.get(dna_id=records[u'DNA提取编号'][row])
            try:  # PUT，改
                inventory = DNAInventoryInfo.objects.get(dna_id=key_dna_id)
                mass_old = inventory.totalM
                inventory.remainM = inventory.remainM + mass_ - mass_old
                inventory.totalM = mass_
                inventory.save()
            except DNAInventoryInfo.DoesNotExist:  # POST，增
                context2 = {
                    'sample_id': context['sample_id'], 'dna_id': key_dna_id,
                    'totalM': mass_, 'remainM': mass_, 'successM': 0, 'failM': 0,
                    'researchM': 0, 'othersM': 0
                }
                inventory = DNAInventoryInfo(**context2)
                inventory.save()

        elif line.uploadUrl == 'DNAUsageRecordInfo':
            # 修改库存表
            inventory = DNAInventoryInfo.objects.get(dna_id=context['dna_id'])
            try:  # PUT，改
                usageRecord = DNAUsageRecordInfo.objects.get(
                    dna_id=context['dna_id'],
                    LB_date=records[u'使用日期'][row],
                    usage=records[u'用途'][row]
                )
                mass_ = float(records[u'使用量'][row]) - usageRecord.mass
            except DNAUsageRecordInfo.DoesNotExist:  # POST，增
                mass_ = float(records[u'使用量'][row])
            inventory.remainM = inventory.remainM - mass_
            if records[u'用途'][row] == '建库失败':
                inventory.failM = inventory.failM + mass_
            elif records[u'用途'][row] == '科研项目':
                inventory.researchM = inventory.researchM + mass_
            elif records[u'用途'][row] == '其他':
                inventory.othersM = inventory.othersM + mass_
            inventory.save()
            # 修改使用记录表
            _, created = DNAUsageRecordInfo.objects.update_or_create(
                dna_id=context['dna_id'],
                LB_date=records[u'使用日期'][row],
                usage=records[u'用途'][row],
                defaults={**context})

        elif line.uploadUrl == 'LibraryInfo':
            _, created = LibraryInfo.objects.update_or_create(
                singleLB_id=records[u'建库编号'][row], defaults={**context})
            # 修改使用记录表
            try:  # PUT，改
                usageRecord = DNAUsageRecordInfo.objects.get(
                    dna_id=context['dna_id'],
                    LB_date=records[u'建库日期'][row],
                    usage='建库成功'
                )
                sub_ = float(records[u'起始量'][row]) - usageRecord.mass
                usageRecord.mass = usageRecord.mass + sub_
                usageRecord.save()
                mass_inventory = sub_
            except DNAUsageRecordInfo.DoesNotExist:  # POST，增
                context2 = {
                    'sample_id': context['sample_id'], 'dna_id': context['dna_id'],
                    'LB_date': records[u'建库日期'][row], 'mass': records[u'起始量'][row],
                    'usage': '建库成功', 'singleLB_id': records[u'建库编号'][row],
                    'others': records[u'备注'][row]
                }
                usageRecord = DNAUsageRecordInfo(**context2)
                usageRecord.save()
                mass_inventory = float(records[u'起始量'][row])
            # 修改库存表
            inventory = DNAInventoryInfo.objects.get(dna_id=context['dna_id'])
            inventory.successM = inventory.successM + mass_inventory
            inventory.remainM = inventory.remainM - mass_inventory
            inventory.save()

        elif line.uploadUrl == 'CaptureInfo':
            _, created = CaptureInfo.objects.update_or_create(
                poolingLB_id=records[u'pooling号'][row], defaults={**context})

        elif line.uploadUrl == 'PoolingInfo':
            _, created = PoolingInfo.objects.update_or_create(
                singleLB_Pooling_id=records[u'文库编号'][row], defaults={**context})

        elif line.uploadUrl == 'SequencingInfo':
            _, created = SequencingInfo.objects.update_or_create(
                sequencing_id=records[u'测序编号'][row], defaults={**context})

        elif line.uploadUrl == 'QCInfo':
            _, created = QCInfo.objects.update_or_create(
                QC_id=records[u'Sample'][row], defaults={**context})

        if created:
            addlist.append(row)
    return [records.shape[0], len(addlist)]


def read_file(url, inf):
    # 读取文件，按文件类型调用不同函数打开
    df = []
    ext = inf.split('.')[-1].lower()
    if ext == "txt":
        df = pd.read_table(inf, sep="\t", header=0, encoding='utf-8')
    elif ext == "csv":
        df = pd.read_csv(inf, header=0, encoding='utf-8')
    elif ext == "xlsx":
        df = pd.read_excel(inf, header=0, encoding='utf-8')
    # 根据url，进行数据清洗
    data = []
    if url == 'ClinicalInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['ClinicalInfo'].keys())
        data = df[cols].copy(deep=True)
        data[u'性别'] = [1 if x == '男' else 0 for x in df[u'性别']]
        for id in [u'备注', u'诊断']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
    elif url == 'ExtractInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['ExtractInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['ExtractInfo'].keys())
        data = df[cols].copy(deep=True)
        for id in [u'备注']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
        for id in [u'样本体积']:
            data[id] = [0 if pd.isnull(x) else x for x in df[id]]
    elif url == 'DNAUsageRecordInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['DNAUsageRecordInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['DNAUsageRecordInfo'].keys())
        filter1 = [u'建库失败', u'科研项目', u'其他']
        data = df[df[u'用途'].isin(filter1)][cols].copy(deep=True)
        for id in [u'备注', u'建库编号(如有)']:
            data[id] = ['无' if pd.isnull(x) else x for x in data[id]]
    elif url == 'LibraryInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['LibraryInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['LibraryInfo'].keys())
        data = df[cols].copy(deep=True)
        for id in [u'备注']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
    elif url == 'CaptureInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['CaptureInfo'].keys())
        data = df[cols].copy(deep=True)
        for id in [u'备注']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
    elif url == 'PoolingInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['PoolingInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['PoolingInfo'].keys())
        data = df[cols].copy(deep=True)
        for id in [u'备注']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
    elif url == 'SequencingInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['SequencingInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['SequencingInfo'].keys())
        data = df[cols].copy(deep=True)
        for id in [u'备注']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
    elif url == 'QCInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['QCInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['QCInfo'].keys())
        data = df[cols].copy(deep=True)
        for id in [u'备注']:
            data[id] = ['无' if pd.isnull(x) else x for x in df[id]]
    # print("return data:\n>>>>>>>")
    # pprint(data)
    # print("<<<<<<<<<")
    return data


def AdvancedSearchV(request):
    return render(request, 'AdvancedSearch.html')


def SearchProcess(request):
    pprint(request)
    pprint(request.GET)
    modellist = request.GET['modellist'].split(', ')
    queryset = {}
    for i in request.GET['queryset'].split('\n'):
        m, f, v = i.split('\t')
        if m in queryset:
            queryset[m][f] = v
        else:
            queryset[m] = {f: v}

    pprint(modellist)
    pprint(queryset)


def uniqueV(request):
    KEY1_TO_MODEL = {
        'ClinicalInfo': ClinicalInfo,
        'ExtractInfo': ExtractInfo,
        'DNAUsageRecordInfo': DNAUsageRecordInfo,
        'DNAInventoryInfo': DNAInventoryInfo,
        'LibraryInfo': LibraryInfo,
        'CaptureInfo': CaptureInfo,
        'PoolingInfo': PoolingInfo,
        'SequencingInfo': SequencingInfo,
        'QCInfo': QCInfo
    }
    data = {}
    try:
        key1 = KEY1_TO_MODEL[request.GET['model']]
        key2 = request.GET['filed']
        pprint([key1, key2])
        data['values'] = list(set([j for i in key1.objects.values_list(key2) for j in i]))
        if request.GET['model'] == 'ClinicalInfo' and key2 == 'gender':
            data['values'] = ['男' if x == 1 else '女' for x in data['values']]
    except:
        data['values'] = []
    return JsonResponse(data)
