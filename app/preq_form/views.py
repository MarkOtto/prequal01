import json
import mimetypes

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage

from preq_form.models import Model_PFT, Model_PF


# GC загрузка шаблона формы из файла в базу
class View_GC_Upload_PFT(View):
    # форма загрузки (начальная, до загрузки)
    def get(self,request):
        return render(
            request,
            'gc_upload.html',
            {'result':'w', 'color':'red'}
        )

    def post(self, request):
        if request.FILES['pft']:  # если файл передан
            file = request.FILES['pft']
            comment = request.POST.get('comment')
            content = file.read().decode("utf-8")
            try:
                a = json.loads(content)
            except:
                return render(
                    request,
                    'gc_upload.html',
                    {'result': 'Error parsing JSON file!', 'color':'red'}
                )

                #return HttpResponse("Ошибка при парсинге фвйла")
            pft = Model_PFT.objects.create(
                content=content,
                comment=comment,
            )
            #return HttpResponse("Файл загружен")
            return render(
                request,
                'gc_upload.html',
                {'result': 'The Prequal Form Template is successfully loaded!', 'color':'#2480EB'}
            )
        return render(
            request,
            'gc_upload.html',
            {'result':'The Prequal Form Template wasn\'t loaded', 'color':'red'}
        )

class View_Sub_PF(View):

    # GET - отображение формы
    def get(self, request):
        pf_str = Model_PF.objects.get(id=1)
        pf_dat = pf_str.json
        pft_str = Model_PFT.objects.get(id=21)
        pft_dat = pft_str.content
        return render(
            request,
            'sub_pf.html',
            {
                'data': pf_dat,
                'template': pft_dat,
            }
        )

class View_Sub_Send(View):

    # GET - обработка формы
    def get(self, request):
        params = request.GET
        pf_data = json.dumps(params)
        pf = Model_PF.objects.get(id=1)
        pf.json = pf_data
        pf.save()

        return HttpResponse('OK')

        return render(
            request,
            'sub_pf.html',
            {}
        )

""" СОХРАНЕНИЕ ФАЙЛА ИЗ ПОСТ
    file = request.FILES['pft']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
"""


