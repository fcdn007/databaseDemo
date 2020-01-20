import datetime
import re

import numpy as np
import pandas as pd
from django.forms.models import model_to_dict

from .models import *

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
                    # print('line.uploadUrl: %s; model_key: %s' % (line.uploadUrl, model_key))
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
                # print('>>>>>>>>>> notice >>>>>>>')
                # pprint(context)
                for c in records[u'捕获文库名'][row]:
                    try:
                        captures.append(CaptureInfo.objects.get(poolingLB_id=c))
                    except CaptureInfo.DoesNotExist:
                        pass
                try:
                    # print('>>>>>>>>>> notice >>>>>>> update')
                    sequencing = SequencingInfo.objects.get(sequencing_id=records[u'上机文库号'][row])
                    sequencing.__dict__.update(**context)
                    sequencing.poolingLB_id.add(*captures)
                except SequencingInfo.DoesNotExist:
                    # print('>>>>>>>>>> notice >>>>>>> create')
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
                            # print(">>>>>>>>>>>>>> notice >>>>>>>>>>>")
                            # pprint({model_key: records[col][row]})
                            obj_ = FOREIGNKEY_TO_MODEL[model_key].objects.get(**{model_key: records[col][row]})
                            context[model_key] = obj_
                    if m in FILECOLUMN_TO_FIELD['foreignAdd']:
                        for col in FILECOLUMN_TO_FIELD['foreignAdd'][m]:
                            l_ = FILECOLUMN_TO_FIELD['foreignAdd'][m][col]
                            value = model_to_dict(l_[0].objects.get(**{l_[1]: records[l_[2]][row]}))[l_[3]]
                            obj_ = FOREIGNKEY_TO_MODEL[l_[3]].objects.get(**{l_[3]: value})
                            context[l_[3]] = obj_
                    # 模型增/改
                    # print(">>>>>>>>>>>>> notice >>>>>>>>>>>")
                    # pprint(context)
                    if m == 'CaptureInfo':
                        # print(">>>>>>>>>>>>> notice >>>>>>>>>>>", records[u'捕获文库名'][row])
                        _, created = CaptureInfo.objects.update_or_create(
                            poolingLB_id=records[u'捕获文库名'][row], defaults={**context})
                    else:
                        # print(">>>>>>>>>>>>> notice >>>>>>>>>>>", records[u'测序文库名'][row])
                        _, created = PoolingInfo.objects.update_or_create(
                            singleLB_Pooling_id=records[u'测序文库名'][row], defaults={**context})

                    if created:
                        addlist.append(row)
    # print("total: %s, len(addlist): %s" % (total, len(addlist)))
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


def list2array(l, names):
    array = []
    for i in l:
        array.append(list(i))
    return pd.DataFrame(array, columns=names)


def filter_conditionFunc(df, f, vp, v, not_):
    filter = [True] * len(df)
    if isinstance(df[f][0], str):
        if vp == 'exact':
            filter = df[f] == v
        elif vp == 'iexact':
            filter = [True if re.match(v, str(i), flags=re.IGNORECASE) else False for i in list(df[f])]
        elif vp == 'contains':
            filter = [True if re.search(v, str(i)) else False for i in list(df[f])]
        elif vp == 'icontains':
            filter = [True if re.search(v, str(i), flags=re.IGNORECASE) else False for i in list(df[f])]
        else:
            filter = [True] * len(df)
    elif isinstance(df[f][0], datetime.date):
        d = datetime.date(1000, 1, 1)
        m1 = re.search(r'(\d{4}).(\d{1,2}).(\d{1,2})', v)
        m2 = re.search(r'(\d{1,2}).(\d{1,2}).(\d{4})', v)
        if re.match(r'\d{8}', v):
            d = datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        elif m1:
            d = datetime.date(int(m1.group(1)), int(m1.group(2)), int(m1.group(3)))
        elif m2:
            d = datetime.date(int(m2.group(3)), int(m2.group(2)), int(m2.group(1)))
        if vp == 'gt':
            filter = df[f] > d
        elif vp == 'gte':
            filter = df[f] >= d
        elif vp == 'lt':
            filter = df[f] < d
        elif vp == 'lte':
            filter = df[f] <= d
        elif vp == 'exact':
            filter = df[f] == d
        else:
            filter = [True] * len(df)
    elif isinstance(df[f][0], np.floating) or isinstance(df[f][0], np.integer):
        v = float(v)
        if vp == 'gt':
            filter = df[f] > v
        elif vp == 'gte':
            filter = df[f] >= v
        elif vp == 'lt':
            filter = df[f] < v
        elif vp == 'lte':
            filter = df[f] <= v
        elif vp == 'exact':
            filter = df[f] == v
        else:
            filter = [True] * len(df)
    else:
        pass
    if not_ == 1:
        filter = [False if x else True for x in filter]
    # print(">>>>>>>>>>>>> filter >>>>>>>>>>>")
    # pprint(filter)
    return pd.Series(data=filter)
