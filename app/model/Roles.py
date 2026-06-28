import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, text, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("user_id", String(36), ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE")),
)

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE")),
    Column("permission_id", String(36), ForeignKey("permissions.id", ondelete="CASCADE")),
)


class Roles(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(255),
        index = True,
        unique=True
    )
 
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    permissions: Mapped[list["Permissions"]] = relationship(
        "Permissions",
        secondary="roles_permissions",
        back_populates="roles",
    )
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
    )


class Permissions(Base):
    __tablename__ = "permissions"
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    permission: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        index = True,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    roles: Mapped[list["Roles"]] = relationship(
        "Roles",
        secondary="roles_permissions",
        back_populates="permissions",
    )