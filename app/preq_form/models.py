from django.db import models
from datetime import datetime


class Model_PFT(models.Model):   # шаблоны Prequal Form
    created = models.DateTimeField(default=datetime.now)  # ЖЦ: дата и время создания заявки
    content = models.TextField()
    comment = models.CharField(max_length=32)
    # active - only one!

    def __str__(self):
        return str(self.id) + ' • • • ' + self.created.strftime('%Y-%m-%d %H:%M') + ' •  •  •  ' + self.comment

class Model_PF(models.Model):   # заполненные Prequal Form
    # ссылка на GC
    # ссылка на Sub
    created = models.DateTimeField(default=datetime.now)  # ЖЦ: дата и время создания заявки
    #pft = models.ForeignKey(to=Model_PFT, verbose_name='Template', db_index=True, on_delete=models.CASCADE,)
    json = models.TextField()



"""
class Model_API_Client(models.Model):  # Учетная запись клиента
    key   = models.CharField(                         # API-ключ клиента
        max_length=64,
        unique=True,                                  # ключи уникальны
        db_index=True,                                # ускоренный поиск
    )
    login = models.CharField(                         # Логин клиента
        max_length=32,
        unique=True,                                  # логины уникальны
        db_index=True,                                # ускоренный поиск
    )
    password = models.CharField(                      # Пароль клиента
        max_length=32
    )
    sms_text  = models.TextField(                     # По ум = ФЛ: текст SMS с кодами и адресом
        blank=True, null=True,                        # необязательное
    )
    mail_text = models.TextField(                     # По уи = ФЛ: текст сообщения
        blank=True, null=True,                        # необязательное
    )
    mail_sub = models.CharField(                      # По уи = ФЛ: тема сообщения
        max_length=50,
        blank=True, null=True,                        # необязательное
    )
    doc_name = models.TextField(                      # По уи = ФЛ: название файла документа
        blank=True, null=True,                        # необязательное
    )
    doc_mime = models.TextField(                      # По уи = ФЛ: mime-type файла
        blank=True, null=True,                        # необязательное
    )
    doc_file = models.BinaryField(                    # По уи = ФЛ: содержимое файла
        blank=True, null=True,                        # необязательное
    )
    ver_sms_attempts = models.SmallIntegerField(      # По уи = верификация короткого кода из SMS: кол-во попыток
        blank=True, null=True,                        # необязательное
    )
    ver_sms_interval = models.CharField(             # По уи = верификация короткого кода из SMS: интервалы между попытками (json)
        max_length=50,
        blank=True, null=True,                        # необязательное
    )
    new_sms_attempts = models.SmallIntegerField(      # По уи = повторная отправка SMS: кол-во попыток
        blank=True, null=True,                        # необязательное
    )
    new_sms_interval = models.CharField(             # По уи = повторная отправка SMS: интервалы между попытками (json)
        max_length=50,
        blank=True, null=True,                        # необязательное
    )
    new_mail_attempts = models.SmallIntegerField(     # По уи = повторная отправка почтового сообщения: кол-во попыток
        blank=True, null=True,                        # необязательное
    )
    new_mail_interval = models.CharField(             # По уи = повторная отправка почтового сообщения: интервалы между попытками (json)
        max_length=50,
        blank=True, null=True,                        # необязательное
    )
    expires  = models.DurationField(                  # ЖЦ: дата и время когда заявка "протухает"
        blank=True, null=True,                        # необязательное
    )

    @staticmethod
    def check_auth(parameters):  # возвращает логин
        #print('parameters=',parameters)
        login = parameters['login']
        passw = parameters['password']
        key   = parameters['key']
        records = None
        auth_key = auth_login = False
        if key:
            records = Model_API_Client.objects.filter(key=key)
            n = len(records)
            auth_key = (n == 1)
        elif login and passw:                         # дб заданы и логин и пароль - во избежание лишних запросов
            records = Model_API_Client.objects.filter(login=login, password=passw)
            n = len(records)
            auth_login = (n == 1)
        if auth_key or auth_login:
            return records[0]
        else: return None

    def __str__(self):
        return str(self.id) + ' • ' + self.login


class Model_Doc(models.Model):                        # Учетная запись документа
    owner = models.ForeignKey(Model_API_Client,on_delete = models.CASCADE)
    id  = models.UUIDField(primary_key=True)          # UUID = ID для API-запросов
    url = models.CharField(                           # ФЛ: короткий URL с формой верификации для ФЛ
        max_length=32,                                # '116c46003f0e4be9ac24a50201909dc6' => 'https://offer-easy.ru/116c46003f0e4be9ac24a50201909dc6'
        blank=False,
        db_index=True,
    )
    kod = models.CharField(                           # ФЛ: код подтверждения = 1234, 123456 ...
        max_length=6,
        blank=False,
    )
    phone = models.CharField(                         # ФЛ: номер телефона, привязанный к документу = '79191112233'
        max_length=11,
        blank=False,
    )
    email = models.CharField(max_length=100)          # ФЛ: почтовый ящик, если пустой - рассылки нет
    sms_text = models.TextField(                      # ФЛ: текст SMS с кодами и адресом = 'Для подписания документа сообщите код <<<CODE>>> менеджеру или введите его на странице <<<URL>>>'
        blank=True,                                   # по ум - из Model_API_Client
    )
    mail_text = models.TextField(                     # ФЛ: текст сообщения
        blank=True,                                   # по ум - из Model_API_Client
    )
    mail_sub = models.CharField(                      # ФЛ: тема сообщения
        max_length=50,
        blank=True,                                   # по ум - из Model_API_Client
    )
    doc_file = models.BinaryField(                    # ФЛ: файл с документом
        blank=True,                                   # по ум - из Model_API_Client
    )
    doc_name = models.TextField(                      # ФЛ: название файла
        blank=True,                                   # по ум - из Model_API_Client
    )
    doc_mime = models.TextField(                      # ФЛ: mime-тип файла
        blank=True,                                   # по ум - из Model_API_Client
    )

    sms_config  = models.SmallIntegerField()          # ФЛ: SMS: конфигурация  = 0..3
    sms_len_kod = models.SmallIntegerField()          # ФЛ: SMS: длина короткого кода
    sms_len_url = models.SmallIntegerField()          # ФЛ: SMS: длина URL

    #life_cycle = models.SmallIntegerField()          # ЖЦ: состояние
    state = models.CharField(                         # ЖЦ: состояние = описание в doc
        max_length=30,
        blank=False
    )
    created  = models.DateTimeField()                 # ЖЦ: дата и время создания заявки
    expires  = models.DateTimeField(                  # ЖЦ: дата и время когда заявка "протухает"
        blank=True,                                   # по ум - из Model_API_Client
    )

    ver_sms_attempts = models.SmallIntegerField(      # ЖЦ: верификация короткого кода из SMS: кол-во попыток
        blank=True,                                   # по ум - из Model_API_Client
    )
    ver_sms_interval = models.CharField(              # ЖЦ: верификация короткого кода из SMS: интервалы между попытками (json)
        max_length=50,
        blank=True,                                   # по ум - из Model_API_Client
    )
    new_sms_attempts = models.SmallIntegerField(      # ЖЦ: повторная отправка SMS: кол-во попыток
        blank=True,                                   # по ум - из Model_API_Client
    )
    new_sms_interval = models.CharField(              # ЖЦ: повторная отправка SMS: интервалы между попытками (json)
        max_length=50,
        blank=True,                                   # по ум - из Model_API_Client
    )
    new_mail_attempts = models.SmallIntegerField(     # ЖЦ: повторная отправка почтового сообщения: кол-во попыток
        blank=True,                                   # по ум - из Model_API_Client
    )
    new_mail_interval = models.CharField(             # ЖЦ: повторная отправка почтового сообщения: интервалы между попытками (json)
        max_length=50,
        blank=True,                                   # по ум - из Model_API_Client
    )

    history  = models.TextField()                     # json с историей действий по договору

    @staticmethod
    def check_uniq_id(id):
        records = Model_Doc.objects.filter(id=id)
        return len(records) == 0

    @staticmethod
    def check_uniq_url(url):
        records = Model_Doc.objects.filter(url=url)
        return len(records) == 0

    def __str__(self):
        return(
            datetime.strftime(self.created, '%y-%m-%d %H:%M:%S') + ' • login: ' +
            self.owner.login + ' • id: ' +
            self.id.hex + ' • КОД: ' +
            self.kod + ' • ' +
            self.url + ' • ' +
            self.phone + ' • ' +
            self.email
        )



    #notify   = models.SmallIntegerField()            # тип уведомления ФЛ = 1 (сразу), 0 (по отдельной команде)


    @staticmethod
    def check_auth(parameters):  # возвращает логин
        LOGIN = 'adv56'
        PASSW = 'n3lk45lk5'
        KEY   = 'nfs56dss7833lsk495lk5'

        auth_key = auth_login = False

        login = parameters['login']
        passw = parameters['password']
        key   = parameters['key']

        if key: # если в запросе указан ключ - авторизуемся по нему
            auth_key = (key == KEY)
        elif login and passw:                 # во избежание лишних запросов
            auth_login = (login == LOGIN and passw == PASSW)
        # print('auth=', auth_key or auth_login)
        return auth_key or auth_login


"""
