import time
import urllib
from functools import lru_cache

import requests
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from crawler.common_user_agent import return_random_user_agent
from django.shortcuts import render
from django.utils.html import escape, escapejs, strip_tags
from django.views.decorators.http import require_GET
from textblob import TextBlob

from .models import *
from .search_engine_scrapper import search


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
    start_time = time.time()
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
    data2 = CrawledWebPages.objects.filter(keywords_meta_tags__icontains=query_list)
    data3 = CrawledWebPages.objects.filter(keywords_in_site__icontains=query_list)
    data4 = CrawledWebPages.objects.filter(stripped_request_body__in=query_list)
    
    if data1.union(data2, data3, data4).count() > 0:
        results = data1.union(data2, data3, data4).all()
    else:
        results = search(query)
        
    page = int(request.GET.get("page", 1))
    paginator = Paginator(results, 10)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    
    spelling_msg_display = False
    if query != query_correct:
        auto_suggestions += [query_correct]
        spelling_msg_display = True
    return render(
        request, 
        'results.html',
        {
            'value_in_input': query,
            'title': query,
            'corrected_input': query_correct,
            'spelling_msg_display': spelling_msg_display,
            'results': results,
            'time': time.time()-start_time,
            'auto_suggestions': auto_suggestions
        }
    )
