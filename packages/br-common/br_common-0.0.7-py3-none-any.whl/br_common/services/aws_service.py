import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
import logging
from br_common.enums import ErrorMessages
from br_common.utils import CoreUtils

# https://aws.amazon.com/developer/language/python/

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class SecretManagerService:
    """
    Service class to interact with AWS Secrets Manager.
    """

    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def get_secret(self, secret_name: str):
        """
        Retrieve a secret value from AWS Secrets Manager.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            if "SecretString" in response:
                return response["SecretString"]
            else:
                return response["SecretBinary"]
        except ClientError as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_SECRET_EXCEPTION.name,
                    ErrorMessages.AWS_SECRET_EXCEPTION.value
                ),
            )


class SESService:
    """
    Service class to interact with AWS Simple Email Service (SES) for sending emails.
    """

    def __init__(self):
        """
        Initialize the SES client.
        """
        self.client = boto3.client("ses")

    def send_email(
        self,
        sender: str,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: str = None,
    ):
        """
        Sends an email using Amazon SES.

        :param sender: Email address of the sender.
        :param recipient: Email address of the recipient.
        :param subject: Subject of the email.
        :param body_text: Text version of the email body.
        :param body_html: Optional HTML version of the email body.
        """
        try:
            # Construct the email payload
            message = {
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Text": {"Data": body_text, "Charset": "UTF-8"}},
            }

            # If HTML body is provided, add it to the message
            if body_html:
                message["Body"]["Html"] = {"Data": body_html, "Charset": "UTF-8"}

            # Send the email using SES
            response = self.client.send_email(
                Source=sender,
                Destination={
                    "ToAddresses": [recipient],
                },
                Message=message,
            )

            logger.info(f"Email sent successfully to {recipient}: {response}")
            return response

        except ClientError as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.EMAIL_SEND_EXCEPTION.name,
                    ErrorMessages.EMAIL_SEND_EXCEPTION.value
                ),
            )
