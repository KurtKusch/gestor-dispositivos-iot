from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

# Tabla de asociación para la relación muchos-a-muchos
dispositivo_grupo = Table(
    'dispositivo_grupo',
    Base.metadata,
    Column('dispositivo_id', Integer, ForeignKey('dispositivo.id'), primary_key=True),
    Column('grupo_id', Integer, ForeignKey('grupo_dispositivos.id'), primary_key=True)
)

class TipoDispositivo(Base):
    __tablename__ = 'tipo_dispositivo'
    
    id = Column(Integer, primary_key=True, index=True)
    fabricante = Column(String, nullable=False)
    modelo = Column(String, unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # Relationships
    dispositivos = relationship("Dispositivo", back_populates="tipo_dispositivo")
    
    def __repr__(self):
        return f"<TipoDispositivo(id={self.id}, fabricante='{self.fabricante}', modelo='{self.modelo}')>"

class GrupoDispositivos(Base):
    __tablename__ = 'grupo_dispositivos'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # Relationships
    dispositivos = relationship("Dispositivo", secondary=dispositivo_grupo, back_populates="grupos")
    
    def __repr__(self):
        return f"<GrupoDispositivos(id={self.id}, nombre='{self.nombre}')>"

class Dispositivo(Base):
    __tablename__ = 'dispositivo'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, unique=True, nullable=False)
    mac_address = Column(String, unique=True, nullable=True)
    version_firmware = Column(String, nullable=False)
    descripcion_ubicacion = Column(String, nullable=False)  # Renamed from ubicacion
    coordenadas_gps = Column(String, nullable=True)  # New column for GPS coordinates
    fecha_registro = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    tipo_dispositivo_id = Column(Integer, ForeignKey('tipo_dispositivo.id'), nullable=False)
    estado_actual = Column(String, nullable=True)  # New column for current status
    
    tipo_dispositivo = relationship("TipoDispositivo", back_populates="dispositivos")
    sensores = relationship("Sensor", back_populates="dispositivo", cascade="all, delete-orphan")
    logs_estado = relationship("LogEstadoDispositivo", back_populates="dispositivo", cascade="all, delete-orphan")
    grupos = relationship("GrupoDispositivos", secondary=dispositivo_grupo, back_populates="dispositivos")
    
    def __repr__(self):
        return f"<Dispositivo(id={self.id}, numero_serie='{self.numero_serie}')>"

class Sensor(Base):
    __tablename__ = 'sensor'
    
    id = Column(Integer, primary_key=True, index=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivo.id'), nullable=False)
    tipo_sensor = Column(String, nullable=False)
    unidad_medida = Column(String, nullable=False)
    umbral_alerta = Column(Float, nullable=True)  # New column for alert threshold
    
    dispositivo = relationship("Dispositivo", back_populates="sensores")
    lecturas = relationship("LecturaDato", back_populates="sensor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Sensor(id={self.id}, tipo_sensor='{self.tipo_sensor}', unidad_medida='{self.unidad_medida}')>"

class LecturaDato(Base):
    __tablename__ = 'lectura_dato'
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey('sensor.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    valor_leido = Column(String, nullable=False)  # Using String for flexibility
    
    sensor = relationship("Sensor", back_populates="lecturas")
    
    def __repr__(self):
        return f"<LecturaDato(id={self.id}, sensor_id={self.sensor_id}, timestamp='{self.timestamp}', valor_leido='{self.valor_leido}')>"

class LogEstadoDispositivo(Base):
    __tablename__ = 'log_estado_dispositivo'
    
    id = Column(Integer, primary_key=True, index=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivo.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    estado = Column(String, nullable=False)  # 'online', 'offline', 'error', 'mantenimiento'
    mensaje_opcional = Column(Text, nullable=True)
    
    dispositivo = relationship("Dispositivo", back_populates="logs_estado")
    
    def __repr__(self):
        return f"<LogEstadoDispositivo(id={self.id}, dispositivo_id={self.dispositivo_id}, estado='{self.estado}')>"