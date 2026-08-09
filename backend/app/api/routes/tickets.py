"""API endpoints for managing tickets."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.ticket import Ticket, TicketCreate, TicketUpdate
from app.database.session import get_db

router = APIRouter()


@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_in: TicketCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    _ = (ticket_in, db)
    return {"message": "Placeholder for creating a ticket."}


@router.get("/", response_model=List[Ticket])
async def get_all_tickets(db: AsyncSession = Depends(get_db)) -> List[Ticket]:
    _ = db
    return []


@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    _ = db
    return {"message": f"Placeholder for retrieving ticket {ticket_id}."}
