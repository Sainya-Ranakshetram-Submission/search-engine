from django.shortcuts import render
from asgiref.sync import sync_to_async
from django.utils.html import escape, strip_tags, escapejs
from django.views.decorators.http import require_GET
from bs4 import BeautifulSoup
import urllib
from textblob import TextBlob
import requests
from .models import *

@sync_to_async
@require_GET
def home(request):
    auto_suggestions = None
    if request.session.get('recorded_keywords'):
        auto_suggestions = request.session.get('recorded_keywords')
    return render(
        request, 
        'index.html',
        {'auto_suggestions': auto_suggestions}
    )
 
@sync_to_async
@require_GET   
def search_results(request):
    #Sanitize Data
    query = strip_tags(escape(escapejs(request.GET.get("q"))))
    from textblob import TextBlob
    #Add Auto Suggestions
    auto_suggestions = None
    if request.session.get('recorded_keywords'):
        auto_suggestions = request.session.get('recorded_keywords') + [query]
    else:
        auto_suggestions = [query]
    query_correct = TextBlob(query).correct().__str__()
    query_list=query_correct.split()
    data1 = CrawledWebPages.objects.filter(url__in=query_list)
    data2 = CrawledWebPages.objects.filter(keywords_meta_tags__in=query_list)
    data3 = CrawledWebPages.objects.filter(keywords_in_site__in=query_list)
    data4 = CrawledWebPages.objects.filter(stripped_request_body__in=query_list)
    
    if data1.union(data2, data3, data4).count() > 0:
        results = data1.union(data2, data3, data4).all()
    else:
        results = get_data_from_other_search_engine(query)
    
    spelling_msg_display = False
    if query != query_correct:
        auto_suggestions += [query_correct]
        spelling_msg_display = True
    return render(
        request, 
        'results.html',
        {
            'value_in_input': query,
            'corrected_input': query_correct,
            'spelling_msg_display': spelling_msg_display,
            'results': results,
            'auto_suggestions': auto_suggestions
        }
    )

@sync_to_async
def get_data_from_other_search_engine(query: str):
    query = urllib.parse.quote_plus(query)
    url = 'https://google.com/search?q=' + query
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    head_object = soup.find_all('a')[16:-6]
    ao=[]
    for info in head_object:
        soup_forloop = BeautifulSoup(str(info), 'lxml')
        url = soup_forloop.find('a').attrs.get('href').lstrip('/url?q=')
        if url.find('&sa=') != -1:
            url = url[:url.find('&sa=')]
        a=CrawledWebPages(url=url, title=info.getText(),keywords_meta_tags=query.split(), keywords_in_site=query.split())
        a.save()
        ao.append(a)
    return ao