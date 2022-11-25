from __future__ import print_function

import logging
import os
import pickle
from functools import lru_cache

import httplib2
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from googleapiclient.discovery import build


logger = logging.getLogger()

# If modifying these scopes, delete the file token.pickle.
# https://developers.google.com/identity/protocols/oauth2/scopes#sheets
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SCOPES = ["https://www.googleapis.com/auth/drive"]
RANGE_NAME = "Sheet1!A:A"
CREDENTIALS_FILE = "~/.cosmic/credentials/google_api.json"


class GoogleSheets:
    def __init__(self, config):
        self.credentials_file = config.get("credentials_file", None)
        self.spreadsheet_id = config.get("sheet_id")
        if self.spreadsheet_id is None:
            raise Exception("Error: no spreadsheet id is configured")

        logger.info("GoogleSheets API initialised")
        logger.info(f"Logging to sheet: {self.spreadsheet_id}")

        self.service = self.get_service()

    def __del__(self):
        logger.warning("GoogleSheets::__del__")
        self.service = None

    @lru_cache()
    def load_credentials(self):
        # Get google service account from home directory
        key_file = os.path.expanduser(CREDENTIALS_FILE)
        if os.path.exists(key_file):
            # https://cloud.google.com/docs/authentication/production#passing_code
            return service_account.Credentials.from_service_account_file(
                key_file, scopes=SCOPES
            )

    def get_service(self):
        if creds := self.load_credentials():
            return build("sheets", "v4", credentials=creds)
        return None

    def write_event(self, iso_time, serial_number, extra_fields):
        if not self.service:
            logger.warning(
                "GoogleSheets - no service provided (likely missing credentials)"
            )
            return

        value_input_option = "RAW"
        insert_data_option = "INSERT_ROWS"

        values = [iso_time, serial_number]
        for key in extra_fields:
            values.append(extra_fields[key])

        body = {"values": [values]}
        try:
            request = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=self.spreadsheet_id,
                    range=RANGE_NAME,
                    valueInputOption=value_input_option,
                    insertDataOption=insert_data_option,
                    body=body,
                )
            )
            result = request.execute()

            if self.debug:
                print(
                    "GoogleSheets: {0} cells updated.".format(
                        result.get("updates").get("updatedCells")
                    )
                )
        except Exception as e:
            logger.warning("GoogleSheets::write_event failed {}".format(e))
