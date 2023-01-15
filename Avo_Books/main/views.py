from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from requests import get

TITLE_SEARCH = 'https://www.googleapis.com/books/v1/volumes?q=search=intitle={}'


def get_book_details(raw_data:dict) -> dict:
    """get details of books"""

    raw_data = raw_data['items']
    output = dict()

    for i in raw_data:
        meta = i['volumeInfo']
        output.update({
                meta['title']: {
                    'authors': meta.get('authors'),
                    'release': meta.get('publishedDate'),
                    'description': meta.get('description'),
                    'pages': meta.get('pageCount'),
                    'categories': meta.get('categories'),
                    'thumbnail_link': meta.get('imageLinks').get('thumbnail'),
                    'language': meta.get('language'),
                    'link': meta.get('infoLink')
                }
            })
    
    return output


# Create your views here.
def home(request:HttpRequest):
    """home page"""

    template = loader.get_template('home.html')
    return HttpResponse(template.render())

@csrf_exempt
def search_results(request:HttpRequest):
    """after clicking search"""

    template = loader.get_template('search_results.html')

    if request.method == 'GET':
        search = request.GET['search']
        book_data = get(TITLE_SEARCH.format(search)).json()
        details = get_book_details(book_data)

        context = {'books': details}

        return HttpResponse(template.render(context, request))
