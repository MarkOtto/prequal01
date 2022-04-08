from django.contrib import admin
from datetime       import datetime

"""
from backend.models import Model_API_Client, Model_Doc

# Register your models here.

admin.site.register(Model_API_Client)


@admin.register(Model_Doc)
class Model_Doc_Admin(admin.ModelAdmin):
    date_hierarchy = 'created'  # виджет даты в админке
    list_display = ('id_admin', 'created', 'owner', 'kod', 'url', 'phone_admin', 'email', 'sms_len_kod', 'sms_len_url', 'sms_config', )

    # fields = ('id', 'url', 'phone') # поля на страницах NEW + EDIT

    #@admin.display(description='Дата создания')
    #def created_admin(self, obj):
    #    return obj.created.strftime('%Y-%m-%d %H:%M:%S')

    @admin.display(description='ID')
    def id_admin(self, obj):
        return obj.id.hex

    @admin.display(description='Телефон')
    def phone_admin(self, obj):
        return obj.phone[0:1] + '\u202f' + obj.phone[1:4] + '\u202f' + obj.phone[4:7] + '\u202f' + obj.phone[7:11]
"""
