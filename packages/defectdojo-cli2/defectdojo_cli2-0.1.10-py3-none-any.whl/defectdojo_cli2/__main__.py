import sys
import argparse
from rich_argparse import RichHelpFormatter
from defectdojo_cli2 import Findings
from defectdojo_cli2 import Engagements
from defectdojo_cli2 import Tests
from defectdojo_cli2 import Announcements
from defectdojo_cli2 import ApiToken
from defectdojo_cli2 import ImportLanguages
from defectdojo_cli2 import ReImportScan
from defectdojo_cli2 import __version__


# Multilevel argparse based on https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class DefectDojoCLI(object):
    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description="CLI wrapper for DefectDojo using APIv2",
            usage="""defectdojo <command> [<args>]

    You can use the following commands:
            announcements     Operations related to Announcements (announcements --help for more details)
            api_token         Operations related to API token auth (api-token-auth --help for more details)
            findings          Operations related to findings (findings --help for more details)
            engagements       Operations related to engagements (engagements --help for more details)
            tests             Operations related to tests (tests --help for more details)
            import_languages  Operations related to import languages (import_languages --help for more details)
            reimport_scan     Operations related to reimport scans (reimport_scan --help for more details)
        """,
            formatter_class=RichHelpFormatter,
        )
        parser.add_argument("command", help="Command to run")
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s_cli v" + __version__
        )
        # Parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, "_" + args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # Use dispatch pattern to invoke method with same name (that starts with _)
        getattr(self, "_" + args.command)()

    def _announcements(self):
        Announcements().parse_cli_args()

    def _findings(self):
        Findings().parse_cli_args()

    def _engagements(self):
        Engagements().parse_cli_args()

    def _api_token(self):
        ApiToken().parse_cli_args()

    def _import_languages(self):
        ImportLanguages().parse_cli_args()

    def _reimport_scan(self):
        ReImportScan().parse_cli_args()

    def _tests(self):
        Tests().parse_cli_args()


def main():
    DefectDojoCLI().parse_cli_args()


if __name__ == "__main__":
    main()
