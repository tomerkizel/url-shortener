from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import UrlRedirect
from urllib.parse import urlparse
import json
import string
import random
import sqlite3

def redirects(request, generated_redirect):
    try:
        # find the UrlRedirect object that holds generated_redirect
        o = UrlRedirect.objects.get(generated_redirect=generated_redirect)
        # increment and save count
        o.increment()
        print(o.counter)
        UrlRedirect.save(o, update_fields=['counter'])
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
        
        # try:
        #     result = urlparse(body['url'])
        #     if not all([result.scheme, result.netloc]):
        #         response = HttpResponse(status=400)
        #         response['content'] = "Bad Request - wrong url format"
        #         print("or here")
        #         return response
        # except:
        #     response = HttpResponse(status=400)
        #     response['content'] = "Bad Request - wrong url format"
        #     print("or there")
        #     return response
        # generate the new url end point
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
    if request.method == "GET":
        response = HttpResponse(status=405)
        response['content'] = "Method Not Allowed - must be POST"
        return response
