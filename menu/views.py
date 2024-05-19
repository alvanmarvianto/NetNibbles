from django.shortcuts import render

from .models import Menu
from django.db.models import Q

# Create your views here.
def index(request):
    template_name = 'index.html'
    menu1 = Menu.objects.filter(Q(category__iexact='Makanan') |
                                Q(category__icontains='Makanan'))
    menu2 = Menu.objects.filter(Q(category__iexact='Minuman') |
                                Q(category__icontains='Minuman'))
    menu3 = Menu.objects.filter(Q(category__iexact='Dessert') |
                                Q(category__icontains='Dessert'))
    
    context = { "menu1": menu1, "menu2": menu2, "menu3": menu3 }
    return render(request, template_name, context)

