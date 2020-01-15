from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from rest_framework import viewsets

from .data_process import *
from .forms import FileUploadModelForm, RegisterForm
from .serializers import *
from .tasks import send_register_active_email


@never_cache
def index(request):
    return render(request, 'base.html')

def get_queryset_base(model_, query_params_):
    query_params = {}
    tmp_dict = query_params_.dict()
    # print(">>>>>> model_ >>>>>")
    # pprint(model_)
    # print(">>>>>> query_params_ >>>>>")
    # pprint(query_params_)
    if 'format' in tmp_dict and tmp_dict['format'] == 'datatables':
        return model_.objects.all()
    for key_ in tmp_dict:
        if key_ != 'format':
            query_params[key_] = tmp_dict[key_]
    if len(query_params.keys()) > 0:
        queryset = model_.objects.filter(**query_params)
        return queryset
    else:
        queryset = model_.objects.all()
        return queryset

class ClinicalInfoViewSet(viewsets.ModelViewSet):
    queryset = ClinicalInfo.objects.all()
    serializer_class = ClinicalInfoSerializer

    def get_queryset(self):
        return get_queryset_base(ClinicalInfo, self.request.query_params)


class ExtractInfoViewSet(viewsets.ModelViewSet):
    queryset = ExtractInfo.objects.all()
    serializer_class = ExtractInfoSerializer

    def get_queryset(self):
        return get_queryset_base(ExtractInfo, self.request.query_params)


class DNAUsageRecordInfoViewSet(viewsets.ModelViewSet):
    queryset = DNAUsageRecordInfo.objects.all()
    serializer_class = DNAUsageRecordInfoSerializer

    def get_queryset(self):
        return get_queryset_base(DNAUsageRecordInfo, self.request.query_params)



class DNAInventoryInfoViewSet(viewsets.ModelViewSet):
    queryset = DNAInventoryInfo.objects.all()
    serializer_class = DNAInventoryInfoSerializer

    def get_queryset(self):
        return get_queryset_base(DNAInventoryInfo, self.request.query_params)

class LibraryInfoViewSet(viewsets.ModelViewSet):
    queryset = LibraryInfo.objects.all()
    serializer_class = LibraryInfoSerializer

    def get_queryset(self):
        return get_queryset_base(LibraryInfo, self.request.query_params)

class CaptureInfoViewSet(viewsets.ModelViewSet):
    queryset = CaptureInfo.objects.all()
    serializer_class = CaptureInfoSerializer

    def get_queryset(self):
        return get_queryset_base(CaptureInfo, self.request.query_params)

class PoolingInfoViewSet(viewsets.ModelViewSet):
    queryset = PoolingInfo.objects.all()
    serializer_class = PoolingInfoSerializer

    def get_queryset(self):
        return get_queryset_base(PoolingInfo, self.request.query_params)

class SequencingInfoViewSet(viewsets.ModelViewSet):
    queryset = SequencingInfo.objects.all()
    serializer_class = SequencingInfoSerializer

    def get_queryset(self):
        return get_queryset_base(SequencingInfo, self.request.query_params)

class QCInfoViewSet(viewsets.ModelViewSet):
    queryset = QCInfo.objects.all()
    serializer_class = QCInfoSerializer

    def get_queryset(self):
        return get_queryset_base(QCInfo, self.request.query_params)

class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return get_queryset_base(User, self.request.query_params)


@login_required
def Main_model(request, re_model):
    if re_model == 'Clinical':
        return render(request, 'ClinicalInfo.html')
    elif re_model == 'Extract':
        return render(request, 'ExtractInfo.html')
    elif re_model == 'DNAUsageRecord':
        return render(request, 'DNAUsageRecordInfo.html')
    elif re_model == 'DNAInventory':
        return render(request, 'DNAInventoryInfo.html')
    elif re_model == 'Library':
        return render(request, 'LibraryInfo.html')
    elif re_model == 'Capture':
        return render(request, 'CaptureInfo.html')
    elif re_model == 'Pooling':
        return render(request, 'PoolingInfo.html')
    elif re_model == 'Sequencing':
        return render(request, 'SequencingInfo.html')
    elif re_model == 'QC':
        return render(request, 'QCInfo.html')
    elif re_model == 'User':
        return render(request, 'UserInfo.html')


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


