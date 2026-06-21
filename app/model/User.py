import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, text, tinyint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.model.Organization import Organization

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    ),
    
    name: Mapped[str] = mapped_column(String(255), nullable=False),
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False),
    # email_verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False),
    
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True),
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True),
    role: Mapped[str] = mapped_column(String(50), server_default="staff"),
    status: Mapped[bool] = mapped_column(tinyint, server_default=text("1")),
    
    description: Mapped[str | None] = mapped_column(String(200), nullable=True),
    profile_photo: Mapped[str | None] = mapped_column(String(255), nullable=True),
    remember_token: Mapped[str | None] = mapped_column(String(100), nullable=True),

   
    organization_id: Mapped[str | None] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="SET NULL"), 
        nullable=True
    ),


    

    # Timestamps & Soft Delete
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP")),
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    ),
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True),

    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="users")