import re

class RenderCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        response.content = re.sub(b'\\n*\\s+\\n', b'\\n', response.content)
        return response