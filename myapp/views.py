from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Webhook(APIView):
    def post(self, request):
        print("\n\n\n************************************",request.data,"\n\n\n\n**********************************")

        return Response(data="Sucess")
    
    def get(self,request):
        print("\n\n\n************************************",request.GET,"\n\n\n\n**********************************")

        return Response(data="Sucess")