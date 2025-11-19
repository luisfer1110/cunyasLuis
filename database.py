from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# --- Configuración de la Conexión a MySQL con XAMPP ---
DB_URL = "mysql+pymysql://root:@localhost:3306/testdb"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Modelos de Tablas ---

class ProductoDB(Base):
    __tablename__ = "productos" # Cambiado a plural para consistencia
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), index=True)
    descripcion = Column(String(500))
    precio = Column(Float)
    cantidad_en_stock = Column(Integer)

class ClienteDB(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    direccion = Column(String(255))
    
    pedidos = relationship("PedidoDB", back_populates="cliente")

class PedidoDB(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)

    cliente = relationship("ClienteDB", back_populates="pedidos")

# --- Funciones de Base de Datos ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
