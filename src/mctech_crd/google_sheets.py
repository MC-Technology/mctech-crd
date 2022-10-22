from __future__ import print_function

import logging
import os.path
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
RANGE_NAME = "Sheet1"


class GoogleSheets:
    def __init__(self, config):
        self.credentials_file = config.get("credentials_file", "development")
        self.spreadsheet_id = config.get("sheet_id")
        self.debug = config.get("debug", False)
        if self.spreadsheet_id is None:
            raise Exception("Error: no spreadsheet id is configured")
        if self.debug:
            print("GoogleSheets API initialised")
        self.service = self.get_service()

    def __del__(self):
        logger.warning("GoogleSheets::__del__")
        self.service = None

    @lru_cache()
    def load_credentials(self):
        if self.debug:
            print("Google service account credentials loaded")
        script_dir = os.path.dirname(__file__)
        creds_rel_path = "../credentials/{}.json".format(self.credentials_file)
        creds_abs_path = os.path.normpath(os.path.join(script_dir, creds_rel_path))
        creds = None
        # https://cloud.google.com/docs/authentication/production#passing_code
        return service_account.Credentials.from_service_account_file(
            creds_abs_path, scopes=SCOPES
        )

    def get_service(self):
        creds = self.load_credentials()
        service = build("sheets", "v4", credentials=creds)
        return service

    def write_event(self, iso_time, serial_number, extra_fields):
        value_input_option = "RAW"
        insert_data_option = "INSERT_ROWS"

        values = [iso_time, serial_number]
        for key in extra_fields:
            values.append(extra_fields[key])

        body = {"values": [values]}
        try:
            service = self.get_service()
            request = (
                service.spreadsheets()
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
