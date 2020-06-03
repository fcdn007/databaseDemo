import time

from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer_its
from rest_framework import viewsets

from .forms import FileUploadModelForm, RegisterForm
from .serializers import *
from .settings import BASE_DIR
from .tasks import send_register_active_email, make_new_merge_df_by_celery
from .utils import *


@never_cache
def index(request):
    return render(request, 'base.html')


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


class DatabaseRecordViewSet(viewsets.ModelViewSet):
    queryset = DatabaseRecord.objects.all()
    serializer_class = DatabaseRecordSerializer

    def get_queryset(self):
        return get_queryset_base(DatabaseRecord, self.request.query_params)


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
        user = User.objects.get(username=request.user.username)
        # print("form: %s" % form)

        if form.is_valid():
            # print("form.is_valid(): TRUE")
            upload_file = form.save()
            # print('upload_file.uploadUrl: %s' % upload_file.uploadUrl)
            # print('upload_file.uploadOperator: %s' % upload_file.uploadOperator)
            # print('upload_file.uploadFile: %s' % upload_file.uploadFile)
            # print(upload_file.uploadFile.path)
            # read file and add records to model
            total, valid, add, warning, error_msg, fatal_error = save_records(upload_file)
            if fatal_error:
                context2 = {
                    'nick_name': user, 'model_changed': request.POST.get('uploadUrl'),
                    'operation': "批量上传失败",
                    'others': "file_path: {};fatal_error: {}".format(upload_file.uploadFile.path, fatal_error)
                }
                record_obj = DatabaseRecord(**context2)
                record_obj.save()
                return JsonResponse({
                    'error_msg_fatal': fatal_error
                })
            else:
                context2 = {
                    'nick_name': user, 'model_changed': request.POST.get('uploadUrl'),
                    'operation': "批量上传成功",
                    'others': "file_path: {};all_records: {};valid_records: {};error_msg_tolerant: {}".format(
                        upload_file.uploadFile.path, total, valid, error_msg)
                }
                record_obj = DatabaseRecord(**context2)
                record_obj.save()
                return JsonResponse({
                    'all_records': total, 'valid_records': valid, 'add_records': add, 'warning': warning,
                    'error_msg_tolerant': error_msg
                })
        else:
            # print("form.is_valid(): FALSE")
            data = {'error_msg_fatal': "严重错误！！！文件上传和批量添加失败。只允许上传以下格式文件：txt, csv and xlsx。"}
            context2 = {
                'nick_name': user, 'model_changed': request.POST.get('uploadUrl'),
                'operation': "批量上传文件格式错误",
                'others': "无"
            }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()
            return JsonResponse(data)
    return JsonResponse({'error_msg_fatal': '严重错误！！！只接受POST请求。'})


def uniqueV(request):
    foreign_keys = {
        'ExtractInfo': ['sample_id'],
        'DNAUsageRecordInfo': ['sample_id', 'dna_id'],
        'DNAInventoryInfo': ['sample_id', 'dna_id'],
        'LibraryInfo': ['sample_id', 'dna_id'],
        'PoolingInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id'],
        'SequencingInfo': ['poolingLB_id'],
        'QCInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'sequencing_id']
    }
    query_fields = {
        'ClinicalInfo': ["sample_id", "name", "gender", "patientId", "category", "stage", "diagnose", "diagnose_others",
                         "centrifugation_date", "hospital", "department", "send_date", "others"],
        'ExtractInfo': ['sample_id', 'dna_id', 'extract_date', 'sample_type', 'extract_method', 'others'],
        'DNAUsageRecordInfo': ['sample_id', 'dna_id', 'LB_date', 'singleLB_id', 'others'],
        'DNAInventoryInfo': ['sample_id', 'dna_id'],
        'LibraryInfo': ['sample_id', 'dna_id', 'singleLB_id', 'tube_id', 'clinical_boolen', 'singleLB_name', 'label',
                        'barcodes', 'LB_date', 'LB_method', 'kit_batch', 'operator', 'others'],
        'CaptureInfo': ['poolingLB_id', 'hybrid_date', 'probes', 'operator', 'others'],
        'PoolingInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'others'],
        'SequencingInfo': ['poolingLB_id', 'sequencing_id', 'send_date', 'start_time', 'end_time', 'machine_id',
                           'chip_id', 'others'],
        'QCInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'sequencing_id',
                   'others']
    }
    data = {}
    key1 = request.GET['model']
    key2 = request.GET['filed']
    if key1 in query_fields and key2 in query_fields[key1]:
        if key1 in foreign_keys and key2 in foreign_keys[key1]:
            data['values'] = [x[0] for x in
                              FOREIGNKEY_TO_MODEL[key2].objects.values_list(key2).distinct().order_by(key2)]
        else:
            data['values'] = [x[0] for x in
                              KEY1_TO_MODEL[key1].objects.values_list(key2).distinct().order_by(key2)]

    else:
        data['values'] = []
    return JsonResponse(data)


