from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from br_common.features.auth.models import OtpSession
from fastapi import HTTPException, status
from br_common.features.employee.models import HRMaster, EmployeeAuditLog
from datetime import datetime, timedelta
from br_common.enums import ErrorMessages, LogEvents, SuccessMessages
import jwt
from fastapi.security import OAuth2PasswordBearer


class CoreUtils:
    def __init__(self, settings):
        """Initialize CoreUtils with settings"""
        self.settings = settings
        self.cipher = Fernet(self.settings.SECRET_KEY.encode())
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def format_error_response(error_type, message):
        return {"error_type": error_type, "message": message}

    def encrypt(self, data: str):
        """Encrypt the data"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, data: str):
        """Decrypt the data"""
        return self.cipher.decrypt(data.encode()).decode()

    def verify_otp(
        self, user: HRMaster, otp: str, db: Session, latitude: float, longitude: float
    ):
        """Verify user-entered OTP"""
        otp_session = (
            db.query(OtpSession)
            .filter(OtpSession.emp_id == user.emp_id)
            .order_by(OtpSession.created_at.desc())
            .first()
        )

        if not otp_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessages.NOT_FOUND.value.format("OTP session"),
            )

        # Decrypt the OTP
        decrypted_otp = self.decrypt(otp_session.otp)  # Use self.decrypt

        if decrypted_otp != otp:
            EmployeeAuditLog.create(
                db=db,
                emp_id=user.emp_id,
                event_type=LogEvents.INVALID_OTP.value,
                context={
                    "OTP": otp,
                    "message": ErrorMessages.INVALID_OTP.value,
                },
                latitude=latitude,
                longitude=longitude,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.INVALID_OTP.value,
            )

        if otp_session.otp_expires_at < datetime.now():
            EmployeeAuditLog.create(
                db=db,
                emp_id=user.emp_id,
                event_type=LogEvents.OTP_EXPIRED.value,
                context={
                    "OTP": otp,
                    "message": ErrorMessages.OTP_EXPIRED.value,
                },
                latitude=latitude,
                longitude=longitude,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.OTP_EXPIRED.value,
            )

        # Mark otp as expired once verified so next time user has to generate new otp.
        otp_session.otp_expires_at = datetime.now() - timedelta(
            minutes=self.settings.OTP_VALIDITY + 1
        )

        # Once verified reset otp attempts
        otp_session.attempts = 0
        otp_session.save(db)

        EmployeeAuditLog.create(
            db=db,
            emp_id=user.emp_id,
            event_type=LogEvents.OTP_VERIFIED.value,
            context={
                "OTP": otp,
                "message": SuccessMessages.OTP_VERIFIED.value,
            },
            latitude=latitude,
            longitude=longitude,
        )

        return True

    def create_access_token(self, data: dict):
        """Generate JWT user access token"""
        to_encode = data.copy()
        expire = datetime.now() + timedelta(
            minutes=self.settings.JWT_EXPIRATION_MINUTES
        )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=self.settings.SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM,
        )
        return encoded_jwt
