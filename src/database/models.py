import uuid

from sqlalchemy import Column, Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_compra = Column(Date, nullable=False)
    supermercado = Column(String)
    total_ticket = Column(Numeric(10, 2), nullable=False)
    raw_gemini_data = Column(JSONB)  # Will save full json from Gemini

    items = relationship("Item", back_populates="ticket")

    def __repr__(self):
        return f"<Ticket(id={self.id}, fecha_compra={self.fecha_compra}, total={self.total_ticket})>"


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False)
    nombre_producto = Column(String, nullable=False)
    categoria = Column(String)
    precio_unitario = Column(Numeric(10, 2))
    cantidad = Column(Numeric(10, 3))  #
    precio_total_linea = Column(Numeric(10, 2), nullable=False)
    fecha_item = Column(Date, nullable=False)
    ticket = relationship("Ticket", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, producto={self.nombre_producto}, precio={self.precio_total_linea})>"
