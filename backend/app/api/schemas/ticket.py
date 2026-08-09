"""Pydantic schemas for Ticket and Customer data transfer."""

from typing import Optional

from pydantic import BaseModel, EmailStr

from app.api.schemas.base import TimeStampedSchema
from app.api.schemas.user import User
from app.models.ticket import TicketPriority, TicketStatus


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    country: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(TimeStampedSchema, CustomerBase):
    pass


class TicketBase(BaseModel):
    subject: str
    description: str
    status: TicketStatus = TicketStatus.OPEN
    priority: TicketPriority = TicketPriority.MEDIUM
    category: Optional[str] = None


class TicketCreate(TicketBase):
    customer_id: int


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assignee_id: Optional[int] = None


class Ticket(TicketBase, TimeStampedSchema):
    customer: Customer
    assignee: Optional[User] = None
