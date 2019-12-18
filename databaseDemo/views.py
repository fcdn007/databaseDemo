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


def AdvancedSearchV(request):
    return render(request, 'AdvancedSearch.html')


def SearchProcess(request):
    # print(">>>>>> request >>>>>>>")
    # pprint(request)
    # print(">>>>>> request.POST >>>>>>>")
    # pprint(request.POST)
    modellist = request.POST['modellist'].split(', ')
    queryset = {}
    for i in request.POST['queryset'].split('\n'):
        m, f, v = i.split('\t')
        if f == 'gender':
            v = 1 if v == '男' else 0
        if m in queryset:
            queryset[m][f] = v
        else:
            queryset[m] = {f: v}
    # print(">>>>>> modellist >>>>>>>")
    # pprint(modellist)
    # print(">>>>>> queryset >>>>>>>")
    # pprint(queryset)
    filter_dict = {}
    values_list1 = []
    values_list2 = []
    model_col = {
        'normal': {
            'ClinicalInfo': ['name', 'gender', 'age', 'patientId', 'category', 'stage', 'diagnose',
                             'diagnose_others', 'sampling_date', 'centrifugation_date', 'hospital', 'department',
                             'plasma_num', 'adjacent_mucosa_num', 'cancer_tissue_num', 'WBC_num', 'stool_num',
                             'send_date', 'others'],
            'ExtractInfo': ['ExtractInfo_ClinicalInfo__extract_date', 'ExtractInfo_ClinicalInfo__sample_type',
                            'ExtractInfo_ClinicalInfo__sample_volume', 'ExtractInfo_ClinicalInfo__extract_method',
                            'ExtractInfo_ClinicalInfo__dna_con', 'ExtractInfo_ClinicalInfo__dna_vol',
                            'ExtractInfo_ClinicalInfo__others'],
            'DNAUsageRecordInfo': ['DNAUsageRecordInfo_ClinicalInfo__LB_date', 'DNAUsageRecordInfo_ClinicalInfo__mass',
                                   'DNAUsageRecordInfo_ClinicalInfo__usage',
                                   'DNAUsageRecordInfo_ClinicalInfo__singleLB_id',
                                   'DNAUsageRecordInfo_ClinicalInfo__others'],
            'DNAInventoryInfo': ['DNAInventoryInfo_ClinicalInfo__totalM', 'DNAInventoryInfo_ClinicalInfo__successM',
                                 'DNAInventoryInfo_ClinicalInfo__failM', 'DNAInventoryInfo_ClinicalInfo__researchM',
                                 'DNAInventoryInfo_ClinicalInfo__othersM', 'DNAInventoryInfo_ClinicalInfo__remainM'],
            'LibraryInfo': ['LibraryInfo_ClinicalInfo__singleLB_name', 'LibraryInfo_ClinicalInfo__label',
                            'LibraryInfo_ClinicalInfo__barcodes', 'LibraryInfo_ClinicalInfo__LB_date',
                            'LibraryInfo_ClinicalInfo__LB_method', 'LibraryInfo_ClinicalInfo__mass',
                            'LibraryInfo_ClinicalInfo__pcr_cycles', 'LibraryInfo_ClinicalInfo__LB_con',
                            'LibraryInfo_ClinicalInfo__LB_vol', 'LibraryInfo_ClinicalInfo__operator',
                            'LibraryInfo_ClinicalInfo__others'],
            'CaptureInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id__hybrid_date',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__probes',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__hybrid_hours',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__postpcr_cycles',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__postpcr_con',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__elution_vol',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__others'],
            'PoolingInfo': ['PoolingInfo_ClinicalInfo__pooling_ratio', 'PoolingInfo_ClinicalInfo__mass',
                            'PoolingInfo_ClinicalInfo__volume', 'PoolingInfo_ClinicalInfo__others'],
            'SequencingInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__sequencing_type',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__start_time',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__end_time',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__machine_id',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__chip_id',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__others'],
            'QCInfo': ['QCInfo_ClinicalInfo__QC_id', 'QCInfo_ClinicalInfo__data_size_gb_field',
                       'QCInfo_ClinicalInfo__clean_rate_field', 'QCInfo_ClinicalInfo__r1_q20',
                       'QCInfo_ClinicalInfo__r2_q20', 'QCInfo_ClinicalInfo__r1_q30',
                       'QCInfo_ClinicalInfo__r2_q30', 'QCInfo_ClinicalInfo__gc_content',
                       'QCInfo_ClinicalInfo__bs_conversion_rate_lambda_dna_field',
                       'QCInfo_ClinicalInfo__bs_conversion_rate_chh_field',
                       'QCInfo_ClinicalInfo__bs_conversion_rate_chg_field',
                       'QCInfo_ClinicalInfo__uniquely_paired_mapping_rate',
                       'QCInfo_ClinicalInfo__mismatch_and_indel_rate',
                       'QCInfo_ClinicalInfo__mode_fragment_length_bp_field',
                       'QCInfo_ClinicalInfo__genome_duplication_rate', 'QCInfo_ClinicalInfo__genome_depth_x_field',
                       'QCInfo_ClinicalInfo__genome_dedupped_depth_x_field', 'QCInfo_ClinicalInfo__genome_coverage',
                       'QCInfo_ClinicalInfo__genome_4x_cpg_depth_x_field',
                       'QCInfo_ClinicalInfo__genome_4x_cpg_coverage',
                       'QCInfo_ClinicalInfo__genome_4x_cpg_methylation_level',
                       'QCInfo_ClinicalInfo__panel_4x_cpg_depth_x_field',
                       'QCInfo_ClinicalInfo__panel_4x_cpg_coverage',
                       'QCInfo_ClinicalInfo__panel_4x_cpg_methylation_level',
                       'QCInfo_ClinicalInfo__panel_ontarget_rate_region_field',
                       'QCInfo_ClinicalInfo__panel_duplication_rate_region_field',
                       'QCInfo_ClinicalInfo__panel_depth_site_x_field',
                       'QCInfo_ClinicalInfo__panel_dedupped_depth_site_x_field',
                       'QCInfo_ClinicalInfo__panel_coverage_site_1x_field',
                       'QCInfo_ClinicalInfo__panel_coverage_site_10x_field',
                       'QCInfo_ClinicalInfo__panel_coverage_site_20x_field',
                       'QCInfo_ClinicalInfo__panel_coverage_site_50x_field',
                       'QCInfo_ClinicalInfo__panel_coverage_site_100x_field',
                       'QCInfo_ClinicalInfo__panel_uniformity_site_20_mean_field',
                       'QCInfo_ClinicalInfo__strand_balance_f_field', 'QCInfo_ClinicalInfo__strand_balance_r_field',
                       'QCInfo_ClinicalInfo__gc_bin_depth_ratio', 'QCInfo_ClinicalInfo__others']
        },
        'link': {
            'ClinicalInfo': ['sample_id'],
            'ExtractInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id'],
            'DNAUsageRecordInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id'],
            'DNAInventoryInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id'],
            'LibraryInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id', 'LibraryInfo_ClinicalInfo__singleLB_id'],
            'CaptureInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id__poolingLB_id'],
            'PoolingInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id', 'LibraryInfo_ClinicalInfo__singleLB_id',
                            'PoolingInfo_ClinicalInfo__poolingLB_id', 'PoolingInfo_ClinicalInfo__singleLB_Pooling_id'],
            'SequencingInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__sequencing_id'],
            'QCInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id', 'LibraryInfo_ClinicalInfo__singleLB_id',
                       'PoolingInfo_ClinicalInfo__poolingLB_id', 'PoolingInfo_ClinicalInfo__singleLB_Pooling_id',
                       'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__sequencing_id']
        }
    }
    for model_ in ['ClinicalInfo', 'ExtractInfo', 'DNAUsageRecordInfo', 'DNAInventoryInfo',
                   'LibraryInfo', 'CaptureInfo', 'PoolingInfo', 'SequencingInfo', 'QCInfo']:
        # 记录输出的字段
        if model_ in modellist:
            for item in model_col['link'][model_]:
                if item not in values_list1:
                    values_list1.append(item)
            values_list2 = values_list2 + model_col['normal'][model_]
        # 记录过滤的条件
        if model_ in queryset:
            for field_ in queryset[model_]:
                for item in model_col['link'][model_] + model_col['normal'][model_]:
                    if item.split('__')[-1] == field_:
                        filter_dict[item] = queryset[model_][field_]
                        break
    # 查询数据库
    values_list = values_list1 + values_list2
    raw_data = ClinicalInfo.objects.filter(**filter_dict).values_list(*values_list)
    # print(">>>>>> raw_data >>>>>>>")
    # pprint(raw_data)
    tmp = ClinicalInfo.objects.values_list(*values_list)
    pro_data = []
    for row in raw_data:
        check_l = list(set(row))
        if len(check_l) == 1 and None in check_l:
            continue
        dat = {}
        for col in range(len(row)):
            if col >= len(values_list1):
                value = row[col]
                if values_list[col] == 'gender':
                    value = '男' if row[col] == 1 else '女'
                dat["normal%s" % (col - len(values_list1))] = value
            else:
                dat["link%s" % col] = row[col]
        pro_data.append(dat)
    # print(">>>>>> pro_data >>>>>>>")
    # pprint(pro_data)
    # print(">>>>>> request.GET >>>>>>>")
    # pprint(request.POST)
    result = {
        'draw': 1,
        'recordsTotal': len(tmp),
        'recordsFiltered': len(pro_data),
        'data': pro_data
    }
    return JsonResponse(result)


def uniqueV(request):
    data = {}
    try:
        key1 = KEY1_TO_MODEL[request.GET['model']]
        key2 = request.GET['filed']
        data['values'] = list(set([j for i in key1.objects.values_list(key2) for j in i]))
        data['values'].sort()
        if request.GET['model'] == 'ClinicalInfo' and key2 == 'gender':
            data['values'] = ['男' if x == 1 else '女' for x in data['values']]
    except:
        data['values'] = []
    return JsonResponse(data)

