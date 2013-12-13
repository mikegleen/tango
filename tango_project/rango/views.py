# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm



def decode_url(url):
    return url.replace('_', ' ')


def encode_url(url):
    return url.replace(' ', '_')


def category(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name}
    context_dict['category_name_url'] = category_name_url

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html', context_dict, context)


def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    for category in category_list:
        category.url = encode_url(category.name)
        pages = Page.objects.filter(category=category)
        category.pages = pages.order_by('-views')[:5]
    return render_to_response('rango/index.html', context_dict, context)

#    return HttpResponse("""Rango says hello world!
#            <a href='/rango/about'>About</a>""")

def about(request):
    return HttpResponse("""Rango says: Here is the about page.
               """)


def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render_to_response('rango/add_category.html', {'form': form}, context)


def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            cat = Category.objects.get(name=category_name)
            page.category = cat
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()
    return render_to_response('rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name,
             'form': form},
            context)

        
