from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import (
    ComplaintCategory,
    ComplaintPriority,
    ComplaintStatus,
    DueStatus,
    NoticeTargetType,
    PaymentStatus,
    UserRole,
    VisitorStatus,
)


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserRead(ORMModel):
    id: str
    name: str
    email: str
    role: UserRole
    is_active: bool


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class SocietyCreate(BaseModel):
    name: str
    address: str


class SocietyRead(ORMModel):
    id: str
    name: str
    address: str
    created_at: datetime
    updated_at: datetime


class BuildingCreate(BaseModel):
    society_id: str
    name: str


class BuildingRead(ORMModel):
    id: str
    society_id: str
    name: str
    created_at: datetime
    updated_at: datetime


class FlatCreate(BaseModel):
    society_id: str
    building_id: str
    flat_number: str
    floor_number: int
    maintenance_amount: Decimal


class FlatRead(ORMModel):
    id: str
    society_id: str
    building_id: str
    flat_number: str
    floor_number: int
    maintenance_amount: Decimal
    created_at: datetime
    updated_at: datetime


class ResidentCreate(BaseModel):
    user_id: str
    society_id: str
    flat_id: str
    phone: str
    is_owner: bool = False


class ResidentRead(ORMModel):
    id: str
    user_id: str
    society_id: str
    flat_id: str
    phone: str
    is_owner: bool
    created_at: datetime
    updated_at: datetime


class GenerateDuesRequest(BaseModel):
    society_id: str
    month: int
    year: int
    due_date: date


class GenerateDuesResponse(BaseModel):
    created: int
    skipped: int


class MaintenanceDueRead(ORMModel):
    id: str
    society_id: str
    flat_id: str
    month: int
    year: int
    amount: Decimal
    status: DueStatus
    due_date: date
    created_at: datetime
    updated_at: datetime


class PaymentRead(ORMModel):
    id: str
    maintenance_due_id: str
    submitted_by_user_id: str
    amount: Decimal
    proof_url: str
    transaction_reference: str | None
    status: PaymentStatus
    admin_note: str | None
    verified_by_user_id: str | None
    verified_at: datetime | None


class PaymentDecisionRequest(BaseModel):
    admin_note: str | None = None


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: ComplaintCategory
    priority: ComplaintPriority = ComplaintPriority.MEDIUM
    image_url: str | None = None


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    admin_note: str | None = None


class ComplaintRead(ORMModel):
    id: str
    society_id: str
    flat_id: str
    resident_id: str
    title: str
    description: str
    category: ComplaintCategory
    status: ComplaintStatus
    priority: ComplaintPriority
    image_url: str | None
    admin_note: str | None
    created_at: datetime
    updated_at: datetime


class NoticeCreate(BaseModel):
    society_id: str
    title: str
    body: str
    target_type: NoticeTargetType = NoticeTargetType.ALL
    building_id: str | None = None


class NoticeRead(ORMModel):
    id: str
    society_id: str
    title: str
    body: str
    target_type: NoticeTargetType
    building_id: str | None
    is_active: bool
    created_by: str
    created_at: datetime
    updated_at: datetime


class ExpectedVisitorCreate(BaseModel):
    visitor_name: str
    visitor_phone: str
    purpose: str
    vehicle_number: str | None = None
    visit_date: date


class WalkInVisitorCreate(BaseModel):
    flat_id: str
    visitor_name: str
    visitor_phone: str
    purpose: str
    vehicle_number: str | None = None
    visit_date: date | None = None


class VisitorRead(ORMModel):
    id: str
    society_id: str
    flat_id: str
    resident_id: str | None
    visitor_name: str
    visitor_phone: str
    purpose: str
    vehicle_number: str | None
    visit_date: date
    entry_time: datetime | None
    exit_time: datetime | None
    status: VisitorStatus
    created_by_user_id: str
    created_at: datetime
    updated_at: datetime


class AdminDashboard(BaseModel):
    total_flats: int
    total_residents: int
    current_month_paid_dues: int
    current_month_unpaid_dues: int
    open_complaints: int
    visitors_today: int


class ResidentDashboard(BaseModel):
    current_due: MaintenanceDueRead | None
    recent_complaints: list[ComplaintRead]
    recent_notices: list[NoticeRead]
    today_visitors: list[VisitorRead]


class SecurityDashboard(BaseModel):
    expected_visitors_today: list[VisitorRead]
    checked_in_visitors: list[VisitorRead]
