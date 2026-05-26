"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-26
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("ADMIN", "RESIDENT", "SECURITY", name="userrole"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "societies",
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "buildings",
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("society_id", "name", name="uq_building_society_name"),
    )
    op.create_table(
        "flats",
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("building_id", sa.String(length=36), nullable=False),
        sa.Column("flat_number", sa.String(length=40), nullable=False),
        sa.Column("floor_number", sa.Integer(), nullable=False),
        sa.Column("maintenance_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"]),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("building_id", "flat_number", name="uq_flat_building_number"),
    )
    op.create_table(
        "residents",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("flat_id", sa.String(length=36), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("is_owner", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["flat_id"], ["flats.id"]),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "maintenance_dues",
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("flat_id", sa.String(length=36), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("status", sa.Enum("UNPAID", "PAYMENT_SUBMITTED", "PAID", "REJECTED", name="duestatus"), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["flat_id"], ["flats.id"]),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("flat_id", "month", "year", name="uq_due_flat_month_year"),
    )
    op.create_table(
        "payments",
        sa.Column("maintenance_due_id", sa.String(length=36), nullable=False),
        sa.Column("submitted_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("proof_url", sa.String(length=500), nullable=False),
        sa.Column("transaction_reference", sa.String(length=120), nullable=True),
        sa.Column("status", sa.Enum("SUBMITTED", "APPROVED", "REJECTED", name="paymentstatus"), nullable=False),
        sa.Column("admin_note", sa.Text(), nullable=True),
        sa.Column("verified_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["maintenance_due_id"], ["maintenance_dues.id"]),
        sa.ForeignKeyConstraint(["submitted_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["verified_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "complaints",
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("flat_id", sa.String(length=36), nullable=False),
        sa.Column("resident_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.Enum("PLUMBING", "ELECTRICAL", "LIFT", "CLEANING", "PARKING", "SECURITY", "OTHER", name="complaintcategory"), nullable=False),
        sa.Column("status", sa.Enum("OPEN", "IN_PROGRESS", "RESOLVED", "REJECTED", name="complaintstatus"), nullable=False),
        sa.Column("priority", sa.Enum("LOW", "MEDIUM", "HIGH", name="complaintpriority"), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("admin_note", sa.Text(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["flat_id"], ["flats.id"]),
        sa.ForeignKeyConstraint(["resident_id"], ["residents.id"]),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "notices",
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("target_type", sa.Enum("ALL", "BUILDING", name="noticetargettype"), nullable=False),
        sa.Column("building_id", sa.String(length=36), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "visitors",
        sa.Column("society_id", sa.String(length=36), nullable=False),
        sa.Column("flat_id", sa.String(length=36), nullable=False),
        sa.Column("resident_id", sa.String(length=36), nullable=True),
        sa.Column("visitor_name", sa.String(length=120), nullable=False),
        sa.Column("visitor_phone", sa.String(length=30), nullable=False),
        sa.Column("purpose", sa.String(length=200), nullable=False),
        sa.Column("vehicle_number", sa.String(length=40), nullable=True),
        sa.Column("visit_date", sa.Date(), nullable=False),
        sa.Column("entry_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("exit_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.Enum("EXPECTED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED", name="visitorstatus"), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["flat_id"], ["flats.id"]),
        sa.ForeignKeyConstraint(["resident_id"], ["residents.id"]),
        sa.ForeignKeyConstraint(["society_id"], ["societies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    for table in [
        "visitors",
        "notices",
        "complaints",
        "payments",
        "maintenance_dues",
        "residents",
        "flats",
        "buildings",
        "societies",
        "users",
    ]:
        op.drop_table(table)
