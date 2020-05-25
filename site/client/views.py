from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache 

import time
import datetime
from datetime import timezone

def index(request):
    return render(request, 'index.html')
       

@csrf_exempt
def send(request):
    # print(request.POST)
    d = request.POST.get("d", "")
    a = request.POST.get("a", "")
    
    # save info about this frame 
    cache.set('c-' + a, d) 
    dt = datetime.datetime.now()
    timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
    cache.set('l-' + a, timestamp)
    o_dic = cache.get('d')
    if o_dic is None:
        o_dic = {}
        
    dic = {}
    res = {}
    
    # get other webcams frame
    for o_a in o_dic.keys(): 
        if a == o_a:
            continue
        last_seen = int(cache.get('l-' + o_a))
        if timestamp - last_seen > 3:
            dic.pop(o_a, None)
            continue
        
        dic[o_a] = 1
        res[o_a] = cache.get('c-' + o_a)
    
    dic[a] = 1
    cache.set('d', dic)

    return JsonResponse(res)
