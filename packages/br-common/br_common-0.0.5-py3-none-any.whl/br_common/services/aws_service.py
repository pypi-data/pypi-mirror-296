import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
import logging
from br_common.enums import ErrorMessages

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
                detail=ErrorMessages.AWS_SECRET_EXCEPTION.value,
            )
