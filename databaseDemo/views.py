import re
from pprint import pprint

import pandas as pd
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
            '其他使用量': 'othersM'
        },
        'LibraryInfo': {
            '建库编号': 'singleLB_id',
            '管上编号': 'tube_id',
            '是否临床': 'clinical_boolen',
            '文库名': 'singleLB_name',
            '样本标签': 'label',
            'index列表': 'barcodes',
            '建库日期': 'LB_date',
            '建库方法': 'LB_method',
            '试剂批次': 'kit_batch',
            '起始量': 'mass',
            'PCR循环数': 'pcr_cycles',
            '文库浓度': 'LB_con',
            '文库体积': 'LB_vol',
            '操作人': 'operator',
            '备注': 'others'
        },
        'CaptureInfo': {
            '捕获文库名': 'poolingLB_id',
            '杂交日期': 'hybrid_date',
            '杂交探针': 'probes',
            '杂交时间': 'hybrid_min',
            'PostPCR循环数': 'postpcr_cycles',
            'PostPCR浓度': 'postpcr_con',
            '洗脱体积': 'elution_vol',
            '操作人': 'operator',
            '备注': 'others'
        },
        'PoolingInfo': {
            '测序文库名': 'singleLB_Pooling_id',
            'pooling比例': 'pooling_ratio',
            '取样': 'mass',
            '体积': 'volume',
            '备注': 'others'
        },
        'SequencingInfo': {
            '上机文库号': 'sequencing_id',
            '送测日期': 'send_date',
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
            'DNA提取编号': 'dna_id'
        },
        'DNAInventoryInfo': {
            'DNA提取编号': 'dna_id'
        },
        'LibraryInfo': {
            'DNA提取编号': 'dna_id',
        },
        'PoolingInfo': {
            '建库编号': 'singleLB_id',
            '捕获文库名': 'poolingLB_id'
        },
        'SequencingInfo': {
            '捕获文库名': 'poolingLB_id'
        },
        'QCInfo': {
            '测序文库名': 'singleLB_Pooling_id',
            '上机文库号': 'sequencing_id'
        }
    },
    'foreignAdd': {
        'DNAUsageRecordInfo': {
            '样本编号': [ExtractInfo, 'dna_id', 'DNA提取编号', 'sample_id']
        },
        'DNAInventoryInfo': {
            '样本编号': [ExtractInfo, 'dna_id', 'DNA提取编号', 'sample_id']
        },
        'LibraryInfo': {
            '样本编号': [ExtractInfo, 'dna_id', 'DNA提取编号', 'sample_id']
        },
        'PoolingInfo': {
            '样本编号': [LibraryInfo, 'singleLB_id', '建库编号', 'sample_id'],
            'DNA提取编号': [LibraryInfo, 'singleLB_id', '建库编号', 'dna_id']
        },
        'QCInfo': {
            '样本编号': [PoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'sample_id'],
            'DNA提取编号': [PoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'dna_id'],
            '建库编号': [PoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'singleLB_id'],
            '捕获文库名': [PoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'poolingLB_id']
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


@csrf_exempt
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
            return JsonResponse({
                'done_msg': "Ok.", 'all_records': total, 'add_records': add
            })
        else:
            # print("form.is_valid(): FALSE")
            data = {'error_msg': "只允许上传以下格式文件：txt, csv and xlsx。"}
            return JsonResponse(data)
    return JsonResponse({'error_msg': '只接受POST请求。'})


def na_process(data_, drop_list, str_list, num_list, date_list):
    data = data_.copy(deep=True)
    for col in drop_list:
        for row in range(len(data[col])):
            if pd.isnull(data[col][row]):
                data.drop(row, inplace=True)
    for id in str_list:
        data[id] = ['无' if pd.isnull(x) else x for x in data[id]]
    for id in num_list:
        data[id] = [0 if pd.isnull(x) else x for x in data[id]]
    for id in date_list:
        list_ = []
        for id2 in range(len(data[id])):
            m = re.match(r'^(\d{4})(\d{2})(\d{2})$', str(data[id][id2]))
            if pd.isnull(data[id][id2]):
                list_.append('2000-01-01')
            elif m:
                list_.append("%s-%s-%s" % (m.group(1), m.group(2), m.group(3)))
            else:
                list_.append(data[id][id2])
        data[id] = list_
    return data


def save_records(line):
    # 读取文件，进行数据清洗
    records = read_file(line.uploadUrl, line.uploadFile.path)
    total = records.shape[0]
    cols = records.columns
    addlist = []
    for row in range(records.shape[0]):
        context = {}
        created = False
        if line.uploadUrl in FILECOLUMN_TO_FIELD['normal']:
            # 数据预处理
            for col in cols:
                if col in FILECOLUMN_TO_FIELD['normal'][line.uploadUrl]:
                    context[FILECOLUMN_TO_FIELD['normal'][line.uploadUrl][col]] = records[col][row]
                else:
                    model_key = FILECOLUMN_TO_FIELD['foreign'][line.uploadUrl][col]
                    # 获取foreignKey对应的object
                    print('line.uploadUrl: %s; model_key: %s' % (line.uploadUrl, model_key))
                    if line.uploadUrl == 'SequencingInfo' and model_key == 'poolingLB_id':
                        pass
                    else:
                        obj_ = FOREIGNKEY_TO_MODEL[model_key].objects.get(**{model_key: records[col][row]})
                        context[model_key] = obj_
            if line.uploadUrl in FILECOLUMN_TO_FIELD['foreignAdd']:
                # 对于输入文件中缺少的外键k1，
                # 先找到输入文件中存在的外键k2，
                # 再通过k2对应的model2找到k1对应的值value1
                # 再通过k1对应的model1找到相应对象
                for col in FILECOLUMN_TO_FIELD['foreignAdd'][line.uploadUrl]:
                    l_ = FILECOLUMN_TO_FIELD['foreignAdd'][line.uploadUrl][col]
                    value = model_to_dict(l_[0].objects.get(**{l_[1]: records[l_[2]][row]}))[l_[3]]
                    obj_ = FOREIGNKEY_TO_MODEL[l_[3]].objects.get(**{l_[3]: value})
                    context[l_[3]] = obj_

            # 模型增/改
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
                    inventory.totalM = mass_
                    inventory.save()
                except DNAInventoryInfo.DoesNotExist:  # POST，增
                    context2 = {
                        'sample_id': context['sample_id'], 'dna_id': key_dna_id,
                        'totalM': mass_, 'successM': 0, 'failM': 0,
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
                inventory.save()

            elif line.uploadUrl == 'CaptureInfo':
                _, created = CaptureInfo.objects.update_or_create(
                    poolingLB_id=records[u'捕获文库名'][row], defaults={**context})

            elif line.uploadUrl == 'PoolingInfo':
                _, created = PoolingInfo.objects.update_or_create(
                    singleLB_Pooling_id=records[u'测序文库名'][row], defaults={**context})

            elif line.uploadUrl == 'SequencingInfo':
                captures = []
                print('>>>>>>>>>> notice >>>>>>>')
                pprint(context)
                for c in records[u'捕获文库名'][row]:
                    try:
                        captures.append(CaptureInfo.objects.get(poolingLB_id=c))
                    except CaptureInfo.DoesNotExist:
                        pass
                try:
                    print('>>>>>>>>>> notice >>>>>>> update')
                    sequencing = SequencingInfo.objects.get(sequencing_id=records[u'上机文库号'][row])
                    sequencing.__dict__.update(**context)
                    sequencing.poolingLB_id.add(*captures)
                except SequencingInfo.DoesNotExist:
                    print('>>>>>>>>>> notice >>>>>>> create')
                    created = True
                    sequencing = SequencingInfo(**context)
                    sequencing.save()
                    sequencing.poolingLB_id.add(*captures)

            elif line.uploadUrl == 'QCInfo':
                _, created = QCInfo.objects.update_or_create(
                    QC_id=records[u'Sample'][row], defaults={**context})

            if created:
                addlist.append(row)
        else:
            if line.uploadUrl == 'CaptureInfoPlus':
                for m in ['CaptureInfo', 'PoolingInfo']:
                    # 数据预处理
                    context = {}
                    for col in cols:
                        if col in FILECOLUMN_TO_FIELD['normal'][m]:
                            total = total + 1
                            context[FILECOLUMN_TO_FIELD['normal'][m][col]] = records[col][row]
                        else:
                            if m not in FILECOLUMN_TO_FIELD['foreign'] or col not in FILECOLUMN_TO_FIELD['foreign'][m]:
                                continue
                            model_key = FILECOLUMN_TO_FIELD['foreign'][m][col]
                            # 获取foreignKey对应的object
                            print(">>>>>>>>>>>>>> notice >>>>>>>>>>>")
                            pprint({model_key: records[col][row]})
                            obj_ = FOREIGNKEY_TO_MODEL[model_key].objects.get(**{model_key: records[col][row]})
                            context[model_key] = obj_
                    if m in FILECOLUMN_TO_FIELD['foreignAdd']:
                        for col in FILECOLUMN_TO_FIELD['foreignAdd'][m]:
                            l_ = FILECOLUMN_TO_FIELD['foreignAdd'][m][col]
                            value = model_to_dict(l_[0].objects.get(**{l_[1]: records[l_[2]][row]}))[l_[3]]
                            obj_ = FOREIGNKEY_TO_MODEL[l_[3]].objects.get(**{l_[3]: value})
                            context[l_[3]] = obj_
                    # 模型增/改
                    print(">>>>>>>>>>>>> notice >>>>>>>>>>>")
                    pprint(context)
                    if m == 'CaptureInfo':
                        print(">>>>>>>>>>>>> notice >>>>>>>>>>>", records[u'捕获文库名'][row])
                        _, created = CaptureInfo.objects.update_or_create(
                            poolingLB_id=records[u'捕获文库名'][row], defaults={**context})
                    else:
                        print(">>>>>>>>>>>>> notice >>>>>>>>>>>", records[u'测序文库名'][row])
                        _, created = PoolingInfo.objects.update_or_create(
                            singleLB_Pooling_id=records[u'测序文库名'][row], defaults={**context})

                    if created:
                        addlist.append(row)
    print("total: %s, len(addlist): %s" % (total, len(addlist)))
    return [total, len(addlist)]


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
        data = na_process(data,
                          [u'样本编号'],
                          [u'姓名', u'性别', u'住院号', u'癌种', u'分期', u'诊断', u'诊断备注', u'医院编号',
                           u'科室', u'备注'],
                          [u'年龄', u'血浆管数', u'癌旁组织', u'癌组织', u'白细胞', '粪便'],
                          [u'离心日期', u'寄送日期'])
    elif url == 'ExtractInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['ExtractInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['ExtractInfo'].keys())
        data = df[cols].copy(deep=True)
        data = na_process(data,
                          [u'DNA提取编号', u'样本编号'],
                          [u'样本类型', u'提取方法', u'备注'],
                          [u'样本体积', u'浓度', u'体积'],
                          [u'提取日期'])
    elif url == 'DNAUsageRecordInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['DNAUsageRecordInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['DNAUsageRecordInfo'].keys())
        filter1 = [u'建库失败', u'科研项目', u'其他']
        data = df[df[u'用途'].isin(filter1)][cols].copy(deep=True)
        data = na_process(data,
                          [u'DNA提取编号'],
                          [u'用途', u'建库编号(如有)', u'备注'],
                          [u'使用量'],
                          [u'使用日期'])
    elif url == 'LibraryInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['LibraryInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['LibraryInfo'].keys())
        data = df[cols].copy(deep=True)
        data = na_process(data,
                          [u'DNA提取编号', u'建库编号'],
                          [u'管上编号', u'是否临床', u'文库名', u'样本标签', u'index列表',
                           u'建库方法', u'试剂批次', u'操作人', u'备注'],
                          [u'起始量', u'PCR循环数', u'文库浓度', u'文库体积'],
                          [u'建库日期'])
    elif url == 'CaptureInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['CaptureInfo'].keys())
        data = df[cols].copy(deep=True)
        data = na_process(data,
                          [u'捕获文库名'],
                          [u'杂交探针', u'操作人', u'备注'],
                          [u'杂交时间', u'PostPCR循环数', u'PostPCR浓度', u'洗脱体积'],
                          [u'杂交日期'])
    elif url == 'PoolingInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['PoolingInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['PoolingInfo'].keys())
        data = df[cols].copy(deep=True)
        data = na_process(data,
                          [u'建库编号', u'捕获文库名', u'测序文库名'],
                          [u'备注'],
                          [u'pooling比例', u'取样', u'体积'],
                          [])
    elif url == 'SequencingInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['SequencingInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['SequencingInfo'].keys())
        data = df[cols].copy(deep=True)
        data[u'捕获文库名'] = [x.split(',') for x in data[u'捕获文库名']]
        data = na_process(data,
                          [u'捕获文库名', u'上机文库号'],
                          [u'机器号', u'芯片号', u'备注'],
                          [],
                          [u'送测日期', u'上机时间', u'下机时间'])
    elif url == 'QCInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['QCInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['QCInfo'].keys())
        data = df[cols].copy(deep=True)
        data = na_process(data,
                          [u'测序文库名', u'上机文库号', u'Sample'],
                          [u'备注'],
                          [u'Data_Size(Gb)', u'Clean_Rate(%)', u'R1_Q20', u'R2_Q20', u'R1_Q30', u'R2_Q30',
                           u'GC_Content', u'BS_conversion_rate(lambda_DNA)', u'BS_conversion_rate(CHH)',
                           u'BS_conversion_rate(CHG)', u'Uniquely_Paired_Mapping_Rate', u'Mismatch_and_InDel_Rate',
                           u'Mode_Fragment_Length(bp)', u'Genome_Duplication_Rate', u'Genome_Depth(X)',
                           u'Genome_Dedupped_Depth(X)', u'Genome_Coverage', u'Genome_4X_CpG_Depth(X)',
                           u'Genome_4X_CpG_Coverage', u'Genome_4X_CpG_methylation_level', u'Panel_4X_CpG_Depth(X)',
                           u'Panel_4X_CpG_Coverage', u'Panel_4X_CpG_methylation_level', u'Panel_Ontarget_Rate(region)',
                           u'Panel_Duplication_Rate(region)', u'Panel_Depth(site,X)', u'Panel_Dedupped_Depth(site,X)',
                           u'Panel_Coverage(site,1X)', u'Panel_Coverage(site,10X)', u'Panel_Coverage(site,20X)',
                           u'Panel_Coverage(site,50X)', u'Panel_Coverage(site,100X)',
                           u'Panel_Uniformity(site,>20%mean)', u'Strand_balance(F)', u'Strand_balance(R)',
                           u'GC_bin_depth_ratio'],
                          [])
    elif url == 'CaptureInfoPlus':
        cols = list(set(list(FILECOLUMN_TO_FIELD['normal']['CaptureInfo'].keys()) + \
                        list(FILECOLUMN_TO_FIELD['normal']['PoolingInfo'].keys()) + \
                        list(FILECOLUMN_TO_FIELD['foreign']['PoolingInfo'].keys())))
        data = df[cols].copy(deep=True)
        data = na_process(data,
                          [u'建库编号', u'捕获文库名', u'测序文库名'],
                          [u'杂交探针', u'操作人', u'备注'],
                          [u'杂交时间', u'PostPCR循环数', u'PostPCR浓度', u'洗脱体积', u'pooling比例', u'取样', u'体积'],
                          [u'杂交日期'])
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
    ## 字典，用于构建request查询数据库，值与model的field一致
    model_col = {
        'normal': {
            'ClinicalInfo': ['name', 'gender', 'age', 'patientId', 'category', 'stage', 'diagnose', 'diagnose_others',
                             'centrifugation_date', 'hospital', 'department', 'plasma_num', 'adjacent_mucosa_num',
                             'cancer_tissue_num', 'WBC_num', 'stool_num', 'send_date', 'others'],
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
                                 'DNAInventoryInfo_ClinicalInfo__othersM', 'remainM'],
            'LibraryInfo': ['LibraryInfo_ClinicalInfo__tube_id', 'LibraryInfo_ClinicalInfo__clinical_boolen',
                            'LibraryInfo_ClinicalInfo__singleLB_name', 'LibraryInfo_ClinicalInfo__label',
                            'LibraryInfo_ClinicalInfo__barcodes', 'LibraryInfo_ClinicalInfo__LB_date',
                            'LibraryInfo_ClinicalInfo__LB_method', 'LibraryInfo_ClinicalInfo__kit_batch',
                            'LibraryInfo_ClinicalInfo__con', 'LibraryInfo_ClinicalInfo__mass',
                            'LibraryInfo_ClinicalInfo__pcr_cycles', 'LibraryInfo_ClinicalInfo__LB_con',
                            'LibraryInfo_ClinicalInfo__LB_vol', 'LibraryInfo_ClinicalInfo__operator',
                            'LibraryInfo_ClinicalInfo__others'],
            'CaptureInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id__hybrid_date',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__probes',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__hybrid_min',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__postpcr_cycles',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__postpcr_con',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__elution_vol',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__operator',
                            'PoolingInfo_ClinicalInfo__poolingLB_id__others'],
            'PoolingInfo': ['PoolingInfo_ClinicalInfo__pooling_ratio', 'PoolingInfo_ClinicalInfo__mass',
                            'PoolingInfo_ClinicalInfo__volume', 'PoolingInfo_ClinicalInfo__others'],
            'SequencingInfo': [
                'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__send_date',
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
            'LibraryInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id',
                            'LibraryInfo_ClinicalInfo__singleLB_id'],
            'CaptureInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id__poolingLB_id'],
            'PoolingInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id',
                            'LibraryInfo_ClinicalInfo__singleLB_id',
                            'PoolingInfo_ClinicalInfo__poolingLB_id',
                            'PoolingInfo_ClinicalInfo__singleLB_Pooling_id'],
            'SequencingInfo': ['PoolingInfo_ClinicalInfo__poolingLB_id',
                               'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__sequencing_id'],
            'QCInfo': ['sample_id', 'ExtractInfo_ClinicalInfo__dna_id', 'LibraryInfo_ClinicalInfo__singleLB_id',
                       'PoolingInfo_ClinicalInfo__poolingLB_id', 'PoolingInfo_ClinicalInfo__singleLB_Pooling_id',
                       'PoolingInfo_ClinicalInfo__poolingLB_id__SequencingInfo_CaptureInfo__sequencing_id']
        }
    }
    models_set = ['ClinicalInfo', 'ExtractInfo', 'DNAUsageRecordInfo', 'DNAInventoryInfo', 'LibraryInfo', 'CaptureInfo',
                  'PoolingInfo', 'SequencingInfo', 'QCInfo']
    if request.method == 'POST':
        print(">>>>>> request >>>>>>>")
        pprint(request)
        print(">>>>>> request.POST >>>>>>>")
        pprint(request.POST)
        modellist = request.POST['modellist'].split(', ')
        queryset = []
        nrow = 0
        for i in request.POST['queryset'].split('\n'):
            dict_ = {}
            for j in i.split(' AND '):
                not_, m, f, vp, v = j.split('\t')
                not_ = not_[1:]
                v = v[:-1]
                if vp in ['gt', 'gte', 'lt', 'lte']:
                    v = float(v)
                if m in dict_:
                    if f in dict_[m]:
                        dict_[m][f].append([vp, v, not_])
                    else:
                        dict_[m][f] = [[vp, v, not_]]
                else:
                    dict_[m] = {f: [[vp, v, not_]]}
            queryset.append(dict_)
            nrow = nrow + 1
        print(">>>>>> modellist >>>>>>>")
        pprint(modellist)
        print(">>>>>> queryset >>>>>>>")
        pprint(queryset)

        values_list1 = []
        values_list2 = []
        for model_ in models_set:
            if model_ in modellist:
                for item in model_col['link'][model_]:
                    if item not in values_list1:
                        values_list1.append(item)
                values_list2 = values_list2 + model_col['normal'][model_]
        values_list = values_list1 + values_list2  # 输出到网页的字段
        values_list_filted = values_list  # 数据库输出字段
        if 'remainM' in values_list_filted:  # 去除并未在models.py定义的field
            idx_ = values_list_filted.index('remainM')
            values_list_filted = values_list_filted[0:idx_] + values_list_filted[idx_ + 1:]

        print(">>>>>> values_list1 >>>>>>>")
        pprint(values_list1)
        print(">>>>>> values_list2 >>>>>>>")
        pprint(values_list2)
        print(">>>>>> values_list >>>>>>>")
        pprint(values_list)
        print(">>>>>> values_list_filted >>>>>>>")
        pprint(values_list_filted)
        # raw_data_set存储queryset全部行的原始查询结果
        raw_data_set = []
        for row in range(nrow):
            filter1_dict = {}  # 数据库过滤条件
            filter2_dict = {}  # 进一步过滤条件
            for model_ in models_set:
                # 记录过滤的条件
                if model_ in queryset[row]:
                    for field_ in queryset[row][model_]:
                        for item in model_col['link'][model_] + model_col['normal'][model_]:
                            if item.split('__')[-1] == field_:
                                for list_ in queryset[row][model_][field_]:
                                    filter1_dict_key = "%s__%s" % (item, list_[0])
                                    filter1_dict[filter1_dict_key] = [list_[1], list_[2]]
                                break
            del_keys = []
            for dict_key in filter1_dict:  # 去除并未在models.py定义的field
                if re.match(r'remainM', dict_key):
                    filter2_dict[dict_key] = filter1_dict[dict_key]
                    del_keys.append(dict_key)
            for del_key in del_keys:
                filter1_dict.pop(del_key)
            # 查询数据库
            # 使用Q函数进行复杂查询
            filter1_dict_list = []
            for filter1_dict_key in filter1_dict:
                value, not_ = filter1_dict[filter1_dict_key]
                if not_ == '1':
                    filter1_dict_list.append(~Q(**{filter1_dict_key: value}))
                else:
                    filter1_dict_list.append(Q(**{filter1_dict_key: value}))

            print(">>>>>> filter1_dict >>>>>>>")
            pprint(filter1_dict)
            print(">>>>>> filter1_dict_list >>>>>>>")
            pprint(filter1_dict_list)
            print(">>>>>> filter2_dict >>>>>>>")
            pprint(filter2_dict)
            raw_data_tmp = ClinicalInfo.objects.filter(*filter1_dict_list).values_list(*values_list_filted)
            print(">>>>>> raw_data_tmp >>>>>>>")
            pprint(raw_data_tmp)
            raw_data = []
            if 'remainM' in values_list:
                idx_ = values_list.index('DNAInventoryInfo_ClinicalInfo__othersM')
                print(">>>>>> idx_: %s >>>>>>>" % idx_)
                for row in raw_data_tmp:
                    print(">>>>>> row in raw_data_tmp >>>>>>>")
                    pprint(row)
                    remainM = None
                    values = list(row[0:idx_ + 1]) + [remainM] + list(row[idx_ + 1:])
                    if row[idx_ - 4] is not None:
                        remainM = row[idx_ - 4] - row[idx_ - 3] - row[idx_ - 2] - row[idx_ - 1] - row[idx_]
                        values = list(row[0:idx_ + 1]) + ["%.3f" % remainM] + list(row[idx_ + 1:])
                    if len(filter2_dict) > 0:
                        if remainM is None:
                            continue
                        pass_mark = 1
                        for filter2_dict_key in filter2_dict:
                            vp = filter2_dict_key.split('__')[-1]
                            if vp == 'gt':
                                if not filter2_dict[filter2_dict_key][1] and \
                                        remainM <= filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                                elif filter2_dict[filter2_dict_key][1] and \
                                        remainM > filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                            elif vp == 'gte':
                                if not filter2_dict[filter2_dict_key][1] and \
                                        remainM < filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                                elif filter2_dict[filter2_dict_key][1] and \
                                        remainM >= filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                            elif vp == 'lt':
                                if not filter2_dict[filter2_dict_key][1] and \
                                        remainM >= filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                                elif filter2_dict[filter2_dict_key][1] and \
                                        remainM < filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                            elif vp == 'lte':
                                if not filter2_dict[filter2_dict_key][1] and \
                                        remainM > filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                                elif filter2_dict[filter2_dict_key][1] and \
                                        remainM <= filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                            elif re.search(r'exact', vp):
                                if not filter2_dict[filter2_dict_key][1] and \
                                        remainM == filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                                elif filter2_dict[filter2_dict_key][1] and \
                                        remainM == filter2_dict[filter2_dict_key][0]:
                                    pass_mark = 0
                                    break
                        if pass_mark:
                            raw_data.append(values)
                    else:
                        raw_data.append(values)
            else:
                raw_data = raw_data_tmp

            for raw_data_row in raw_data:
                if raw_data_row not in raw_data_set:
                    raw_data_set.append(raw_data_row)

        print(">>>>>> raw_data >>>>>>>")
        pprint(raw_data)
        pro_data = []
        for row in raw_data_set:
            check_l = list(set(row))
            if len(check_l) == 1 and None in check_l:
                continue
            dat = {}
            for col in range(len(row)):
                if col >= len(values_list1):
                    value = row[col]
                    dat["normal%s" % (col - len(values_list1))] = value
                else:
                    dat["link%s" % col] = row[col]
            pro_data.append(dat)
        print(">>>>>> pro_data >>>>>>>")
        pprint(pro_data)
        # print(">>>>>> request.GET >>>>>>>")
        # pprint(request.POST)
        result = {
            'draw': 1,
            'recordsTotal': len(pro_data),
            'recordsFiltered': len(pro_data),
            'data': pro_data
        }
        return JsonResponse(result)
    else:
        return render(request, 'AdvancedSearch.html')


def uniqueV(request):
    data = {}
    try:
        key1 = KEY1_TO_MODEL[request.GET['model']]
        key2 = request.GET['filed']
        data['values'] = list(set([j for i in key1.objects.values_list(key2) for j in i]))
        data['values'].sort()
    except:
        data['values'] = []
    return JsonResponse(data)


def AdvanceUploadV(request):
    return render(request, 'AdvancedUpload.html')