@login_required
@never_cache
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
            user.bulk_delete_privilege = u'无'
            user.save()
            context2 = {
                'nick_name': user, 'model_changed': "User",
                'operation': "注册", 'others': "bulk_delete_privilege: {}".format(user.bulk_delete_privilege)
            }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()

            # 发送激活链接，包含激活链接：(http://%s:8000/user/active/5) % SERVER_HOST
            # 激活链接中需要包含用户的身份信息，并要把身份信息进行加密
            # 激活链接格式: /user/active/用户身份加密后的信息 /user/active/token

            # 加密用户的身份信息，生成激活token
            serializer = Serializer_its(settings.SECRET_KEY, 3600)
            info = {'confirm': user.index}
            token = serializer.dumps(info)  # bytes
            token = token.decode('utf8')  # 解码, str
            # 找其他人帮助我们发送邮件 celery:异步执行任务
            # print(">>>>>>>>>>>>>> user.email: %s >>>>>>>>>>>" % user.email)
            # print(">>>>>>>>>>>>>> user.username: %s >>>>>>>>>>>" % user.username)
            # print(">>>>>>>>>>>>>> token: %s >>>>>>>>>>>" % token)
            send_register_active_email.delay(user.email, user.username, token)
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
    serializer = Serializer_its(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        # 获取待激活用户的id
        user_index = info['confirm']
        # 根据id获取用户信息
        user = User.objects.get(index=user_index)
        user.is_active = 1
        user.save()
        context2 = {
            'nick_name': user, 'model_changed': "User",
            'operation': "激活成功", 'others': "无"
        }
        record_obj = DatabaseRecord(**context2)
        record_obj.save()
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
                serializer = Serializer_its(settings.SECRET_KEY, 3600)
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
    # 合并所有model，形成一张大表
    # 检测所有model的最新修改时间time1，
    # > 如果time1等于已有json文件的时间戳time2，直接读取已有的json文件，
    # > 否则重新创建merge_df，并把merge_df输出为json文件，打上时间戳。清除旧的json文件(保留10个)
    merge_df = []
    flag_update, json_files, time2, time2_json = check_new_merge_df()
    if flag_update:
        # 使用djcelery异步执行make_new_merge_df
        print("do make_new_merge_df_by_celery")
        make_new_merge_df_by_celery.delay(json_files, time2)
    else:
        merge_df = pd.read_json(time2_json)
        for col_ in ['ClinicalInfo_centrifugation_date', 'ClinicalInfo_send_date', 'ExtractInfo_extract_date',
                     'DNAUsageRecordInfo_LB_date', 'LibraryInfo_LB_date', 'CaptureInfo_hybrid_date',
                     'SequencingInfo_send_date', 'SequencingInfo_start_time', 'SequencingInfo_end_time']:
            merge_df.loc[:, col_] = [datetime.datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ').date() for date_
                                     in merge_df.loc[:, col_]]
        print("read merge_df.json")

    if request.method == 'POST':
        # print("request.method == 'POST'")
        if flag_update:  # "等待异步task make_new_merge_df完成"
            sleep_flag = True
            sleep_n = 0
            while sleep_flag:
                print("sleep {}".format(5 * sleep_n))
                for file in os.listdir(os.path.join(MEDIA_ROOT, "json")):
                    if re.match(r'[0-9]+.*\.merge_df.json', file):
                        time2_tmp, _, _ = file.split('.')
                        time2_tmp = int(time2_tmp)
                        # print("time2_tmp: {}".format(time2_tmp))
                        if time2_tmp == time2:
                            time2_json = os.path.join(MEDIA_ROOT, "json", file)
                            sleep_flag = False
                            flag_update = False
                time.sleep(5)
                sleep_n += 1

            merge_df = pd.read_json(time2_json)
            for col_ in ['ClinicalInfo_centrifugation_date', 'ClinicalInfo_send_date', 'ExtractInfo_extract_date',
                         'DNAUsageRecordInfo_LB_date', 'LibraryInfo_LB_date', 'CaptureInfo_hybrid_date',
                         'SequencingInfo_send_date', 'SequencingInfo_start_time', 'SequencingInfo_end_time']:
                merge_df.loc[:, col_] = [datetime.datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ').date() for date_ in
                                         merge_df.loc[:, col_]]
        # print(merge_df)
        merge_df_columns = list(merge_df.columns)
        filed_idx = [6, 24, 31, 36, 42, 56, 64, 68, 74, 112]
        model_list = request.POST['modellist'].split(', ')
        # print(">>>>>>>>>>>>>> model_list >>>>>>>>")
        # pprint(model_list)
        links_dict = {}
        res_columns_normal = []
        for m in range(len(models_set2)):
            if models_set2[m] in model_list:
                res_columns_normal = res_columns_normal + merge_df_columns[filed_idx[m]:filed_idx[m + 1]]
                for link in model_links[models_set2[m]]:
                    links_dict[link] = 1
        res_columns_link = []
        for link in special_fields:
            if link in links_dict:
                res_columns_link.append(link)
        res_raw = merge_df[res_columns_link + res_columns_normal]
        # print(">>>>>>>>>>>> res_raw.column >>>>>>>>>>>>")
        # pprint(res_raw.columns)
        res_filtered = res_raw
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
                    filter_condition = condition_filter(res_raw, f, vp, v, not_) if f in special_fields else \
                        condition_filter(res_raw, m + '_' + f, vp, v, not_)
                    filter_line = filter_line & filter_condition
                filter_total = filter_line if filter_total == "" else filter_total | filter_line
            res_filtered = res_raw[filter_total]
        # make res_pro
        # print(">>>>>>>>>>>>>> res_filtered >>>>>>>>")
        # pprint(res_filtered)
        link_n = 0
        res_pro_df = pd.DataFrame()
        for link in special_fields:
            if link in links_dict:
                res_pro_df.loc[:, "link%s" % link_n] = list(res_filtered[link])
                link_n = link_n + 1
        normal_n = 0
        for col in res_columns_normal:
            res_pro_df.loc[:, "normal%s" % normal_n] = list(res_filtered[col])
            normal_n = normal_n + 1
        res_pro = res_pro_df.to_dict('records')
        # print('res_pro')
        # print(res_pro)
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
        # print("request.method == 'get'")
        return render(request, 'AdvancedSearch.html')


def Download_excel(request, model):
    # print(model)
    if model == 'ClinicalInfo':
        file_name = "ClinicalInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'ExtractInfo':
        file_name = "ExtractInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'DNAUsageRecordInfo':
        file_name = "DNAUsageRecordInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'LibraryInfo':
        file_name = "LibraryInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'CaptureInfo':
        file_name = "CaptureInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'PoolingInfo':
        file_name = "PoolingInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'SequencingInfo':
        file_name = "SequencingInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'QCInfo':
        file_name = "QCInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'CaptureInfoPlus':
        file_name = "CaptureInfoPlus.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response


def Test_model(request, re_model):
    if re_model == 'Clinical':
        return render(request, 'TestClinicalInfo.html')
    elif re_model == 'Extract':
        return render(request, 'TestExtractInfo.html')
    elif re_model == 'DNAUsageRecord':
        return render(request, 'TestDNAUsageRecordInfo.html')
    elif re_model == 'DNAInventory':
        return render(request, 'TestDNAInventoryInfo.html')
    elif re_model == 'Library':
        return render(request, 'TestLibraryInfo.html')
    elif re_model == 'Capture':
        return render(request, 'TestCaptureInfo.html')
    elif re_model == 'Pooling':
        return render(request, 'TestPoolingInfo.html')
    elif re_model == 'Sequencing':
        return render(request, 'TestSequencingInfo.html')
    elif re_model == 'QC':
        return render(request, 'TestQCInfo.html')


def plotDataV(request):
    data = {}
    data_sum = 0
    try:
        key1 = KEY1_TO_MODEL[request.GET['model']]
        key2 = request.GET['field']
        values = key1.objects.values_list(key2)
        data_sum = len(values)
        for v in values:
            if isinstance(v[0], str):
                data[v[0]] = data[v[0]] + 1 if v[0] in data else 1
            elif isinstance(v[0], int) or isinstance(v[0], float):
                k = v[0] // 10
                data[k] = data[k] + 1 if k in data else 1
            elif isinstance(v[0], datetime.date):
                k = int("{}01".format(v[0].year)) if v[0].month < 7 else int("{}02".format(v[0].year))
                data[k] = data[k] + 1 if k in data else 1

        for k in data:
            data[k] = round(100 * data[k] / data_sum, 2)
    except FieldError:
        data['空'] = 100

    data_sort = {}
    if isinstance(list(data.keys())[0], str):
        for k in sorted(data, key=lambda x: x):
            data_sort[k] = data[k]
    elif isinstance(list(data.keys())[0], int) or isinstance(list(data.keys())[0], float):
        if re.match(r'^\d{6}$', str(list(data.keys())[0])):
            for k in sorted(data, key=lambda x: x):
                k_str = "{}年上半年".format(str(k)[:4]) if str(k)[4:] == '01' else "{}年下半年".format(str(k)[:4])
                data_sort[k_str] = data[k]
        else:
            for k in sorted(data, key=lambda x: x):
                k_str = "{}~{}".format(int(10 * k), int(10 * (k + 1)))
                data_sort[k_str] = data[k]

    return JsonResponse({'sum': data_sum, 'data': data_sort})


def test_html(request):
    # print("request: {}".format(request))
    # user = User.objects.get(username=request.user.username)
    # print("request.user: {}".format(request.user))
    # context2 = {
    #     'nick_name': user, 'model_changed': "test",
    #     'operation': "test", 'others': "无"
    # }
    # record_obj = DatabaseRecord(**context2)
    # record_obj.save()
    # print("record_obj: {}".format(record_obj))
    return render(request, 'test.html')
