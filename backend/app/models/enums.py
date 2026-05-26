from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    RESIDENT = "RESIDENT"
    SECURITY = "SECURITY"


class DueStatus(str, Enum):
    UNPAID = "UNPAID"
    PAYMENT_SUBMITTED = "PAYMENT_SUBMITTED"
    PAID = "PAID"
    REJECTED = "REJECTED"


class PaymentStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ComplaintCategory(str, Enum):
    PLUMBING = "PLUMBING"
    ELECTRICAL = "ELECTRICAL"
    LIFT = "LIFT"
    CLEANING = "CLEANING"
    PARKING = "PARKING"
    SECURITY = "SECURITY"
    OTHER = "OTHER"


class ComplaintStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


class ComplaintPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class NoticeTargetType(str, Enum):
    ALL = "ALL"
    BUILDING = "BUILDING"


class VisitorStatus(str, Enum):
    EXPECTED = "EXPECTED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"
