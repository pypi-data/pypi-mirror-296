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
        except requests.exceptions.HTTPError as error:
            print("HTTP Error")
            print(error.args[0])
        except requests.exceptions.ReadTimeout:
            print("Time out")
        except requests.exceptions.ConnectionError:
            print("Connection error")
        except requests.exceptions.RequestException:
            print("Exception request")
        return response

    # Pretty print JSON response exiting with a success if the response status code is the same as the 'success_status_code' argument
    def default_output(self, response, success_status_code):
        json_out = json.loads(response.text)
        pretty_json_out = json.dumps(json_out, indent=4)
        print(pretty_json_out)

        if response.status_code == success_status_code:  # Success
            exit(0)
        else:  # Failure
            exit(1)
