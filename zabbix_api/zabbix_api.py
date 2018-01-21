# zabbix_api.py
# Zabbix API Operation util.
#
# [AUTHOR]
# sy4may0
#
# [VERSION]
# 1.0

import requests
import json

class zabbix_api():
    # IP address or Domain name of Zabbix Server.
    __zbx_addr = None
    # Zabbix API URL.
    __zbx_api_url = None
    # Zabbix API Request headers.
    __zbx_api_headers = {"Content-Type":"application/json-rpc"}
    # Authentication key of Zabbix API.
    __authentication_key = None
    # Zabbix API requesting id.
    __zbx_api_id = 1

    # __init__
    # Constructor.
    # Request user.login method to Zabbix API
    # and get authentication-key.
    #
    # [PARAMETERS]
    # string   zbx_addr  : IP address or Domain name of Zabbix Server.
    # string   user      : Zabbix user.
    # string   password  : Zabbix user password.
    def __init__(self, zbx_addr, user, password):
        self.__zbx_addr = zbx_addr
        
        url = []
        url.append("http:/")
        url.append(self.__zbx_addr)
        url.append("zabbix")
        url.append("api_jsonrpc.php")
        self.__zbx_api_url = "/".join(url)

        payload = dict()
        params = dict()

        params["user"] = user
        params["password"] = password

        payload["jsonrpc"] = "2.0"
        payload["method"] = "user.login"
        payload["params"] = params
        payload["id"] = self.__zbx_api_id
        payload["auth"] = None

        response = requests.post( \
                    self.__zbx_api_url, \
                    headers=self.__zbx_api_headers, \
                    data=json.dumps(payload) \
                    )


        result = json.loads(response.text)

        if result["id"] != self.__zbx_api_id:
            raise id_mismatch_exception( \
                            self.__zbx_api_id, \
                            result["id"] \
                            )
            return

        self.__authentication_key = result["result"]

    # zbx_post
    # Send the request of Zabbix API and get result.
    #
    # [PARAMETERS]
    # String   method    : Zabbix API method.
    # dict     params    : Zabbix API parameters.
    #
    # [RETURN]
    # dict     result    : Zabbix API response data.
    def zbx_post(self, method, params):
        payload = dict()

        payload["jsonrpc"] = "2.0"
        payload["method"] = method
        payload["params"] = params
        payload["id"] = 1
        payload["auth"] = self.__authentication_key

        response = requests.post( \
                    self.__zbx_api_url, \
                    headers=self.__zbx_api_headers, \
                    data=json.dumps(payload) \
                    )

        result = json.loads(response.text)

        if result["id"] != self.__zbx_api_id:
            raise id_mismatch_exception( \
                            self.__zbx_api_id, \
                            result["id"] \
                            )

        return result
         
# id_mismatch_exception
# The Exception for Zabbix API id mismatch.
class id_mismatch_exception():
    __message = None
    # Request Zabbix API id.
    __request_id = 0
    # Response Zabbix API id.
    __response_id = 0

    def __init__(self, req_id, res_id):
        self.__request_id = req_id
        self.__response_id = res_id
        m = []
        m.append("Exchanged Zabbix API id is mismatch.")
        m.append("Request id: " + self.__request_id)
        m.append("Response id: " + self.__response_id)
        self.message = " ".join(m)

    def get_message(self): 
        return self.__message

    def get_request_id(self):
        return self.__request_id

    def get_response_id(self):
        return self.__response_id
