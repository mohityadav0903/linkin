from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from rest_framework import serializers
# Create your views here.
class Webhook(APIView):
    def post(self, request):
        print("\n\n\n************************************",request.data,"\n\n\n\n**********************************")
        ghl_api_key = request.GET.get("twilead_api_key")
        tag_type = request.GET.getlist("type")
        print(tag_type)
        if ghl_api_key == None:
            raise serializers.ValidationError("twilead_api_key is required.")
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
                    "tags":tag_type,
                    "customField": cust_field
                    })

            print("\n\n POST PAYLOAD", payload)

            url = "https://rest.gohighlevel.com/v1/contacts/"
            final_response = requests.request("POST", url, headers=headers, data=payload).json()
            print("\n\n\n** POST RESPONSE **\n\n",final_response)
        # return Response(data="Sucess")

        else:
            id = response.get("contacts")[0].get("id")
            tags = response.get("contacts")[0].get("tags")
            tag_var=tags + tag_type
            print(tags,tag_var)
            cust_field = {}
            cust_field[con_name.get("public_identifier")] = request.data.get("contact").get("public_identifier")
            cust_field[con_name.get("Message")] = request.data.get("messenger").get("message")
            cust_field[con_name.get("profile_link")] = request.data.get("contact").get("profile_link")
            payload = json.dumps({
                    "firstName": request.data.get("contact").get("first_name"),
                    "lastName": request.data.get("contact").get("last_name"),
                    "address1": request.data.get("contact").get("address"),
                    "companyName": request.data.get("contact").get("company_name"),
                    "tags": tag_var,
                    "customField": cust_field
                    })
            print("\n\n PUT PPAYLOAD RESPONSE", payload)

            url = "https://rest.gohighlevel.com/v1/contacts/" + str(id)
            final_response = requests.request("PUT", url, headers=headers, data=payload).json()
            print("\n\n\n** PUT RESPONSE **\n\n",final_response)
        return Response(data="sucess")

    def get(self,request):
        print("\n\n\n************************************",request.GET,"\n\n\n\n**********************************")

        return Response(data="Sucess")

class GHLWebhook(APIView):
    def post(self, request):
        # print(request.data)
        # print(request.GET)
        key = request.GET.get("key")
        # ghl_api_key = request.GET.get("ghl_api_key")
        camp_id = request.GET.get("camp_id")
        secret = request.GET.get("secret")

        if request.GET.get("type") == "assign":
            print("done")
            payload = json.dumps({"profile_link": request.data.get("profile_link")})
            print(payload)
            headers = {
            'Content-Type': 'application/json',
            }
            url = "https://api.liaufa.com/api/v1/open-api/campaign-instance/"+str(camp_id)+"/assign/?key="+str(key) +"&secret=" +str(secret)
            final_response = requests.request("POST", url, headers=headers, data=payload).json()
            print("response",final_response)
        return Response(data="sucess")

class MsgWebhook(APIView):
    def post(self, request):

        msg = request.data.get("Message")
        profile_url = request.data.get("Likedin Url")
        print(msg,profile_url)
        headers = {
        'Content-Type': 'application/json',
        'Origin':'https://app.leadin.tech'
        }
        data =json.dumps({
              "username": "clement@leadin.fr",
              "password": "er1919rce"
            })
        resp = requests.request("POST", "https://api.liaufa.com/api/v1/token/",headers=headers, data=data).json()
        print(resp)
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + resp.get("access")
        }


        resp = requests.request("GET", "https://api.liaufa.com/api/v1/linkedin/accounts/?page_size=100",headers=headers).json()
        print(resp)
        for data in resp.get("results"):
            if data.get("name") == "Pierre-Ange CHEMARIN":
                li_id = data.get("id")
                break
        print(li_id)
        resp = requests.request("GET", "https://api.liaufa.com/api/v1/linkedin/messenger/?search=" +  str(profile_url) + "&li_account_id=" + str(li_id) + "&ordering=-last_datetime",headers=headers).json()
        print(resp)
        messenger_id = resp.get("results")[0].get("id")
        data = json.dumps({"body":str(msg),"messenger":messenger_id,"image_template":None})
        print(data)
        resp = requests.request("POST", "https://api.liaufa.com/api/v1/linkedin/messenger/messages/",headers=headers, data=data).json()
        print(resp)
        return Response(data=resp)



