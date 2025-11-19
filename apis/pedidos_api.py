from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.pedido_schema import Pedido, PedidoCreate, PedidoUpdate
from database import get_db, PedidoDB, ClienteDB # Importar ClienteDB para la verificación

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@router.post("/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    # Verificación de que el cliente existe antes de crear el pedido
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == pedido.cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail=f"Cliente con id {pedido.cliente_id} no encontrado")
    
    db_pedido = PedidoDB(**pedido.dict())
    try:
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el pedido.")
    return db_pedido


@router.get("/", response_model=List[Pedido])
def read_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidos = db.query(PedidoDB).offset(skip).limit(limit).all()
    return pedidos


@router.get("/{pedido_id}", response_model=Pedido)
def read_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido


@router.put("/{pedido_id}", response_model=Pedido)
def update_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    update_data = pedido.dict(exclude_unset=True)
    # Si se intenta actualizar cliente_id, verificar que el nuevo cliente exista
    if 'cliente_id' in update_data and update_data['cliente_id'] is not None:
        db_cliente = db.query(ClienteDB).filter(ClienteDB.id == update_data['cliente_id']).first()
        if not db_cliente:
            raise HTTPException(status_code=404, detail=f"Nuevo cliente con id {update_data['cliente_id']} no encontrado")

    for key, value in update_data.items():
        setattr(db_pedido, key, value)
    
    try:
        db.commit()
        db.refresh(db_pedido)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar el pedido.")
    return db_pedido


@router.delete("/{pedido_id}", response_model=Pedido)
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    db.delete(db_pedido)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al eliminar el pedido.")
    return db_pedido
