from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json

# Create your views here.
class Webhook(APIView):
    def post(self, request):
        print("\n\n\n************************************",request.data,"\n\n\n\n**********************************")
        ghl_api_key = request.GET.get("ghl_api_key")
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ghl_api_key
        }
        con_name={}
        print(ghl_api_key)
        url = "https://rest.gohighlevel.com/v1/custom-fields/"
        response = requests.request("GET", url, headers=headers).json()
        # print("\n\n CUSTOM FIELD RESPONSE", response)
        for cust_fields in response.get("customFields"):
        # print(cust_fields)
            con_name[cust_fields.get("name")] = cust_fields.get("id")

        print("\n\n\n CCUSTOM FIELDS DICT:",con_name)
        email = request.data.get("contact").get("email")
        phone = request.data.get("contact").get("phone")
        
        url = "https://rest.gohighlevel.com/v1/contacts/lookup?email=" + str(email)
        response = requests.request("GET", url, headers=headers).json()
        print("\n\n EMAIL LOOKUP RESPONSE", response)

        if response.get("contacts") == None :
            url = "https://rest.gohighlevel.com/v1/contacts/lookup?phone=" + str(phone)
            response = requests.request("GET", url, headers=headers).json()
            print("\n\n PHONE LOOKUP RESPONSE", response)

        if response.get("contacts") == None :
            cust_field = {}
            cust_field[con_name.get("public_identifier")] = request.data.get("contact").get("public_identifier")
            cust_field[con_name.get("Message")] = request.data.get("messenger").get("message")
            cust_field[con_name.get("profile_link")] = request.data.get("contact").get("profile_link")
            payload = json.dumps({
                    "email": request.data.get("contact").get("email"),
                    "phone": request.data.get("contact").get("phone"),
                    "firstName": request.data.get("contact").get("first_name"),
                    "lastName": request.data.get("contact").get("last_name"),
                    "address1": request.data.get("contact").get("address"),
                    "companyName": request.data.get("contact").get("company_name"),
                    "customField": cust_field
                    })

            print("\n\n POST PAYLOAD", payload)

            url = "https://rest.gohighlevel.com/v1/contacts/"
            final_response = requests.request("POST", url, headers=headers, data=payload).json()
            print("\n\n\n** POST RESPONSE **\n\n",final_response)
        # return Response(data="Sucess")

        else:
            id = response.get("contacts")[0].get("id")
            cust_field = {}
            cust_field[con_name.get("public_identifier")] = request.data.get("contact").get("public_identifier")
            cust_field[con_name.get("Message")] = request.data.get("messenger").get("message")
            cust_field[con_name.get("profile_link")] = request.data.get("contact").get("profile_link")
            payload = json.dumps({
                    "firstName": request.data.get("contact").get("first_name"),
                    "lastName": request.data.get("contact").get("last_name"),
                    "address1": request.data.get("contact").get("address"),
                    "companyName": request.data.get("contact").get("company_name"),
                    "customField": cust_field
                    })
            print("\n\n PUT PPAYLOAD RESPONSE", payload)

            url = "https://rest.gohighlevel.com/v1/contacts/" + str(id)
            final_response = requests.request("PUT", url, headers=headers, data=payload).json()
            print("\n\n\n** POST RESPONSE **\n\n",final_response)
        return Response(data="sucess")

    def get(self,request):
        print("\n\n\n************************************",request.GET,"\n\n\n\n**********************************")

        return Response(data="Sucess")