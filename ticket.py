"""Pydantic schemas for Ticket and Customer data transfer."""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .base import TimeStampedSchema
from .user import User
from app.models.ticket import TicketStatus, TicketPriority

# --- Customer Schemas ---

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    country: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(TimeStampedSchema, CustomerBase):
    pass

# --- Ticket Schemas ---

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

class Ticket(TimeStampedSchema, TicketBase):
    customer: Customer
    assignee: Optional[User] = None