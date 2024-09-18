from br_common.models import BaseModel
from sqlalchemy import Column, String


class SalesOffice(BaseModel):
    __tablename__ = "sales_offices"

    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<SalesOffice: [{self.name if self.name else 'Unsaved'}]>"
