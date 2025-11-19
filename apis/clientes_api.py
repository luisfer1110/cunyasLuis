from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.cliente_schema import Cliente, ClienteCreate, ClienteUpdate
from database import get_db, ClienteDB

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(ClienteDB).filter(ClienteDB.email == cliente.email).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    db_cliente = ClienteDB(**cliente.dict())
    try:
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el cliente.")
    return db_cliente

@router.get("/", response_model=List[Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(ClienteDB).offset(skip).limit(limit).all()
    return clientes

@router.get("/{cliente_id}", response_model=Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=Cliente)
def update_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    update_data = cliente.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    
    try:
        db.commit()
        db.refresh(db_cliente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar el cliente.")
    return db_cliente

@router.delete("/{cliente_id}", response_model=Cliente)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(db_cliente)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al eliminar el cliente.")
    return db_cliente
