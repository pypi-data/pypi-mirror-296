from br_common.models import BaseModel
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship


class Auth(BaseModel):
    __tablename__ = "auth"

    emp_id = Column(String(10), ForeignKey("hr_master.emp_id"), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    mfa_secret = Column(String(40), nullable=True)

    otp_sessions = relationship("OtpSession", back_populates="auth")

    def __repr__(self):
        return f"<Auth: [{self.id if self.id else 'Unsaved'}]>"


class OtpSession(BaseModel):
    __tablename__ = "otp_sessions"

    otp = Column(String(255), nullable=False)
    attempts = Column(Integer, default=0)
    otp_expires_at = Column(DateTime, nullable=False)
    emp_id = Column(String(10), ForeignKey("hr_master.emp_id"), nullable=False)

    auth = relationship("Auth", back_populates="otp_sessions")

    def __repr__(self):
        return f"<OtpSession: [{self.id if self.id else 'Unsaved'}]>"
