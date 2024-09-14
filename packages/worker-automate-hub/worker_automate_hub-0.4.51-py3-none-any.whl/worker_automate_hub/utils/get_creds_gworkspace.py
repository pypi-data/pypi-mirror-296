import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from worker_automate_hub.api.client import sync_get_config_by_name


def save_to_json(file_name: str, data: dict) -> Path:
    file_path = Path(f"./{file_name}.json")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    return file_path


def get_token_gcp_path() -> Path:
    get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
    return save_to_json("gcp_token", get_gcp_token["conConfiguracao"])


def get_credentials_gcp_path() -> Path:
    get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
    return save_to_json("gcp_credentials", get_gcp_credentials["conConfiguracao"])


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://mail.google.com/",
]


class GetCredsGworkspace:
    def get_creds_gworkspace(self):
        creds = None
        gcp_token = get_token_gcp_path()
        gcp_credentials = get_credentials_gcp_path()

        try:
            creds = Credentials.from_authorized_user_file(
                gcp_token,
                SCOPES,
            )

        except Exception as e:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        gcp_credentials,
                        SCOPES,
                    )

                    creds = flow.run_local_server(port=0)
                with open(
                    gcp_token,
                    "w",
                ) as token:

                    token.write(creds.to_json())

        return creds
