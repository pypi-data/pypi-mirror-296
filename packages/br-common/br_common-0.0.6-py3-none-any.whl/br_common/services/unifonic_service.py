import requests
import logging
import json
from fastapi import HTTPException, status
from br_common.services.aws_service import SecretManagerService
from br_common.enums import ErrorMessages
from br_common.utils import CoreUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifonicService:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.secret_manager = SecretManagerService()
        self.api_key = None
        self.sender_id = None
        return self.get_unifonic_secrets()

    def get_unifonic_secrets(self):
        secret_data = self.secret_manager.get_secret("UNIFONIC")
        secret_data = json.loads(secret_data)
        self.api_key = secret_data.get("UNIFONIC_API_KEY")
        self.sender_id = secret_data.get("UNIFONIC_SENDER_ID")

    def send_sms(self, phone_number: str, message_body: str):
        payload = {
            "AppSid": self.api_key,
            "SenderID": self.sender_id,
            "Recipient": phone_number,
            "Body": message_body,
            "responseType": "JSON",
            "statusCallback": "sent",
            "async": False,
        }

        try:
            # Make the request to Unifonic with a timeout
            response = requests.post(self.base_url, data=payload, timeout=self.timeout)

            response_data = response.json()

            # Check for success in the response
            if response.status_code != 200 or not response_data.get("success"):
                logger.error(
                    ErrorMessages.UNIFONIC_EXCEPTION.value.format(
                        response_data.get("message", "Unknown error")
                    )
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=CoreUtils.format_error_response(
                        ErrorMessages.UNIFONIC_EXCEPTION.name,
                        ErrorMessages.UNIFONIC_EXCEPTION.value.format(
                            response_data.get("message", "Unknown error")
                        ),
                    ),
                )

            logger.info(f"OTP sent successfully to {phone_number}")
            return True

        except requests.Timeout:
            logger.error("Request to Unifonic timed out.")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.UNIFONIC_REQUEST_TIMEOUT.name,
                    ErrorMessages.UNIFONIC_REQUEST_TIMEOUT.value,
                ),
            )

        except requests.RequestException as e:
            logger.error(f"Request to Unifonic failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.UNKNOWN.name, ErrorMessages.UNKNOWN.value
                ),
            )
