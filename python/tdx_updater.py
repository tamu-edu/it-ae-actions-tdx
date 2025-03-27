import argparse
import os
from pprint import pprint
import requests

import logging
import http.client

logging.basicConfig(level=logging.DEBUG)

httpclient_logger = logging.getLogger("http.client")

def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework"""

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1

httpclient_logging_patch()


class TDxUpdater:
    def __init__(self, base_url: str, account_id: str, secret: str, flow_id: str, flow_version: str) -> None:
        self._base_url = base_url
        self._account_id = account_id
        self._secret = secret
        self._flow_id = flow_id
        self._flow_version = flow_version

    def _get_auth_header(self) -> dict:
        return {
            "X-TdxiPaaS-AccountId": self._account_id,
            "X-TdxiPaaS-Secret": self._secret,
        }
    
    def _get_flow_url(self) -> str:
        return f"{self._base_url}/start/{self._flow_id}?flowVersion={self._flow_version}"

    def add_request_comment(self, request_id: str, comment: str) -> None:
        pass

    def close_request(
        self, request_id: str, variable_name: str = None, variable_value: str = None
    ) -> None:
        data = {"ticket_number": int(request_id)}
        if variable_name and variable_value:
            data[variable_name] = variable_value
        r = requests.post(headers=self._get_auth_header(), json=data, url=self._get_flow_url())

        if r.status_code != 200:
            raise ValueError(f"Failed to close request: {r.status_code}: {r.reason} ({r.text})")
        else:
            print(f"Request {request_id} closed successfully")


def main():

    assert "TDX_BASE_URL" in os.environ, "TDX_BASE_URL not set (format: https://us1.teamdynamix.com/tdapp/app/flow/api/v1)"
    assert "TDX_ACCOUNT_ID" in os.environ, "TDX_ACCOUNT_ID not set (format: c4a4f617-0510-4dcb-af07-5ae296c858d0)"
    assert "TDX_SECRET" in os.environ, "TDX_SECRET not set"

    parser = argparse.ArgumentParser()

    parser.add_argument("--request_id", help="ServiceNow request ID", required=True)
    parser.add_argument("--flow_id", help="Flow ID", required=True)
    parser.add_argument("--flow_version", help="Flow Version", required=True)
    subparsers = parser.add_subparsers(help="Action to perform")
    group_comment_and_notify = subparsers.add_parser(
        "add_comment_and_notify", help="Add comment to request and notify user"
    )
    group_comment_and_notify.add_argument(
        "--comment", help="Comment to add to request", required=False
    )
    group_update_variable_and_close = subparsers.add_parser(
        "update_request_variable_and_close_request",
        help="Update request variable and close request",
    )
    group_update_variable_and_close.add_argument(
        "--variable_name", help="Variable name to update", required=True
    )
    group_update_variable_and_close.add_argument(
        "--variable_value", help="Variable value to update", required=True
    )

    group_close_request = subparsers.add_parser("close_request", help="Close request")
    group_close_request.add_argument(
        "--close", help="Close request", action="store_true"
    )

    args = parser.parse_args()

    tdx_updater = TDxUpdater(
        base_url=os.environ["TDX_BASE_URL"],
        account_id=os.environ["TDX_ACCOUNT_ID"],
        secret=os.environ["TDX_SECRET"],
        flow_id=args.flow_id,
        flow_version=args.flow_version
    )

    if "add_comment_and_notify" in args:
        tdx_updater.add_request_comment(args.request_id, args.comment)
    elif "variable_name" in args and "variable_value" in args:
        tdx_updater.close_request(
            args.request_id, args.variable_name, args.variable_value
        )
    elif "close" in args:
        tdx_updater.close_request(args.request_id)
    else:
        raise ValueError("No action specified")


if __name__ == "__main__":
    main()