@login_required
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
                            'LibraryInfo_ClinicalInfo__mass', 'LibraryInfo_ClinicalInfo__pcr_cycles',
                            'LibraryInfo_ClinicalInfo__LB_con', 'LibraryInfo_ClinicalInfo__LB_vol',
                            'LibraryInfo_ClinicalInfo__operator', 'LibraryInfo_ClinicalInfo__others'],
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
        # print(">>>>>> request >>>>>>>")
        # pprint(request)
        # print(">>>>>> request.POST >>>>>>>")
        # pprint(request.POST)
        modellist = request.POST['modellist'].split(', ')
        # print(">>>>>> modellist >>>>>>>")
        # pprint(modellist)
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

        # print(">>>>>> values_list1 >>>>>>>")
        # pprint(values_list1)
        # print(">>>>>> values_list2 >>>>>>>")
        # pprint(values_list2)
        # print(">>>>>> values_list >>>>>>>")
        # pprint(values_list)
        # print(">>>>>> values_list_filted >>>>>>>")
        # pprint(values_list_filted)
        # raw_data_set存储queryset全部行的原始查询结果
        raw_data_set = []

        if request.POST['queryset']:  # 有过滤条件
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

            # print(">>>>>> queryset >>>>>>>")
            # pprint(queryset)
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

                # print(">>>>>> filter1_dict >>>>>>>")
                # pprint(filter1_dict)
                # print(">>>>>> filter1_dict_list >>>>>>>")
                # pprint(filter1_dict_list)
                # print(">>>>>> filter2_dict >>>>>>>")
                # pprint(filter2_dict)
                raw_data_tmp = ClinicalInfo.objects.filter(*filter1_dict_list).values_list(*values_list_filted)
                # print(">>>>>> raw_data_tmp >>>>>>>")
                # pprint(raw_data_tmp)
                raw_data = []
                if 'remainM' in values_list:
                    idx_ = values_list.index('DNAInventoryInfo_ClinicalInfo__othersM')
                    # print(">>>>>> idx_: %s >>>>>>>" % idx_)
                    for row in raw_data_tmp:
                        # print(">>>>>> row in raw_data_tmp >>>>>>>")
                        # pprint(row)
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
                    raw_data_set.append(raw_data_row)
        else:  # 无过滤条件
            raw_data_tmp = ClinicalInfo.objects.values_list(*values_list_filted)
            # print(">>>>>> raw_data_tmp >>>>>>>")
            # pprint(raw_data_tmp)
            if 'remainM' in values_list:
                idx_ = values_list.index('DNAInventoryInfo_ClinicalInfo__othersM')
                # print(">>>>>> idx_: %s >>>>>>>" % idx_)
                for row in raw_data_tmp:
                    # print(">>>>>> row in raw_data_tmp >>>>>>>")
                    # pprint(row)
                    remainM = None
                    values = list(row[0:idx_ + 1]) + [remainM] + list(row[idx_ + 1:])
                    if row[idx_ - 4] is not None:
                        remainM = row[idx_ - 4] - row[idx_ - 3] - row[idx_ - 2] - row[idx_ - 1] - row[idx_]
                        values = list(row[0:idx_ + 1]) + ["%.3f" % remainM] + list(row[idx_ + 1:])
                    raw_data_set.append(values)
            else:
                raw_data_set = raw_data_tmp
        # 数据进一步处理，生成response内容
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
        # print(">>>>>> pro_data >>>>>>>")
        # pprint(pro_data)
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

@login_required
def AdvanceUploadV(request):
    return render(request, 'AdvancedUpload.html')


