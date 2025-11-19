from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.producto_schema import Producto, ProductoCreate, ProductoUpdate
from database import get_db, ProductoDB

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = ProductoDB(**producto.dict())
    try:
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el producto.")
    return db_producto


@router.get("/", response_model=List[Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = db.query(ProductoDB).offset(skip).limit(limit).all()
    return productos


@router.get("/{producto_id}", response_model=Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@router.put("/{producto_id}", response_model=Producto)
def update_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    try:
        db.commit()
        db.refresh(db_producto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar el producto.")
    return db_producto


@router.delete("/{producto_id}", response_model=Producto)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al eliminar el producto.")
    return db_producto
