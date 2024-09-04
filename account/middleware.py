from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, get_object_or_404

class catchLogin404Middleware(MiddlewareMixin):
    def process_response(self,request,response):
        if response.status_code == 404:
            print('Se respondio con un 404')
            return redirect('account:Login')
        return response


class CaptureLastUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 

    def __call__(self,request):
        current_url = request.build_absolute_uri()
        request.session['last_url'] = request.session.get('current_url','/')
        request.session['current_url'] = current_url
        response = self.get_response(request)
        return response
    