@never_cache
def RegisterV(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        username = request.POST.get('username')
        nick_name = request.POST.get('nick_name')
        email = request.POST.get('email')
        if username == '':
            return JsonResponse({'error_msg': '用户名为空，请重新输入。'})
        elif User.objects.filter(username=username):
            return JsonResponse({'error_msg': '用户名已存在，请重新输入。'})
        elif User.objects.filter(nick_name=nick_name):
            return JsonResponse({'error_msg': '昵称已存在，请重新输入。'})
        elif User.objects.filter(email=email):
            return JsonResponse({'error_msg': '邮箱地址已存在，请重新输入。'})
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=username)
            user.is_active = 0
            user.save()

            # 发送激活链接，包含激活链接：(http://%s:8000/user/active/5) % SERVER_HOST
            # 激活链接中需要包含用户的身份信息，并要把身份信息进行加密
            # 激活链接格式: /user/active/用户身份加密后的信息 /user/active/token

            # 加密用户的身份信息，生成激活token
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user.index}
            token = serializer.dumps(info)  # bytes
            token = token.decode('utf8')  # 解码, str
            # 找其他人帮助我们发送邮件 celery:异步执行任务
            # print(">>>>>>>>>>>>>> user.email: %s >>>>>>>>>>>" % user.email)
            # print(">>>>>>>>>>>>>> user.username: %s >>>>>>>>>>>" % user.username)
            # print(">>>>>>>>>>>>>> token: %s >>>>>>>>>>>" % token)
            send_register_active_email(user.email, user.username, token)
            if redirect_to:
                return JsonResponse({'success_msg': '注册成功！请查收激活邮件，激活账号后登录。', 'next': redirect_to})
            else:
                return JsonResponse({'success_msg': '注册成功！请查收激活邮件，激活账号后登录。', 'next': '/'})
        else:
            # print(">>>>>>>>>>>>>>>> form.errors: %s >>>>>>>>>>>>>>>>>" % form.errors)
            # print(">>>>>>>>>>>>>>>> type(form.errors): %s >>>>>>>>>>>>>>>>>" % type(form.errors))
            return JsonResponse({'form_errors': "%s" % form.errors})
    else:
        return render(request, 'register.html')


@never_cache
def ActiveV(request, token):
    # 进行用户激活
    # 进行解密，获取要激活的用户信息
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        # 获取待激活用户的id
        user_index = info['confirm']
        # 根据id获取用户信息
        user = User.objects.get(index=user_index)
        user.is_active = 1
        user.save()
        # 跳转到登录页面
        return render(request, 'active.html', {'success_msg': '账号已激活'})
    except SignatureExpired as e:
        # 激活链接已过期
        return render(request, 'active.html', {'error_msg': '激活链接已过期'})
    except:
        # 激活链接已过期
        return render(request, 'active.html', {'error_msg': '激活链接无效，'})


@never_cache
def Active_resendV(request):
    if request.method == 'POST':
        key_ = request.POST.get('name')
        value_ = request.POST.get('value')
        try:
            user = User.objects.get(**{key_: value_})
            # 加密用户的身份信息，生成激活token
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user.index}
            token = serializer.dumps(info)  # bytes
            token = token.decode('utf8')  # 解码, str
            # 找其他人帮助我们发送邮件 celery:异步执行任务
            # print(">>>>>>>>>>>>>> user.email: %s >>>>>>>>>>>" % user.email)
            # print(">>>>>>>>>>>>>> user.username: %s >>>>>>>>>>>" % user.username)
            # print(">>>>>>>>>>>>>> token: %s >>>>>>>>>>>" % token)
            send_register_active_email(user.email, user.username, token)
            return JsonResponse({'success_msg': '激活邮件发送成功！请注意查收，激活账号后登录。'})
        except User.DoesNotExist:
            return JsonResponse({'error_msg': '用户不存在，请重新输入。'})
    else:
        return render(request, 'active_resend.html')
