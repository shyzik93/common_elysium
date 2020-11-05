from django.shortcuts import render

# Create your views here.

def view_index(request):
    #return str([page_id, page_code])
    
    context = {
        'content': str({'page_id':8787878}),
        'page_title': 'tile',
        'description': 'fdgdfgdgtdgg',
        'keywords': 'svfdb',
    }
    
    return render(request, 'main/index.html', context)