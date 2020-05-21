from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache 

def index_t(request):
    return render(request, 'index.html', {'role': 't'})
    
def index_r(request):
    return render(request, 'index.html', {'role': 'r'})    

@csrf_exempt
def send(request):
    d = request.POST.get("d", "")
    r = request.POST.get("r", "")
    if (r == "r"):
        key = "t"
    else:
        key = "r"
        
    last = cache.get('last-'+key)
    # print(d)
    cache.set('last', r) 
    return JsonResponse({'d': last})
