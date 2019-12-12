import os
import uuid

from django.db import models


# 表1 临床信息表
class ClinicalInfo(models.Model):
    sample_id = models.CharField(
        db_column='样本编号', unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(
        db_column='姓名', max_length=255, blank=True, null=True)
    gender = models.IntegerField(
        db_column='性别', blank=True, null=True, default=1)
    age = models.IntegerField(db_column='年龄', blank=True, null=True)
    patientId = models.CharField(
        db_column='住院号', max_length=255, blank=True, null=True)
    diagnose = models.TextField(db_column='诊断', blank=True, null=True)
    sampling_date = models.DateField(db_column='采样日期', blank=True, null=True)
    centrifugation_date = models.DateField(
        db_column='离心日期', blank=True, null=True)
    hospital = models.CharField(
        db_column='医院编号', max_length=255, blank=True, null=True)
    department = models.CharField(
        db_column='科室', max_length=255, blank=True, null=True)
    plasma_num = models.PositiveIntegerField(db_column='血浆管数', default=0)
    adjacent_mucosa_num = models.PositiveIntegerField(
        db_column='癌旁组织', default=0)
    cancer_tissue_num = models.PositiveIntegerField(db_column='癌组织', default=0)
    WBC_num = models.PositiveIntegerField(db_column='白细胞', default=0)
    stool_num = models.PositiveIntegerField(db_column='粪便', default=0)
    send_date = models.DateField(db_column='寄送日期', blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sample_id

    class Meta:
        db_table = '临床信息表'
        verbose_name = '临床信息表'
        ordering = ['index']


# 表2 样本提取表
class ExtractInfo(models.Model):
    dna_id = models.CharField(db_column='DNA提取编号', unique=True, max_length=255)
    sample_id = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='ExtractInfo_ClinicalInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    extract_date = models.DateField(db_column='提取日期', blank=True, null=True)
    sample_type = models.CharField(db_column='样本类型', max_length=255)
    sample_volume = models.FloatField(db_column='样本体积', blank=True, null=True)
    extract_method = models.CharField(
        db_column='提取方法', max_length=255, blank=True, null=True)
    dna_con = models.FloatField(db_column='浓度', blank=True, null=True)
    dna_vol = models.FloatField(db_column='体积', blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dna_id

    class Meta:
        db_table = '样本提取表'
        verbose_name = '样本提取表'
        ordering = ['index']


# 表3 样本DNA使用记录表
class DNAUsageRecordInfo(models.Model):
    dna_id = models.ForeignKey(
        "ExtractInfo",
        on_delete=models.CASCADE,
        related_name='DNAUsageRecordInfo_ExtractInfo',
        to_field="dna_id",
        db_column='DNA提取编号',
        blank=True,
        null=True)
    sample_id = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='DNAUsageRecordInfo_ClinicalInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    LB_date = models.DateField(db_column='使用日期', blank=True, null=True)
    mass = models.FloatField(db_column='使用量', blank=True, null=True)
    usage = models.CharField(db_column='用途', max_length=255)
    singleLB_id = models.CharField(
        db_column='建库编号', max_length=255, blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ":".join([str(self.dna_id), str(self.index)])

    class Meta:
        db_table = '样本DNA使用记录表'
        verbose_name = '样本DNA使用记录表'
        ordering = ['index']


# 表9 样本DNA库存信息表
class DNAInventoryInfo(models.Model):
    sample_id = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='DNAInventoryInfo_ClinicalInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)

    dna_id = models.ForeignKey(
        "ExtractInfo",
        on_delete=models.CASCADE,
        related_name='DNAInventoryInfo_ExtractInfo',
        to_field="dna_id",
        db_column='DNA提取编号',
        blank=True,
        null=True)
    totalM = models.FloatField(db_column='DNA提取总量', blank=True, null=True)
    successM = models.FloatField(db_column='成功建库使用量', blank=True, null=True)
    failM = models.FloatField(db_column='失败建库使用量', blank=True, null=True)
    researchM = models.FloatField(db_column='科研项目使用量', blank=True, null=True)
    othersM = models.FloatField(db_column='其他使用量', blank=True, null=True)
    remainM = models.FloatField(db_column='剩余量', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ":".join([str(self.dna_id), str(self.index)])

    class Meta:
        db_table = '样本DNA库存信息表'
        verbose_name = '样本DNA库存信息表'
        ordering = ['index']


# 表4 甲基化建库表
class LibraryInfo(models.Model):
    singleLB_id = models.CharField(
        db_column='建库编号', unique=True, max_length=255, blank=True, null=True)
    sample_id = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='DLibraryInfo_ClinicalInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    dna_id = models.ForeignKey(
        "ExtractInfo",
        on_delete=models.CASCADE,
        related_name='DLibraryInfo_ExtractInfo',
        to_field="dna_id",
        db_column='DNA提取编号',
        blank=True,
        null=True)
    singleLB_name = models.CharField(
        db_column='文库名', max_length=255, blank=True, null=True)
    label = models.CharField(
        db_column='样本标签', max_length=255, blank=True, null=True)
    barcodes = models.CharField(
        db_column='index列表', max_length=255, blank=True, null=True)
    LB_date = models.DateField(db_column='建库日期', blank=True, null=True)
    LB_method = models.CharField(
        db_column='建库方法', max_length=255, blank=True, null=True)
    mass = models.FloatField(db_column='起始量', blank=True, null=True)
    pcr_cycles = models.IntegerField(db_column='PCR循环数', blank=True, null=True)
    LB_con = models.FloatField(db_column='文库浓度', blank=True, null=True)
    LB_vol = models.FloatField(db_column='文库体积', blank=True, null=True)
    operator = models.CharField(
        db_column='操作人', max_length=255, blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.singleLB_id

    class Meta:
        db_table = '甲基化建库表'
        verbose_name = '甲基化建库表'
        ordering = ['index']


# 表5 甲基化捕获文库信息表
class CaptureInfo(models.Model):
    poolingLB_id = models.CharField(
        db_column='pooling号',
        unique=True,
        max_length=255,
        blank=True,
        null=True)
    hybrid_date = models.DateField(db_column='杂交日期', blank=True, null=True)
    probes = models.CharField(
        db_column='杂交探针', max_length=255, blank=True, null=True)
    hybrid_hours = models.FloatField(db_column='杂交时间', blank=True, null=True)
    postpcr_cycles = models.IntegerField(
        db_column='PostPCR循环数', blank=True, null=True)
    postpcr_con = models.FloatField(
        db_column='PostPCR浓度', blank=True, null=True)
    elution_vol = models.FloatField(db_column='洗脱体积', blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.poolingLB_id

    class Meta:
        db_table = '甲基化捕获文库信息表'
        verbose_name = '甲基化捕获文库信息表'
        ordering = ['index']


# 表6 pooling表
class PoolingInfo(models.Model):
    sample_id = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='PoolingInfo_ClinicalInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    dna_id = models.ForeignKey(
        "ExtractInfo",
        on_delete=models.CASCADE,
        related_name='PoolingInfo_ExtractInfo',
        to_field="dna_id",
        db_column='DNA提取编号',
        blank=True,
        null=True)
    singleLB_id = models.ForeignKey(
        "LibraryInfo",
        on_delete=models.CASCADE,
        related_name='PoolingInfo_LibraryInfo',
        to_field="singleLB_id",
        db_column='建库编号',
        blank=True,
        null=True)
    poolingLB_id = models.ForeignKey(
        "CaptureInfo",
        on_delete=models.CASCADE,
        related_name='PoolingInfo_CaptureInfo',
        to_field="poolingLB_id",
        db_column='pooling号',
        blank=True,
        null=True)
    pooling_ratio = models.FloatField(
        db_column='pooling比例', blank=True, null=True)
    mass = models.FloatField(db_column='取样', blank=True, null=True)
    volume = models.FloatField(db_column='体积', blank=True, null=True)
    singleLB_Pooling_id = models.CharField(
        db_column='文库编号', unique=True, max_length=255, blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.singleLB_Pooling_id

    class Meta:
        db_table = 'pooling表'
        verbose_name = 'pooling表'
        ordering = ['index']


# 表7 测序登记表
class SequencingInfo(models.Model):
    sequencing_id = models.CharField(
        db_column='测序编号', unique=True, max_length=255, blank=True, null=True)
    poolingLB_id = models.ForeignKey(
        "CaptureInfo",
        on_delete=models.CASCADE,
        related_name='SequencingInfo_CaptureInfo',
        to_field="poolingLB_id",
        db_column='pooling号',
        blank=True,
        null=True)
    sequencing_type = models.CharField(
        db_column='测序类型', max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(db_column='上机时间', blank=True, null=True)
    end_time = models.DateTimeField(db_column='下机时间', blank=True, null=True)
    machine_id = models.CharField(
        db_column='机器号', max_length=255, blank=True, null=True)
    chip_id = models.CharField(
        db_column='芯片号', max_length=255, blank=True, null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sequencing_id

    class Meta:
        db_table = '测序登记表'
        verbose_name = '测序登记表'
        ordering = ['index']


# 表8 样本测序质控表
class QCInfo(models.Model):
    QC_id = models.CharField(
        db_column='Sample', unique=True, max_length=255, blank=True, null=True)
    data_size_gb_field = models.FloatField(
        db_column='Data_Size-Gb', blank=True, null=True)
    clean_rate_field = models.FloatField(
        db_column='Clean_Rate', blank=True, null=True)
    r1_q20 = models.FloatField(db_column='R1_Q20', blank=True, null=True)
    r2_q20 = models.FloatField(db_column='R2_Q20', blank=True, null=True)
    r1_q30 = models.FloatField(db_column='R1_Q30', blank=True, null=True)
    r2_q30 = models.FloatField(db_column='R2_Q30', blank=True, null=True)
    gc_content = models.FloatField(
        db_column='GC_Content', blank=True, null=True)
    bs_conversion_rate_lambda_dna_field = models.FloatField(
        db_column='BS_conversion_rate-lambda_DNA', blank=True, null=True)
    bs_conversion_rate_chh_field = models.FloatField(
        db_column='BS_conversion_rate-CHH', blank=True, null=True)
    bs_conversion_rate_chg_field = models.FloatField(
        db_column='BS_conversion_rate-CHG', blank=True, null=True)
    uniquely_paired_mapping_rate = models.FloatField(
        db_column='Uniquely_Paired_Mapping_Rate', blank=True, null=True)
    mismatch_and_indel_rate = models.FloatField(
        db_column='Mismatch_and_InDel_Rate', blank=True, null=True)
    mode_fragment_length_bp_field = models.FloatField(
        db_column='Mode_Fragment_Length-bp', blank=True, null=True)
    genome_duplication_rate = models.FloatField(
        db_column='Genome_Duplication_Rate', blank=True, null=True)
    genome_depth_x_field = models.FloatField(
        db_column='Genome_Depth', blank=True, null=True)
    genome_dedupped_depth_x_field = models.FloatField(
        db_column='Genome_Dedupped_Depth', blank=True, null=True)
    genome_coverage = models.FloatField(
        db_column='Genome_Coverage', blank=True, null=True)
    genome_4x_cpg_depth_x_field = models.FloatField(
        db_column='Genome_4X_CpG_Depth', blank=True, null=True)
    genome_4x_cpg_coverage = models.FloatField(
        db_column='Genome_4X_CpG_Coverage', blank=True, null=True)
    genome_4x_cpg_methylation_level = models.FloatField(
        db_column='Genome_4X_CpG_methylation_level', blank=True, null=True)
    panel_4x_cpg_depth_x_field = models.FloatField(
        db_column='Panel_4X_CpG_Depth', blank=True, null=True)
    panel_4x_cpg_coverage = models.FloatField(
        db_column='Panel_4X_CpG_Coverage', blank=True, null=True)
    panel_4x_cpg_methylation_level = models.FloatField(
        db_column='Panel_4X_CpG_methylation_level', blank=True, null=True)
    panel_ontarget_rate_region_field = models.FloatField(
        db_column='Panel_Ontarget_Rate-region', blank=True, null=True)
    panel_duplication_rate_region_field = models.FloatField(
        db_column='Panel_Duplication_Rate-region', blank=True, null=True)
    panel_depth_site_x_field = models.FloatField(
        db_column='Panel_Depth-site_X', blank=True, null=True)
    panel_dedupped_depth_site_x_field = models.FloatField(
        db_column='Panel_Dedupped_Depth-site_X', blank=True, null=True)
    panel_coverage_site_1x_field = models.FloatField(
        db_column='Panel_Coverage-site_1X', blank=True, null=True)
    panel_coverage_site_10x_field = models.FloatField(
        db_column='Panel_Coverage-site_10X', blank=True, null=True)
    panel_coverage_site_20x_field = models.FloatField(
        db_column='Panel_Coverage-site_20X', blank=True, null=True)
    panel_coverage_site_50x_field = models.FloatField(
        db_column='Panel_Coverage-site_50X', blank=True, null=True)
    panel_coverage_site_100x_field = models.FloatField(
        db_column='Panel_Coverage-site_100X', blank=True, null=True)
    panel_uniformity_site_20_mean_field = models.FloatField(
        db_column='Panel_Uniformity-site_gt0.2mean', blank=True, null=True)
    strand_balance_f_field = models.FloatField(
        db_column='Strand_balance-F', blank=True, null=True)
    strand_balance_r_field = models.FloatField(
        db_column='Strand_balance-R', blank=True, null=True)
    gc_bin_depth_ratio = models.FloatField(
        db_column='GC_bin_depth_ratio', blank=True, null=True)
    sample_id = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='QCInfo_ClinicalInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    dna_id = models.ForeignKey(
        "ExtractInfo",
        on_delete=models.CASCADE,
        related_name='QCInfo_ExtractInfo',
        to_field="dna_id",
        db_column='DNA提取编号',
        blank=True,
        null=True)
    singleLB_id = models.ForeignKey(
        "LibraryInfo",
        on_delete=models.CASCADE,
        related_name='QCInfo_LibraryInfo',
        to_field="singleLB_id",
        db_column='建库编号',
        blank=True,
        null=True)
    poolingLB_id = models.ForeignKey(
        "CaptureInfo",
        on_delete=models.CASCADE,
        related_name='QCInfo_CaptureInfo',
        to_field="poolingLB_id",
        db_column='pooling号',
        blank=True,
        null=True)
    singleLB_Pooling_id = models.ForeignKey(
        "PoolingInfo",
        on_delete=models.CASCADE,
        related_name='QCInfo_PoolingInfo',
        to_field="singleLB_Pooling_id",
        db_column='文库编号',
        blank=True,
        null=True)
    sequencing_id = models.ForeignKey(
        "SequencingInfo",
        on_delete=models.CASCADE,
        related_name='QCInfo_SequencingInfo',
        to_field="sequencing_id",
        db_column='测序编号',
        blank=True,
        null=True)
    others = models.CharField(
        db_column='备注', max_length=255, blank=True, null=True)
    index = models.AutoField(primary_key=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.QC_id

    class Meta:
        db_table = '样本测序质控表'
        verbose_name = '样本测序质控表'
        ordering = ['index']


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class UploadFile(models.Model):
    uploadFile = models.FileField(
        db_column='上传文件',
        upload_to=user_directory_path,
        null=True)
    uploadUrl = models.CharField(db_column='项目', max_length=255)
    uploadOperator = models.CharField(
        db_column='上传者',
        max_length=255,
        blank=True,
        null=True)

    def __str__(self):
        return self.uploadFile.url

    class Meta:
        db_table = '上传文件信息表'
        verbose_name = '上传文件信息表'
