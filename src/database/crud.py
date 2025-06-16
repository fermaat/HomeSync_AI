# src/database/crud.py
from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Item, Ticket


def create_ticket(
    db: Session,
    date: date,
    total_ticket: float,
    raw_gemini_data: dict,
    supermarket: str = None,
):
    db_ticket = Ticket(
        fecha_compra=date,
        supermercado=supermarket,
        total_ticket=total_ticket,
        raw_gemini_data=raw_gemini_data,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_ticket(db: Session, ticket_id: str):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def create_item(
    db: Session,
    ticket_id: str,
    product_name: str,
    unit_price: float,
    quantity: float,
    line_total_price: float,
    item_date: date,
    category: str = None,
):
    db_item = Item(
        ticket_id=ticket_id,
        nombre_producto=product_name,
        categoria=category,
        precio_unitario=unit_price,
        cantidad=quantity,
        precio_total_linea=line_total_price,
        fecha_item=item_date,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items_by_ticket(db: Session, ticket_id: str):
    return db.query(Item).filter(Item.ticket_id == ticket_id).all()


def get_items_by_category_and_date_range(
    db: Session, category: str, start_date: date, end_date: date
):
    return (
        db.query(Item)
        .filter(
            Item.categoria == category,
            Item.fecha_item >= start_date,
            Item.fecha_item <= end_date,
        )
        .all()
    )


def save_gemini_ticket_data(db: Session, gemini_extracted_data: dict):
    try:
        fecha_str = gemini_extracted_data.get("date") or str(date.today())
        try:
            item_date = date.fromisoformat(fecha_str)
        except ValueError:
            item_date = date.today()

        total_ticket = float(gemini_extracted_data.get("total", 0.0))
        supermarket = gemini_extracted_data.get("supermarket")

        db_ticket = create_ticket(
            db, item_date, total_ticket, gemini_extracted_data, supermarket
        )

        items_list = gemini_extracted_data.get("items", [])
        for item_data in items_list:
            print(item_data)
            name = item_data.get("product_name") or item_data.get("product")
            quantity = float(item_data.get("quantity", 1.0))
            unit_price = float(
                item_data.get("unit_price") or item_data.get("price", 0.0)
            )
            line_total_price = float(
                item_data.get("total_price", unit_price * quantity)
            )
            category = item_data.get("category", "Unknown")
            if name and line_total_price is not None:
                create_item(
                    db,
                    db_ticket.id,
                    name,
                    unit_price,
                    quantity,
                    line_total_price,
                    item_date,
                    category=category,
                )
        db.commit()
        return db_ticket

    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al guardar datos de Gemini en la BD: {e}")
