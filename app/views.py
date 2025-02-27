from django.shortcuts import render

from .documents import BookDocument


def index(request):
    q = request.GET.get('q')
    context = {}
    if q:
        s = BookDocument.search().query('match', title=q)
        context['books'] = s
        print(len(s.to_queryset()))
    return render(request, 'index.html', context)
