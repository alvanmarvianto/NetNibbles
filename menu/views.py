from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Menu


# Create your views here.
def index(request):
    template_name = 'index.html'
    menu = Menu.objects.all()
    
    context = { "menu": menu }
#    return render(request, 'index.html', context)
    return render(request, template_name, context)

'''
def id_listview(request):
    template_name = 'index.html'
    queryset1 = Identity.objects.all()
    context = {
        "object_list1": queryset1
    }
    return render(request, template_name, context)
    
def res_listview(request):
    template_name = 'resume.html'
    queryset2 = Experience.objects.all()
    queryset2 = Education.objects.all()
    context = {
        "object_list2": queryset1, "object_list2": queryset1
    }
    return render(request, template_name, context)

def pro_listview(request):
    template_name = 'index.html'
    queryset = Project.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, template_name, context)
    
'''