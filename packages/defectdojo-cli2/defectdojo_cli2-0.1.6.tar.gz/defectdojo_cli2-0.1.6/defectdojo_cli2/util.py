from datetime import datetime
import json
import requests


class Util(object):
    # Generic method for all HTTP requests
    # IMPORTANT: The url must end with '/', otherwise some requests will not work
    def request_apiv2(
        self,
        http_method,
        url,
        api_key,
        params=dict(),
        data=None,
        files=None,
        verify=True,
    ):
        headers = dict()
        headers["Authorization"] = "Token " + api_key
        if not files:
            headers["Accept"] = "application/json"
            headers["Content-Type"] = "application/json"

        # if files:
        #    headers["Content-Type"] = "multipart/form-data"

        response = requests.request(
            method=http_method,
            url=url,
            params=params,
            data=data,
            files=files,
            headers=headers,
            verify=verify,
        )
        try:
          response
          response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])
        except requests.exceptions.ReadTimeout as errrt:
            print("Time out")
        except requests.exceptions.ConnectionError as conerr:
            print("Connection error")
        except requests.exceptions.RequestException as errex:
            print("Exception request")
        return response

    # Pretty print JSON response exiting with a sucess if the response status code is the same as the 'sucess_status_code' argument
    def default_output(self, response, sucess_status_code):
        json_out = json.loads(response.text)
        pretty_json_out = json.dumps(json_out, indent=4)
        print(pretty_json_out)

        if response.status_code == sucess_status_code:  # Sucess
            exit(0)
        else:  # Failure
            exit(1)
