from django.contrib.auth.decorators import login_required
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


@never_cache
def UserInfoV(request):
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
    except SignatureExpired:
        # 激活链接已过期
        return render(request, 'active.html', {'error_msg': '激活链接已过期'})
    except:
        # 激活链接已过期
        return render(request, 'active.html', {'error_msg': '激活链接无效，'})


def Active_resendV(request):
    if request.method == 'POST':
        key_ = request.POST.get('name')
        value_ = request.POST.get('value')
        try:
            user = User.objects.get(**{key_: value_})
            if user.is_active:
                return JsonResponse({'error_msg': '用户已激活，请返回登录页面进行登录。'})
            else:
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


@login_required
@csrf_exempt
def AdvancedSearchV(request):
    special_fields = ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'sequencing_id']
    model_links = {
        'ClinicalInfo': ['sample_id'],
        'ExtractInfo': ['sample_id', 'dna_id'],
        'DNAUsageRecordInfo': ['sample_id', 'dna_id'],
        'DNAInventoryInfo': ['sample_id', 'dna_id'],
        'LibraryInfo': ['sample_id', 'dna_id', 'singleLB_id'],
        'CaptureInfo': ['poolingLB_id'],
        'PoolingInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id'],
        'SequencingInfo': ['poolingLB_id', 'sequencing_id'],
        'QCInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'sequencing_id']
    }
    models_set = [ClinicalInfo, ExtractInfo, DNAUsageRecordInfo, DNAInventoryInfo, LibraryInfo, CaptureInfo,
                  PoolingInfo, SequencingInfo, QCInfo]
    merge_df = []
    for m in [0, 1, 2, 3, 4, 6, 5, 7, 8]:
        if m == 0:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = fields[6:25]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['sample_id'] else 'ClinicalInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            merge_df = res_df
        elif m == 1:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = fields[5:14]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['sample_id', 'dna_id'] else 'ExtractInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df.columns)
            merge_df = pd.merge(merge_df, res_df, how='left', on='sample_id')
            merge_df = merge_df[['sample_id', 'dna_id'] + columns_raw[1:] + fields_filt_rename[2:]]
        elif m == 2:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = [fields[0]] + fields[2:7]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['dna_id'] else 'DNAUsageRecordInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            merge_df = pd.merge(merge_df, res_df, how='left', on='dna_id')
        elif m == 3:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = fields[1:7]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            res_raw_shift = []
            for l_ in res_raw:
                res_raw_shift.append(list(l_) + [round(l_[1] - l_[2] - l_[3] - l_[4] - l_[5], 3)])
            fields_filt_rename = [x if x in ['dna_id'] else 'DNAInventoryInfo_' + x for x in fields_filt + ['remainM']]
            res_df = list2array(res_raw_shift, fields_filt_rename)
            merge_df = pd.merge(merge_df, res_df, how='left', on='dna_id')
        elif m == 4:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = [fields[2]] + fields[5:19]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['dna_id', 'singleLB_id'] else 'LibraryInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df.columns)
            merge_df = pd.merge(merge_df, res_df, how='left', left_on='DNAUsageRecordInfo_singleLB_id',
                                right_on='singleLB_id')
            merge_df['singleLB_id'] = merge_df['DNAUsageRecordInfo_singleLB_id']
            merge_df = merge_df[['sample_id', 'dna_id', 'singleLB_id'] + columns_raw[2:] + fields_filt_rename[1:]]
        elif m == 6:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = fields[3:10]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id'] else
                                  'PoolingInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df.columns)
            merge_df = pd.merge(merge_df, res_df, how='left', on='singleLB_id')
            merge_df = merge_df[['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id'] +
                                columns_raw[3:] + fields_filt_rename[2:5] + [fields_filt_rename[6]]]
        elif m == 5:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = fields[3:13]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['poolingLB_id'] else 'CaptureInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df.columns)
            idx_ = columns_raw.index('PoolingInfo_pooling_ratio')
            merge_df = pd.merge(merge_df, res_df, how='left', on='poolingLB_id')
            merge_df = merge_df[columns_raw[:idx_] + fields_filt_rename[1:] + columns_raw[idx_:]]
        elif m == 7:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = [fields[11]] + fields[1:8]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            res_raw_shift = []
            for l_ in res_raw:
                if isinstance(l_[0], int):
                    res_raw_shift.append(list(l_))
                else:
                    for idx in l_[0]:
                        res_raw_shift.append([idx] + list(l_[1:]))
            fields_filt_rename = [x if x in ['sequencing_id'] else 'SequencingInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw_shift, fields_filt_rename)
            columns_raw = list(merge_df.columns)
            idx_ = columns_raw.index('CaptureInfo_index')
            merge_df = pd.merge(merge_df, res_df, how='left', left_on='CaptureInfo_index',
                                right_on='SequencingInfo_poolingLB_id')
            merge_df = merge_df[special_fields + columns_raw[5:idx_] + columns_raw[idx_ + 1:] + fields_filt_rename[2:]]
        elif m == 8:
            fields = [field.name for field in models_set[m]._meta.get_fields()]
            fields_filt = fields[:44]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id',
                                             'singleLB_Pooling_id', 'sequencing_id'] else 'QCInfo_' +
                                                                                          x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            merge_df = pd.merge(merge_df, res_df, how='left', on=special_fields)
    merge_df_columns = list(merge_df.columns)
    filed_idx = [6, 24, 31, 36, 42, 56, 64, 68, 74, 112]
    models_set = ['ClinicalInfo', 'ExtractInfo', 'DNAUsageRecordInfo', 'DNAInventoryInfo', 'LibraryInfo', 'CaptureInfo',
                  'PoolingInfo', 'SequencingInfo', 'QCInfo']
    # print(">>>>>>>>>>>>>> merge_df_columns >>>>>>>>")
    # pprint(merge_df_columns)

    if request.method == 'POST':
        modellist = request.POST['modellist'].split(', ')
        # print(">>>>>>>>>>>>>> modellist >>>>>>>>")
        # pprint(modellist)
        links_dict = {}
        res_columns_normal = []
        for m in range(len(models_set)):
            if models_set[m] in modellist:
                res_columns_normal = res_columns_normal + merge_df_columns[filed_idx[m]:filed_idx[m + 1]]
                for link in model_links[models_set[m]]:
                    links_dict[link] = 1
        res_columns_link = []
        for link in special_fields:
            if link in links_dict:
                res_columns_link.append(link)
        res_raw = merge_df[res_columns_link + res_columns_normal]
        # print(">>>>>>>>>>>> res_raw.column >>>>>>>>>>>>")
        # pprint(res_raw.columns)
        res_filt = res_raw
        if request.POST['queryset']:  # 有过滤条件
            filter_total = ""
            for i in request.POST['queryset'].split('\n'):
                filter_line = pd.Series(data=[True] * len(merge_df))
                for j in i.split(' AND '):
                    not_, m, f, vp, v = j.split('\t')
                    not_ = not_[1:]
                    v = v[:-1]
                    # print(">>>>>>>>>> not_, m, f, vp, v >>>>>>>>")
                    # print("%s, %s, %s, %s, %s" % (not_, m, f, vp, v))
                    filter_condition = filter_conditionFunc(res_raw, f, vp, v, not_) if f in special_fields else \
                        filter_conditionFunc(res_raw, m + '_' + f, vp, v, not_)
                    filter_line = filter_line & filter_condition
                filter_total = filter_line if filter_total == "" else filter_total | filter_line
            res_filt = res_raw[filter_total]
        # make res_pro
        # print(">>>>>>>>>>>>>> res_filt >>>>>>>>")
        # pprint(res_filt)
        res_pro = []
        for nrow in range(len(res_filt)):
            dat = {}
            link_n = 0
            for link in special_fields:
                if link in links_dict:
                    value_ = list(res_filt[link])[nrow]
                    if pd.isna(value_):
                        value_ = " "
                    dat["link%s" % link_n] = value_
                    link_n = link_n + 1
            normal_n = 0
            for col in res_columns_normal:
                value_ = list(res_filt[col])[nrow]
                if pd.isna(value_):
                    value_ = " "
                elif isinstance(value_, np.floating):
                    value_ = "%.3f" % value_
                elif isinstance(value_, np.integer):
                    value_ = "%d" % value_
                elif isinstance(value_, str):
                    value_ = "%s" % value_

                dat["normal%s" % normal_n] = value_
                normal_n = normal_n + 1
            res_pro.append(dat)
        result = {
            'draw': 1,
            'recordsTotal': len(res_raw),
            'recordsFiltered': len(res_pro),
            'data': res_pro
        }
        # print(">>>>>>>>>>>>>> result >>>>>>>>")
        # pprint(result)
        return JsonResponse(result)
    else:
        return render(request, 'AdvancedSearch.html')
