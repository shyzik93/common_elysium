from django.shortcuts import render


def view_broadcasts(request):
    #return str([page_id, page_code])
    
    context = {
        'page_title': 'Трансляции',
        'description': 'fdgdfgdgtdgg',
        'keywords': 'svfdb',
    }
    
    return render(request, 'broadcasts/index.html', context)