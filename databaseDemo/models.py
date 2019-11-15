from django.db import models


## 表0 临床信息表
class ClinicalInfo(models.Model):
    sample_id = models.CharField(db_column='样本编号', unique=True, max_length=255)
    name = models.CharField(db_column='姓名', max_length=255)
    gender = models.IntegerField(db_column='性别', blank=True, null=True)
    age = models.IntegerField(db_column='年龄')
    hospital = models.CharField(db_column='住院号', max_length=255)
    diagnose = models.TextField(db_column='诊断', blank=True, null=True)
    others = models.CharField(db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '临床信息表'


# 表1 医院送样表
class HospitalInfo(models.Model):
    sample_id = models.ForeignKey("ClinicalInfo", on_delete=models.CASCADE, related_name='HospitalInfo_ClinicalInfo',
                                  to_field="sample_id", db_column='全血编号', blank=True, null=True)
    sampling_date = models.DateField(db_column='采样日期')
    centrifugation_date = models.DateField(db_column='离心日期')
    hospital = models.CharField(db_column='医院编号', max_length=255)
    department = models.CharField(db_column='科室', max_length=255)
    plasma_num = models.IntegerField(db_column='血浆管数')
    adjacent_mucosa_num = models.IntegerField(db_column='癌旁组织')
    cancer_tissue_num = models.IntegerField(db_column='癌组织')
    WBC_num = models.IntegerField(db_column='白细胞')
    stool_num = models.IntegerField(db_column='粪便')
    send_date = models.DateField(db_column='寄送日期')
    others = models.CharField(db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '医院送样表'


# 表2 样本提取表
class ExtractInfo(models.Model):
    dna_id = models.CharField(db_column='DNA提取编号', unique=True, max_length=255)
    sample_id = models.ForeignKey("ClinicalInfo", on_delete=models.CASCADE, related_name='ExtractInfo_ClinicalInfo',
                                  to_field="sample_id", db_column='虚拟入库号', blank=True, null=True)
    extract_date = models.DateField(db_column='提取日期')
    sample_type = models.CharField(db_column='样本类型', max_length=255)
    sample_volume = models.FloatField(db_column='样本体积', blank=True, null=True)
    extract_method = models.CharField(db_column='提取方法', max_length=255)
    dna_con = models.FloatField(db_column='浓度')
    dna_vol = models.FloatField(db_column='体积')
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '样本提取表'


# 表3 样本DNA使用记录表
class DNAUsageRecordInfo(models.Model):
    dna_id = models.ForeignKey("ExtractInfo", on_delete=models.CASCADE, related_name='DNAUsageRecordInfo_ExtractInfo',
                               to_field="dna_id", db_column='DNA提取编号', blank=True, null=True)
    sample_id = models.ForeignKey("ClinicalInfo", on_delete=models.CASCADE,
                                  related_name='DNAUsageRecordInfo_ClinicalInfo',
                                  to_field="sample_id", db_column='虚拟入库号', blank=True, null=True)
    usage_time = models.DateTimeField(db_column='使用时间')
    mass = models.FloatField(db_column='使用量')
    usage = models.CharField(db_column='用途', max_length=255)
    others = models.CharField(db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '样本DNA使用记录表'


# 表4 甲基化建库表
class LibraryInfo(models.Model):
    singleLB_id = models.CharField(db_column='单个文库编号', unique=True, max_length=255)
    sample_id = models.ForeignKey("ClinicalInfo", on_delete=models.CASCADE, related_name='DLibraryInfo_ClinicalInfo',
                                  to_field="sample_id", db_column='样本编号', blank=True, null=True)
    dna_id = models.ForeignKey("ExtractInfo", on_delete=models.CASCADE, related_name='DLibraryInfo_ExtractInfo',
                               to_field="dna_id", db_column='DNA提取编号', blank=True, null=True)
    singleLB_name = models.CharField(db_column='文库名', max_length=255)
    label = models.CharField(db_column='样本标签', max_length=255)
    barcodes = models.CharField(db_column='index列表', max_length=255)
    LB_date = models.DateField(db_column='建库日期')
    LB_method = models.CharField(db_column='建库方法', max_length=255)
    mass = models.FloatField(db_column='起始量')
    pcr_cycles = models.IntegerField(db_column='PCR循环数')  # Field name made lowercase.
    LB_con = models.FloatField(db_column='文库浓度')
    LB_vol = models.FloatField(db_column='文库体积')
    operator = models.CharField(db_column='操作人', max_length=255)
    others = models.CharField(db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '甲基化建库表'


# 表5 甲基化捕获文库信息表
class CaptureInfo(models.Model):
    poolingLB_id = models.CharField(db_column='捕获pooling文库编号', unique=True, max_length=255)
    hybrid_date = models.DateField(db_column='杂交日期')
    probes = models.CharField(db_column='杂交探针', max_length=255)
    hybrid_hours = models.FloatField(db_column='杂交时间')
    postpcr_cycles = models.IntegerField(db_column='PostPCR循环数')  # Field name made lowercase.
    postpcr_con = models.FloatField(db_column='PostPCR浓度')  # Field name made lowercase.
    elution_vol = models.FloatField(db_column='洗脱体积')
    pooling_id = models.CharField(db_column='Pooling号', max_length=255)  # Field name made lowercase.
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '甲基化捕获文库信息表'


# 表6 pooling表
class PoolingInfo(models.Model):
    sample_id = models.ForeignKey("ClinicalInfo", on_delete=models.CASCADE, related_name='PoolingInfo_ClinicalInfo',
                                  to_field="sample_id", db_column='样本编号', blank=True, null=True)
    dna_id = models.ForeignKey("ExtractInfo", on_delete=models.CASCADE, related_name='PoolingInfo_ExtractInfo',
                               to_field="dna_id", db_column='DNA提取编号', blank=True, null=True)
    singleLB_id = models.ForeignKey("LibraryInfo", on_delete=models.CASCADE, related_name='PoolingInfo_LibraryInfo',
                                    to_field="singleLB_id", db_column='单文库编号', blank=True, null=True)
    poolingLB_id = models.ForeignKey("CaptureInfo", on_delete=models.CASCADE, related_name='PoolingInfo_CaptureInfo',
                                     to_field="poolingLB_id", db_column='pooling文库编号', blank=True, null=True)
    pooling_ratio = models.FloatField(db_column='pooling比例')
    mass = models.FloatField(db_column='取样')
    volume = models.FloatField(db_column='体积')
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'pooling表'


# 表7 测序登记表
class SequencingInfo(models.Model):
    sequencing_id = models.CharField(db_column='测序编号', unique=True, max_length=255)
    poolingLB_id = models.ForeignKey("CaptureInfo", on_delete=models.CASCADE, related_name='SequencingInfo_CaptureInfo',
                                     to_field="poolingLB_id", db_column='捕获pooling文库编号', blank=True, null=True)
    sequencing_type = models.CharField(db_column='测序类型', max_length=255)
    start_time = models.DateTimeField(db_column='上机时间')
    end_time = models.DateTimeField(db_column='下机时间')
    machine_id = models.CharField(db_column='机器号', max_length=255)
    chip_id = models.CharField(db_column='芯片号', max_length=255)
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '测序登记表'


# 表8 样本测序质控表
class QCInfo(models.Model):
    singleLB_id = models.ForeignKey("LibraryInfo", on_delete=models.CASCADE, related_name='QCInfo_LibraryInfo',
                                    to_field="singleLB_id", db_column='Sample', blank=True, null=True)
    data_size_gb_field = models.FloatField(
        db_column='Data_Size(Gb)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    clean_rate_field = models.FloatField(
        db_column='Clean_Rate(%)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    r1_q20 = models.FloatField(db_column='R1_Q20')  # Field name made lowercase.
    r2_q20 = models.FloatField(db_column='R2_Q20')  # Field name made lowercase.
    r1_q30 = models.FloatField(db_column='R1_Q30')  # Field name made lowercase.
    r2_q30 = models.FloatField(db_column='R2_Q30')  # Field name made lowercase.
    gc_content = models.FloatField(db_column='GC_Content')  # Field name made lowercase.
    bs_conversion_rate_lambda_dna_field = models.FloatField(
        db_column='BS_conversion_rate(lambda_DNA)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    bs_conversion_rate_chh_field = models.FloatField(
        db_column='BS_conversion_rate(CHH)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    bs_conversion_rate_chg_field = models.FloatField(
        db_column='BS_conversion_rate(CHG)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    uniquely_paired_mapping_rate = models.FloatField(
        db_column='Uniquely_Paired_Mapping_Rate')  # Field name made lowercase.
    mismatch_and_indel_rate = models.FloatField(db_column='Mismatch_and_InDel_Rate')  # Field name made lowercase.
    mode_fragment_length_bp_field = models.FloatField(
        db_column='Mode_Fragment_Length(bp)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    genome_duplication_rate = models.FloatField(db_column='Genome_Duplication_Rate')  # Field name made lowercase.
    genome_depth_x_field = models.FloatField(
        db_column='Genome_Depth(X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    genome_dedupped_depth_x_field = models.FloatField(
        db_column='Genome_Dedupped_Depth(X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    genome_coverage = models.FloatField(db_column='Genome_Coverage')  # Field name made lowercase.
    genome_4x_cpg_depth_x_field = models.FloatField(
        db_column='Genome_4X_CpG_Depth(X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    genome_4x_cpg_coverage = models.FloatField(db_column='Genome_4X_CpG_Coverage')  # Field name made lowercase.
    genome_4x_cpg_methylation_level = models.FloatField(db_column='Genome_4X_CpG_methylation_level', blank=True,
                                                        null=True)  # Field name made lowercase.
    panel_4x_cpg_depth_x_field = models.FloatField(db_column='Panel_4X_CpG_Depth(X)', blank=True,
                                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_4x_cpg_coverage = models.FloatField(db_column='Panel_4X_CpG_Coverage', blank=True,
                                              null=True)  # Field name made lowercase.
    panel_4x_cpg_methylation_level = models.FloatField(db_column='Panel_4X_CpG_methylation_level', blank=True,
                                                       null=True)  # Field name made lowercase.
    panel_ontarget_rate_region_field = models.FloatField(
        db_column='Panel_Ontarget_Rate(region)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_duplication_rate_region_field = models.FloatField(
        db_column='Panel_Duplication_Rate(region)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_depth_site_x_field = models.FloatField(
        db_column='Panel_Depth(site,X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_dedupped_depth_site_x_field = models.FloatField(
        db_column='Panel_Dedupped_Depth(site,X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_coverage_site_1x_field = models.FloatField(
        db_column='Panel_Coverage(site,1X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_coverage_site_10x_field = models.FloatField(
        db_column='Panel_Coverage(site,10X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_coverage_site_20x_field = models.FloatField(
        db_column='Panel_Coverage(site,20X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_coverage_site_50x_field = models.FloatField(
        db_column='Panel_Coverage(site,50X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_coverage_site_100x_field = models.FloatField(
        db_column='Panel_Coverage(site,100X)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    panel_uniformity_site_20_mean_field = models.FloatField(
        db_column='Panel_Uniformity(site,>20%mean)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    strand_balance_f_field = models.FloatField(db_column='Strand_balance(F)', blank=True,
                                               null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    strand_balance_r_field = models.FloatField(
        db_column='Strand_balance(R)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    gc_bin_depth_ratio = models.FloatField(db_column='GC_bin_depth_ratio')  # Field name made lowercase.
    sample_id = models.ForeignKey("ClinicalInfo", on_delete=models.CASCADE, related_name='QCInfo_ClinicalInfo',
                                  to_field="sample_id", db_column='样本编号', blank=True, null=True)
    dna_id = models.ForeignKey("ExtractInfo", on_delete=models.CASCADE, related_name='QCInfo_ExtractInfo',
                               to_field="dna_id", db_column='DNA提取编号', blank=True, null=True)
    poolingLB_id = models.ForeignKey("CaptureInfo", on_delete=models.CASCADE, related_name='QCInfo_CaptureInfo',
                                     to_field="poolingLB_id", db_column='pooling文库编号', blank=True, null=True)
    sequencing_id = models.ForeignKey("SequencingInfo", on_delete=models.CASCADE, related_name='QCInfo_SequencingInfo',
                                      to_field="sequencing_id", db_column='测序编号', blank=True, null=True)
    index = models.AutoField(primary_key=True)

    class Meta:
        db_table = '样本测序质控表'
