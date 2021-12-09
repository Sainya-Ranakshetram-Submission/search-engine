from django.shortcuts import render
from asgiref.sync import sync_to_async
from django.utils.html import escape, strip_tags, escapejs
from django.views.decorators.http import require_GET

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
    #Add Auto Suggestions
    auto_suggestions = None
    if request.session.get('recorded_keywords'):
        auto_suggestions = request.session.get('recorded_keywords') + [query]
    else:
        auto_suggestions = [query]
    
    return render(
        request, 
        'results.html',
        {'auto_suggestions': auto_suggestions}
    )