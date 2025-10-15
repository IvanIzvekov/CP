import uuid

from sqlalchemy import UUID, Column, ForeignKey, String

from app.core.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False
    )
