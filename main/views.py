from django.shortcuts import render
from asgiref.sync import sync_to_async
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
        {'auto_suggestions', auto_suggestions}
    )