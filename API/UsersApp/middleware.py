from rest_framework.response import Response
from django.middleware.csrf import get_token

class RequestLogMiddleWare(object):
    wl_views = ['/api/users/login/']
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(request.path)
        if isinstance(response, Response) and request.path in self.wl_views:
            print(response)
            response['csrftoken'] = get_token(request)
            # you need to change private attribute `_is_render` 
            # to call render second time
            response._is_rendered = False 
            response.render()
        return response