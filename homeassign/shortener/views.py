from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import UrlRedirect
from django.db.models import F
import json
import string
import random
import sqlite3

def redirects(request, generated_redirect):
    try:
        # find the UrlRedirect object that holds generated_redirect
        o = UrlRedirect.objects.get(generated_redirect=generated_redirect)
        # increment and save count
    
        o.count = F("count") + 1
        o.save(update_fields=["count"])
        return redirect(o.original_url)

    except UrlRedirect.DoesNotExist:
        # show error if invalid generated_redirect was entered
        return HttpResponse("invalid Url")

@csrf_exempt
def create(request):
    if request.method == "POST":
        # check body correctness
        try:
            body = json.loads(request.body)
        except Exception:
            response = HttpResponse(status=400)
            response['content'] = "Bad Request - wrong body format"
            print("maybe here")
            return response

        if "url" not in body:
            response = HttpResponse(status=400)
            response['content'] = "Bad Request - body must contain url"
            print("here")
            return response
    
        letters = string.ascii_letters
        all = letters.join(string.digits)
        # find a unique end point
        res_str = ''.join(random.choice(all) for _ in range(6))
        res_str = ''.join(random.sample(res_str, len(res_str)))
        while True:
            try:
                UrlRedirect.objects.create(original_url=body['url'], generated_redirect=res_str)
                break
            except sqlite3.IntegrityError:
                res_str = ''.join(random.choice(all) for _ in range(6))
                res_str = ''.join(random.sample(res_str, len(res_str)))
        # add the new UrlRedirect object
        return HttpResponse("http://localhost:8000/s/%s" % res_str)
    # if GET - send Method Not Allowed
    if request.method == "GET" or request.method == "PUT" or request.method == "DELETE":
        response = HttpResponse(status=405)
        response['content'] = "Method Not Allowed - must be POST"
        return response
