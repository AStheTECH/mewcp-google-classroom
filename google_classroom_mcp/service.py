import logging

from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger("google-classroom-mcp-server")


def get_service():
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    logger.info("Creating Google Classroom API service with provided access token")
    creds = Credentials(token=cred.access_token, scopes=cred.scopes)
    service = build("classroom", "v1", credentials=creds)
    logger.info("Google Classroom API service created successfully")
    return service
