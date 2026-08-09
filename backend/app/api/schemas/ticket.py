"""Pydantic schemas for Ticket and Customer data transfer."""


from pydantic import BaseModel, EmailStr

from app.api.schemas.base import TimeStampedSchema
from app.api.schemas.user import User
from app.models.ticket import TicketPriority, TicketStatus


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None
    country: str | None = None


class CustomerCreate(CustomerBase):
    pass


class Customer(TimeStampedSchema, CustomerBase):
    pass


class TicketBase(BaseModel):
    subject: str
    description: str
    status: TicketStatus = TicketStatus.OPEN
    priority: TicketPriority = TicketPriority.MEDIUM
    category: str | None = None


class TicketCreate(TicketBase):
    customer_id: int


class TicketUpdate(BaseModel):
    subject: str | None = None
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    assignee_id: int | None = None


class Ticket(TicketBase, TimeStampedSchema):
    customer: Customer
    assignee: User | None = None
