from datetime import datetime
import sys
import argparse
from tabulate import tabulate
from rich_argparse import RichHelpFormatter
from defectdojo_cli2.util import Util
from defectdojo_cli2.EnvDefaults import EnvDefaults

class ReImportScan(object):
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
        product_name,
        engagement_name,
        scan_type,
        test_title,
        file,
        active=None,
        verified=None,
        push_to_jira=None,
        branch_tag=None,
        commit_hash=None,
        **kwargs,
    ):
        API_URL = url + "/api/v2"
        API_TOKEN_URL = API_URL + "/reimport-scan/"
        files = {
          'file': open(file, 'rb')
        }
        payload = {'product_name': product_name,
                   'engagement_name': engagement_name,
                   'scan_type': scan_type,
                   'active': active,
                   'verified': verified,
                   'test_title': test_title,
                   'auto_create_context': True,
        }
        if push_to_jira is not None:
            payload["push_to_jira"] = push_to_jira
        if branch_tag is not None:
            payload["branch_tag"] = branch_tag
        if commit_hash is not None:
            payload["commit_hash"] = commit_hash

        response = Util().request_apiv2(
            "POST", API_TOKEN_URL, api_key, data=payload, files=files
        )
        return response

    def _upload(self):
        # Read user-supplied arguments
        parser = argparse.ArgumentParser(
            description="Reimport scan",
            usage="defectdojo reimport_scan upload [<args>]",
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
            "--product_name",
            action=EnvDefaults,
            envvar="DEFECTDOJO_PRODUCT_NAME",
            help="Product name",
            required=True,
        )
        required.add_argument(
            "--engagement_name",
            action=EnvDefaults,
            envvar="DEFECTDOJO_ENGAGEMENT_NAME",
            help="Engagement name",
            required=True,
        )
        required.add_argument(
            "--scan_type",
            action=EnvDefaults,
            envvar="DEFECTDOJO_SCAN_TYPE",
            help="Scan type",
            required=True,
        )
        required.add_argument(
            "--test_title",
            action=EnvDefaults,
            envvar="DEFECTDOJO_TEST_TITLE",
            help="Test title",
            required=True,
        )
        required.add_argument(
            "--file",
            action=EnvDefaults,
            envvar="DEFECTDOJO_LANGUAGES_FILE",
            help="File with languages",
            required=True,
        )
        optional.add_argument(
            "--verified",
            help="Mark vulnerabilities found as verified",
            action="store_true",
            dest="verified",
        )
        optional.add_argument(
            "--unverified",
            help="Mark vulnerabilities found as unverified (default)",
            action="store_false",
            dest="verified",
        )
        optional.add_argument(
            "--active",
            help="Mark vulnerabilities found as active (default)",
            action="store_true",
            dest="active",
        )
        optional.add_argument(
            "--inactive",
            help="Mark vulnerabilities found as inactive",
            action="store_false",
            dest="active",
        )
        optional.add_argument(
            "--branch_tag",
            action=EnvDefaults,
            envvar="DEFECTDOJO_BRANCH_TAG",
            help="Branch or tag",
            required=False,
        )
        optional.add_argument(
            "--commit_hash",
            action=EnvDefaults,
            envvar="DEFECTDOJO_COMMIT_HASH",
            help="Git commit hash",
            required=False,
        )

        optional.set_defaults(active=True, verified=False, push_to_jira=False)
        optional.add_argument(
            "--push_to_jira",
            help="push to Jira",
            action="store_true",
            dest="push_to_jira",
        )

        parser._action_groups.append(optional)
        # Parse out arguments ignoring the first three (because we're inside a sub-command)
        args = vars(parser.parse_args((sys.argv[3:])))

        response = self.upload(**args)

        if response.status_code == 201:
            print("Test uploaded")
            sys.exit(0)
