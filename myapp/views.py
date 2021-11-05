from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Webhook(APIView):
    def post(self, request):
        print(request.data)

        return Response(data="Sucess")
    
    def get(self,request):
        print(request.GET)

        return Response(data="Sucess")