"""

# ФЛ: Скачивание файла договора
class Download_View(View):

    def get(self, request):  # для браузера
        fl_path='document.pdf'
        filename='document.pdf'
        #fl_path='1.txt'
        #filename='1.txt'
        fl = open(fl_path, 'r')
        #mime_type, _ = mimetypes.guess_type(fl_path)
        #response = HttpResponse(fl, content_type=mime_type)
        response = HttpResponse('1234')
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    def get(self, request):  # для браузера
        id = str(request.get_full_path())[10:]
        print('id=',id)
        records = Model_Doc.objects.filter(url=id)
        if len(records) != 1:
            return HttpResponseNotFound('Not found')
        fl = records[0].doc_file

        fl_path='document.pdf'
        #fl_path='1.txt'
        #fl = open(fl_path, 'rb')
        print(1)
        record = Model_Doc.objects.filter(id='a8fffb09-dcff-4458-9880-26c456a1f2c9')
        fl = record[0].doc_file

        response = HttpResponse(
            #'1234',
            fl,
            headers={
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'attachment; filename="foo.pdf"',
            }
        )
        return response

# ФЛ: Отображение формы для ввода короткого кода
class View_form_enter_code(View):

    def get(self, request):  # для браузера
        print('View_for_kod_verification===get===')

        url = str(request.get_full_path())[1:]
        records = Model_Doc.objects.filter(url=url)
        if len(records) != 1:
            return HttpResponseNotFound('Not found')

        state = records[0].state
        if Doc.check_if_signed(state):              # если подписан - шаблон с текстом
            return render(
                request,
                'page_verified_allready.html',
                {'url':url}
            )

        state = Doc.set_state_FRM(state, '1')
        records[0].state = state
        records[0].save()
        return render(                              # если не подписан - шаблон с формой
            request,
            'page_verify.html',
            {'url':url, 'max_length': records[0].sms_len_kod, }
        )

# ФЛ: Проверка короткого кода, введенного в форму
class View_verify_code_fl(View):

    def post(self, request):  # для браузера
        kod = request.POST['code']
        url = request.POST['url']
        records = Model_Doc.objects.filter(url=url)
        n = len(records)
        if n == 0:  # нет заявки с таким url - ошибка
            #return HttpResponse('Ошибка!')
            return HttpResponseNotFound('Not found')
        elif n >1: # больше 1 заявки с таким url = сбой в сервисе, которого не должно быть (при создании заявки)
            return HttpResponse('Ошибка!')
        if kod == records[0].kod:
            state = records[0].state
            state = Doc.set_state_FRM(state, '2')
            records[0].state = state
            records[0].save()
            return HttpResponse("Документ подписан!")
        else:
            return HttpResponse("Код неверный!")

# API: Проверка статусов документов
@method_decorator(csrf_exempt, name='dispatch')  # для status не используем csrf токены
class Status_View(View):

    #order = 'body_url'            # body, body_url, url_body
    #order = 'url_body'
    order = 'url'
    #order = 'body'

    parameters = {                # это должно быть в Doc View - что на входе в запросе, не менять - привязано к структуре класса Doc
        "key"       : "",         # Параметры аутенификации
        "login"     : "",
        "password"  : "",
        "id"        : "",         # Список запрашиваемых документов
    }

    def post(self, request):
        print('==1==')
        parameters = parse_parameters(request=request, parameters=self.parameters, order=self.order,)
        print('==2==')
        if parameters['code'] != 0:
            return HttpResponseBadRequest('eroor parsing parameters')
        print('==3==')
        parameters = parameters['result']
        print('==4==')
        owner = Model_API_Client.check_auth(parameters)  # аутенификация
        print('==5==')
        if owner is None:
            return HttpResponseForbidden('403 • Forbidden')
        print('==6==')
        s = parameters['id']  # строка в виде списка строк ['', '', '']
        print('s=',s)
        try:
            ids = json.loads(s)
        except:
            return HttpResponseBadRequest('eroor parsing ID list')

        print('ids=',ids)
        print('==7==')

        result = {'signed': [], 'unsigned': [], }  # 'not_found': [] - их просто нет в выдаче
        records = Model_Doc.objects.filter(id__in=ids)

        for record in records:
            print('record.id=',record.id)
            print('record.state=',record.state)
            state = record.state
            if Doc.check_if_signed(state):              # если подписан - шаблон с текстом
                result['signed'].append(record.id.hex)
            else:
                result['unsigned'].append(record.id.hex)

        return HttpResponse(json.dumps(result))
        #return HttpResponse(json.dumps(self.parameters, indent=2))

# API: Проверка короткого кода, введенного в CRM
@method_decorator(csrf_exempt, name='dispatch')  # для status не используем csrf токены
class Verify_View(View):

    #order = 'body_url'            # body, body_url, url_body
    #order = 'url_body'
    order = 'url'
    #order = 'body'

    parameters = {                # это должно быть в Doc View - что на входе в запросе, не менять - привязано к структуре класса Doc
        "key"       : "",         # Параметры аутенификации
        "login"     : "",
        "password"  : "",
        "id"        : "",         # ID документа
        "code"      : "",         # Короткий код
    }

    def post(self, request):
        parameters = parse_parameters(request=request, parameters=self.parameters, order=self.order,)
        if parameters['code'] != 0:
            return HttpResponseBadRequest('eroor parsing parameters')
        parameters = parameters['result']
        owner = Model_API_Client.check_auth(parameters)  # аутенификация
        if owner is None:
            return HttpResponseForbidden('403 • Forbidden')
        records = Model_Doc.objects.filter(id=parameters['id'])
        if len(records) != 1:
            return HttpResponseNotFound('Not found')
        state = records[0].state
        if records[0].kod == parameters['code']:
            state = Doc.set_state_API(state, '2')
            records[0].state = state
            records[0].save()
            return HttpResponseNotFound('OK')
        else:
            state = Doc.set_state_API(state, '1')
            records[0].state = state
            records[0].save()
            return HttpResponseNotFound('Incorrect')

# API: Создание нового документа
@method_decorator(csrf_exempt, name='dispatch')  # для doc не используем csrf токены
class Doc_View(View):
    # Контроллер для DOC

    @staticmethod
    def parse_parameters(request):
        p = {
            # Параметры аутенификации
            'key'      : request.GET.get('key'      ,''),
            'login'    : request.GET.get('login'    ,''),
            'password' : request.GET.get('password' ,''),
            # Параметры SMS
            'phone'    : request.GET.get('phone'    ,''),
            'sms_text' : request.GET.get('sms_text' ,''), #'Для подписания договора сообщите сотруднику код <KOD_4> или введите его на странице <URL_32>'
            # Параметры почтового сообщения
            'email'    : request.GET.get('email'    ,''),
            'mail_text': request.GET.get('mail_text','Для подписания договора перейдите на страницу <URL> и следуйте инструкциям'),
            'mail_sub' : request.GET.get('mail_sub' ,'Подписание договора'),
            # Документ
            'doc_name' : request.GET.get('doc_name' ,'doc.pdf'),
            'doc_mime' : request.GET.get('doc_mime' ,'application/pdf'),
            'doc_text' : request.GET.get('doc_text' ,''),
            'doc_file' : request.body,
            # Параметры повторной отправки
            'new_sms'  : request.GET.get('new_sms'  ,'5,2'),
            'new_mail' : request.GET.get('new_mail' ,'3,1'),
            # Параметры верификации
            'ver_sms'  : request.GET.get(''         ,'5,1'),
            'expires'  : request.GET.get(''         ,''),  # класс doc автоматом подставит макс срок действия оферты
        }
        return p

    def post(self, request):
        parameters = self.parse_parameters(request)
        doc = Doc()
        if not doc.check_auth(parameters):
            return HttpResponseForbidden('403 • Forbidden')

        result = {'code_final':[], 'id':''}

        OK = doc.create(parameters)

        print('post=',OK)

        result['code_final'] = doc.errors
        if OK:
            result['id'] = doc.id.hex

        #return HttpResponse(json.dumps(result))
        return HttpResponse('{\n  "code_final" : ' + json.dumps(result['code_final']) + ',\n  "id"         : "' + result['id'] + '"\n}')

    def get(self, request): return self.post(request)  # для браузера


@method_decorator(csrf_exempt, name='dispatch')  # для тестов не используем csrf токены
class View_for_test_parse_parameters(View):
    №Контроллер для тестов

    #order = 'body_url'            # body, body_url, url_body
    #order = 'url_body'
    order = 'url'
    #order = 'body'

    parameters = {                # это должно быть в Doc View - что на входе в запросе, не менять - привязано к структуре класса Doc
        "key"       : "",         # Параметры аутенификации
        "login"     : "",
        "password"  : "",
        "phone"     : "",         # Параметры SMS
        "sms_text"  : "",
        "email"     : "",
        "mail_text" : "",
        "mail_sub"  : "",
        "mail_sub"  : "",
        "doc_file"  : "",
        "new_sms"   : "",
        "new_mail"  : "",
        "ver_sms"   : "",
        "expires"   : "",
    }

    def get(self, request):
        self.parameters = parse_parameters(request=request, parameters=self.parameters, order=self.order,)
        return HttpResponse(json.dumps(self.parameters, indent=2))



    #order = 'body_url'            # body, body_url, url_body
    #order = 'url_body'
    #order = 'url'
    #order = 'body'

    parameters = {                # это должно быть в Doc View - что на входе в запросе, не менять - привязано к структуре класса Doc
        "key"       : "",         # Параметры аутенификации
        "login"     : "",
        "password"  : "",
        "phone"     : "",         # Параметры SMS
        "sms_text"  : "",
        "email"     : "",         # Параметры почтового сообщения
        "mail_text" : "",
        "mail_sub"  : "",
        "doc_name"  : "",
        "doc_mime"  : "",
        "new_sms"   : "",
        "new_mail"  : "",
        "ver_sms"   : "",
        "expires"   : "",
    }

        if self.parameters['code'] != 0:
            pass
            # здесь - все устарело:
            # 1 - ошибка UTF decode для json-body
            # 2 - ошибка парсинга json-body
            # 3 - неверный порядок парсинга

"""