from django.conf import settings
from rest_framework import serializers

from .models import *


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ClinicalInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = ClinicalInfo
        fields = ('sample_id', 'name', 'gender', 'age', 'patientId', 'category', 'stage', 'diagnose', 'diagnose_others',
                  'centrifugation_date', 'hospital', 'department', 'plasma_num', 'adjacent_mucosa_num',
                  'cancer_tissue_num', 'WBC_num', 'stool_num', 'send_date', 'others', 'index', 'last_modify_date',
                  'created')


class ExtractInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = ExtractInfo
        fields = ('dna_id', 'sample_id', 'extract_date', 'sample_type', 'sample_volume', 'extract_method', 'dna_con',
                  'dna_vol', 'others', 'index', 'last_modify_date', 'created')


class DNAUsageRecordInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = DNAUsageRecordInfo
        fields = ('dna_id', 'sample_id', 'LB_date', 'mass', 'usage', 'singleLB_id', 'others',
                  'index', 'last_modify_date', 'created')


class DNAInventoryInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = DNAInventoryInfo
        fields = ('dna_id', 'sample_id', 'totalM', 'successM', 'failM', 'researchM', 'othersM',
                  'index', 'last_modify_date', 'created')


class LibraryInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = LibraryInfo
        fields = ('singleLB_id', 'sample_id', 'dna_id', 'tube_id', 'clinical_boolen', 'singleLB_name', 'label',
                  'barcodes', 'LB_date', 'LB_method', 'kit_batch', 'mass', 'pcr_cycles', 'LB_con', 'LB_vol',
                  'operator', 'others', 'index', 'last_modify_date', 'created')


class CaptureInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = CaptureInfo
        fields = ('poolingLB_id', 'hybrid_date', 'probes', 'hybrid_min', 'postpcr_cycles', 'postpcr_con', 'elution_vol',
                  'operator', 'others', 'index', 'last_modify_date', 'created')


class PoolingInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = PoolingInfo
        fields = ('sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'pooling_ratio', 'mass', 'volume',
                  'singleLB_Pooling_id', 'others', 'index', 'last_modify_date', 'created')


class SequencingInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = SequencingInfo
        fields = ('sequencing_id', 'poolingLB_id', 'send_date', 'start_time', 'end_time', 'machine_id', 'chip_id',
                  'others', 'index', 'last_modify_date', 'created')


class QCInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = QCInfo
        fields = ('QC_id', 'data_size_gb_field', 'clean_rate_field', 'r1_q20', 'r2_q20', 'r1_q30', 'r2_q30',
                  'gc_content', 'bs_conversion_rate_lambda_dna_field', 'bs_conversion_rate_chh_field',
                  'bs_conversion_rate_chg_field', 'uniquely_paired_mapping_rate', 'mismatch_and_indel_rate',
                  'mode_fragment_length_bp_field', 'genome_duplication_rate', 'genome_depth_x_field',
                  'genome_dedupped_depth_x_field', 'genome_coverage', 'genome_4x_cpg_depth_x_field',
                  'genome_4x_cpg_coverage', 'genome_4x_cpg_methylation_level', 'panel_4x_cpg_depth_x_field',
                  'panel_4x_cpg_coverage', 'panel_4x_cpg_methylation_level', 'panel_ontarget_rate_region_field',
                  'panel_duplication_rate_region_field', 'panel_depth_site_x_field',
                  'panel_dedupped_depth_site_x_field', 'panel_coverage_site_1x_field', 'panel_coverage_site_10x_field',
                  'panel_coverage_site_20x_field', 'panel_coverage_site_50x_field', 'panel_coverage_site_100x_field',
                  'panel_uniformity_site_20_mean_field', 'strand_balance_f_field', 'strand_balance_r_field',
                  'gc_bin_depth_ratio', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id',
                  'sequencing_id', 'others', 'index', 'last_modify_date', 'created')


class UserInfoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ("username", "nick_name", "email", "bulk_delete_privilege", "password")


class DatabaseRecordSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DatabaseRecord
        fields = ("nick_name", "model_changed", "operation", "others", "index", "last_modify_date", "created")
