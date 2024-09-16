from datetime import datetime
import json
import sys
import argparse
from tabulate import tabulate
from rich_argparse import RichHelpFormatter
from defectdojo_cli2.util import Util
from defectdojo_cli2.EnvDefaults import EnvDefaults

class Announcements(object):
    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description="Perform <sub_command> related to announcements on DefectDojo",
            usage="""defectdojo announcements <sub_command> [<args>]

    You can use the following sub_commands:
        create          Create an announcement
        delete          Delete an announcement
        list            List announcements
        update          Update an announcement
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

    def create(
        self,
        url,
        api_key,
        dismissable=None,
        message=None,
        style=None,
        **kwargs,
    ):
        request_json = dict()
        API_URL = url + "/api/v2"
        ANNOUNCMENTS_URL = API_URL + "/announcements/"
        if dismissable is not None:
            request_json["dismissable"] = dismissable
        if message is not None:
            request_json["message"] = message
        if style is not None:
            request_json["style"] = style
        request_json = json.dumps(request_json)
        response = Util().request_apiv2(
            "POST", ANNOUNCMENTS_URL, api_key, data=request_json
        )
        return response

    def _create(self):
        # Read user-supplied arguments
        parser = argparse.ArgumentParser(
            description="Create an announcement",
            usage="defectdojo announcements create [<args>]",
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
            "--message",
            help="What to display",
            required=True,
        )
        optional.add_argument(
            "--dismissable",
            help="Set as dismissable",
            action="store_true",
        )
        optional.add_argument(
            "--style",
            help="Style (info, success, warning, danger)",
            choices=["info", "success", "warning", "danger"],
        )

        parser._action_groups.append(optional)
        # Parse out arguments ignoring the first three (because we're inside a sub-command)
        args = vars(parser.parse_args((sys.argv[3:])))

        response = self.create(**args)

        json_out = json.loads(response.text)
        if response.status_code == 201:
                pretty_json_out = json.dumps(json_out, indent=4)
                print(pretty_json_out)
                sys.exit(0)
        else:
            pretty_json_out = json.dumps(json_out, indent=4)
            print(pretty_json_out)
            sys.exit(1)


    def list(
        self,
        url,
        api_key,
        dismissable=None,
        limit=None,
        message=None,
        offset=None,
        style=None,
        **kwargs,
    ):
        request_params = dict()
        API_URL = url + "/api/v2"
        ANNOUNCMENTS_URL = API_URL + "/announcements/"
        if dismissable is not None:
            request_params["dismissable"] = dismissable
        if limit is not None:
            request_params["limit"] = limit
        if message is not None:
            request_params["message"] = message
        if offset is not None:
            request_params["offset"] = offset
        if style is not None:
            request_params["style"] = style

        else:
            # Make a request to API getting only one finding to retrieve the total amount of findings
            temp_params = request_params.copy()
            temp_params["url"] = url
            temp_params["api_key"] = api_key
            temp_params["limit"] = 1
            temp_response = self.list(**temp_params)
            limit = int(json.loads(temp_response.text)["count"])
            request_params["limit"] = limit

        # Make request
        response = Util().request_apiv2(
            "GET", ANNOUNCMENTS_URL, api_key, params=request_params
        )
        return response

    def _list(self):
        # Read user-supplied arguments
        parser = argparse.ArgumentParser(
            description="List announcements in DefectDojo",
            usage="defectdojo announcements list [<args>]",
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
        optional.add_argument(
            "--dismissable",
            help="Get dismissable announcements",
            action="store_true",
            dest="active",
        )

        optional.add_argument(
            "--json",
            help="Print output in JSON format",
            action="store_true",
            default=False,
        )
        optional.add_argument(
            "--limit",
            help="Number of results to return (default: all)",
        )
        optional.add_argument(
            "--offset",
            help="The initial index from which to return the results "
            + "(not needed if the --limit flag is not set)",
        )
        optional.add_argument(
            "--message",
            help="Number of results to return (by default it gets all the findings)",
        )
        optional.add_argument(
            "--style",
            help="Style of announcement",
            default="",
            choices=["info", "success", "warning", "danger"],
        )

        parser._action_groups.append(optional)
        # Parse out arguments ignoring the first three (because we're inside a sub-command)
        args = vars(parser.parse_args((sys.argv[3:])))

        response = self.list(**args)

        json_out = json.loads(response.text)
        if response.status_code == 200:
            if args["json"] is True:
                pretty_json_out = json.dumps(json_out, indent=4)
                print(pretty_json_out)
            else:
                announcements_amount = json_out["count"]
                print("\nAnnouncements amount: " + str(json_out["count"]))
                if announcements_amount > 0:
                    table = dict()
                    table["id"] = list()
                    table["message"] = list()
                    table["style"] = list()
                    table["dismissable"] = list()
                    for announcement in json_out["results"]:
                      table["id"].append(announcement["id"])
                      table["message"].append(announcement["message"])
                      table["style"].append(announcement["style"])
                      table["dismissable"].append(announcement["dismissable"])
                      print(tabulate(table, headers="keys", tablefmt="pretty", maxcolwidths=[None, 40]))
                else:
                    sys.exit()
        else:
            pretty_json_out = json.dumps(json_out, indent=4)
            print(pretty_json_out)
            sys.exit(1)

    def delete(
        self,
        url,
        api_key,
        id,
        **kwargs,
    ):
        API_URL = url + "/api/v2"
        ANNOUNCMENTS_URL = API_URL + "/announcements/" + id
        response = Util().request_apiv2(
            "DELETE", ANNOUNCMENTS_URL, api_key
        )
        return response

    def _delete(self):
        parser = argparse.ArgumentParser(
            description="Delete an announcement",
            usage="defectdojo announcements delete [<args>]",
            formatter_class=RichHelpFormatter,
        )
        parser.add_argument(
            "--id",
            help="Id of announcement to delete)",
            required=True,
        )
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
        # This is a sub-command, ignore first three
        args = vars(parser.parse_args((sys.argv[3:])))

        response = self.delete(**args)
        if response.status_code == 204:
            print(json.dumps({"status": "success"}, indent=4))
            sys.exit()
        else:
            print(json.dumps({"status": "error"}, indent=4))
            sys.exit(1)
