from datetime import datetime
import json
import sys
import argparse
from tabulate import tabulate
from rich_argparse import RichHelpFormatter
from defectdojo_cli2.util import Util
from defectdojo_cli2.EnvDefaults import EnvDefaults

class ApiToken(object):
    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description="Perform <sub_command> related to announcements on DefectDojo",
            usage="""defectdojo announcements <sub_command> [<args>]

    You can use the following sub_commands:
        get            Get API key
""",
            formatter_class=RichHelpFormatter,
        )
        parser.add_argument("sub_command", help="Sub_command to run")
        # Get sub_command
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, "_" + args.sub_command):
            print("Unrecognized sub_command " + args.sub_command)
            parser.print_help()
            sys.exit(1)
        # Use dispatch pattern to invoke method with same name (that starts with _)
        getattr(self, "_" + args.sub_command)()

    def get(
        self,
        url,
        username,
        password,
        api_key,
        **kwargs,
    ):
        request_json = dict()
        API_URL = url + "/api/v2"
        API_TOKEN_URL = API_URL + "/api-token-auth/"
        request_json["username"] = username
        request_json["password"] = password
        request_json = json.dumps(request_json)
        response = Util().request_apiv2(
            "POST", API_TOKEN_URL, api_key, data=request_json
        )
        return response

    def _get(self):
        # Read user-supplied arguments
        parser = argparse.ArgumentParser(
            description="Get API key",
            usage="defectdojo api_token get [<args>]",
            formatter_class=RichHelpFormatter,
        )
        optional = parser._action_groups.pop()
        required = parser.add_argument_group("required arguments")
        required.add_argument(
            "--url",
            action=EnvDefaults,
            envvar="DEFECTDOJO_URL",
            help="DefectDojo URL",
            required=True,
        )
        required.add_argument(
            "--api_key",
            action=EnvDefaults,
            envvar="DEFECTDOJO_API_KEY",
            help="API v2 Key",
            required=True,
        )
        required.add_argument(
            "--username",
            action=EnvDefaults,
            envvar="DEFECTDOJO_USER_NAME",
            help="Username",
            required=True,
        )
        required.add_argument(
            "--password",
            action=EnvDefaults,
            envvar="DEFECTDOJO_PASSWORD",
            help="Password",
            required=True,
        )

        optional.add_argument(
            "--json",
            help="Print output in JSON format",
            action="store_true",
            default=False,
        )

        parser._action_groups.append(optional)
        # Parse out arguments ignoring the first three (because we're inside a sub-command)
        args = vars(parser.parse_args((sys.argv[3:])))

        response = self.get(**args)

        json_out = json.loads(response.text)
        if response.status_code == 200:
            if args["json"] is True:
                pretty_json_out = json.dumps(json_out, indent=4)
                print(pretty_json_out)
            else:
                print(json_out)
                sys.exit(1)
