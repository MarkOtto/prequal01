"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls    import path
from django.views.generic import TemplateView
from preq_form.views import View_GC_Upload_PFT, View_Sub_PF, View_Sub_Send

urlpatterns = [
    path('admin/', admin.site.urls),
    # Главные страницы
    path('',          TemplateView.as_view(template_name="index.html")),
    path('gc/index',  TemplateView.as_view(template_name="gc_index.html")),   # GC
    path('sub/index', TemplateView.as_view(template_name="sub_index.html")),  # Sub
    # GC
    path('gc/upload', View_GC_Upload_PFT.as_view()),  # адрес загрузки PFT + страница отчета
    # Sub
    path('sub/pf',      View_Sub_PF.as_view()),  # адрес загрузки PFT + страница отчета
    path('sub/pf_send', View_Sub_Send.as_view()),  # адрес загрузки PFT + страница отчета


    #path('sub/bundle.js', View_Sub_PF.as_view()),  # адрес загрузки PFT + страница отчета

    #path('gc/upload', TemplateView.as_view(template_name="gc_upload.html")),  # страница загрузки PFT
    #path('gc/upload_pft', Upload_PFT.as_view()),  # адрес загрузки PFT + страница отчета
    #path('', Simple_Template_View.as_view()),  # главная страница
]
