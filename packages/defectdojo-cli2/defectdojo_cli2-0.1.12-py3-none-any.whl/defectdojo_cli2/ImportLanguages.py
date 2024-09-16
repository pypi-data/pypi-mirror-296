from datetime import datetime
import sys
import argparse
from tabulate import tabulate
from rich_argparse import RichHelpFormatter
from defectdojo_cli2.util import Util
from defectdojo_cli2.EnvDefaults import EnvDefaults

class ImportLanguages(object):
    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description="Perform <sub_command> related to announcements on DefectDojo",
            usage="""defectdojo announcements <sub_command> [<args>]

    You can use the following sub_commands:
        upload            Upload
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

    def upload(
        self,
        url,
        api_key,
        product_id,
        file,
        **kwargs,
    ):
        API_URL = url + "/api/v2"
        API_TOKEN_URL = API_URL + "/import-languages/"
        files = {
          'file': open(file, 'rb')
        }
        payload = {'product': product_id}
        response = Util().request_apiv2(
            "POST", API_TOKEN_URL, api_key, data=payload, files=files
        )
        return response

    def _upload(self):
        # Read user-supplied arguments
        parser = argparse.ArgumentParser(
            description="Upload Languages",
            usage="defectdojo import_languages upload [<args>]",
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
            "--product_id",
            action=EnvDefaults,
            envvar="DEFECTDOJO_PRODUCT_ID",
            help="Product id",
            required=True,
        )
        required.add_argument(
            "--file",
            action=EnvDefaults,
            envvar="DEFECTDOJO_LANGUAGES_FILE",
            help="File with languages",
            required=True,
        )

        parser._action_groups.append(optional)
        # Parse out arguments ignoring the first three (because we're inside a sub-command)
        args = vars(parser.parse_args((sys.argv[3:])))

        response = self.upload(**args)

        if response.status_code == 201:
            print("File uploaded")
            sys.exit(0)
