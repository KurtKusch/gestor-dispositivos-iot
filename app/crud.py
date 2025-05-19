from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Union
from datetime import datetime

from . import models

# ---- Operaciones CRUD para TipoDispositivo ----

def create_tipo_dispositivo(db: Session, fabricante: str, modelo: str, descripcion: Optional[str] = None):
    """Crea un nuevo tipo de dispositivo o devuelve uno existente"""
    # Verificar si el tipo de dispositivo ya existe
    existing = db.query(models.TipoDispositivo).filter(models.TipoDispositivo.modelo == modelo).first()
    if existing:
        return existing
        
    # Crear nuevo si no existe
    db_tipo = models.TipoDispositivo(fabricante=fabricante, modelo=modelo, descripcion=descripcion)
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

def get_tipos_dispositivo(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los tipos de dispositivo"""
    return db.query(models.TipoDispositivo).offset(skip).limit(limit).all()

def get_tipo_dispositivo_by_id(db: Session, tipo_id: int):
    """Obtiene un tipo de dispositivo por ID"""
    return db.query(models.TipoDispositivo).filter(models.TipoDispositivo.id == tipo_id).first()

# ---- Operaciones CRUD para GrupoDispositivos ----

def create_grupo_dispositivos(db: Session, nombre: str, descripcion: Optional[str] = None):
    """Crea un nuevo grupo de dispositivos o devuelve uno existente"""
    # Verificar si el grupo ya existe
    existing = db.query(models.GrupoDispositivos).filter(models.GrupoDispositivos.nombre == nombre).first()
    if existing:
        return existing
        
    # Crear nuevo si no existe
    db_grupo = models.GrupoDispositivos(nombre=nombre, descripcion=descripcion)
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

def get_grupos_dispositivos(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los grupos de dispositivos"""
    return db.query(models.GrupoDispositivos).offset(skip).limit(limit).all()

def get_grupo_dispositivos_by_id(db: Session, grupo_id: int):
    """Obtiene un grupo de dispositivos por ID"""
    return db.query(models.GrupoDispositivos).filter(models.GrupoDispositivos.id == grupo_id).first()

# ---- Operaciones CRUD para Dispositivo ----

def create_dispositivo(db: Session, tipo_dispositivo_id: int, numero_serie: str, version_firmware: str, 
                       descripcion_ubicacion: str, mac_address: Optional[str] = None, coordenadas_gps: Optional[str] = None):
    """Crea un nuevo dispositivo"""
    db_dispositivo = models.Dispositivo(
        tipo_dispositivo_id=tipo_dispositivo_id,
        numero_serie=numero_serie,
        mac_address=mac_address,
        version_firmware=version_firmware,
        descripcion_ubicacion=descripcion_ubicacion,
        coordenadas_gps=coordenadas_gps
    )
    db.add(db_dispositivo)
    db.commit()
    db.refresh(db_dispositivo)
    return db_dispositivo

def get_dispositivos(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los dispositivos"""
    return db.query(models.Dispositivo).offset(skip).limit(limit).all()

def get_dispositivo_by_id(db: Session, dispositivo_id: int):
    """Obtiene un dispositivo por ID"""
    return db.query(models.Dispositivo).filter(models.Dispositivo.id == dispositivo_id).first()

def get_dispositivos_by_tipo(db: Session, tipo_id: int, skip: int = 0, limit: int = 100):
    """Obtiene todos los dispositivos de un tipo específico"""
    return db.query(models.Dispositivo).filter(models.Dispositivo.tipo_dispositivo_id == tipo_id)\
             .offset(skip).limit(limit).all()

def get_dispositivos_by_grupo(db: Session, grupo_id: int, skip: int = 0, limit: int = 100):
    """Obtiene todos los dispositivos pertenecientes a un grupo específico"""
    grupo = get_grupo_dispositivos_by_id(db, grupo_id)
    if grupo:
        return grupo.dispositivos[skip:skip+limit]
    return []

def get_grupos_by_dispositivo(db: Session, dispositivo_id: int):
    """Obtiene todos los grupos a los que pertenece un dispositivo"""
    dispositivo = get_dispositivo_by_id(db, dispositivo_id)
    if dispositivo:
        return dispositivo.grupos
    return []

def add_dispositivo_to_grupo(db: Session, dispositivo_id: int, grupo_id: int):
    """Asocia un dispositivo con un grupo"""
    dispositivo = get_dispositivo_by_id(db, dispositivo_id)
    grupo = get_grupo_dispositivos_by_id(db, grupo_id)
    
    if not dispositivo or not grupo:
        return None
    
    if grupo not in dispositivo.grupos:
        dispositivo.grupos.append(grupo)
        db.commit()
        db.refresh(dispositivo)
    
    return dispositivo

def remove_dispositivo_from_grupo(db: Session, dispositivo_id: int, grupo_id: int):
    """Desasocia un dispositivo de un grupo"""
    dispositivo = get_dispositivo_by_id(db, dispositivo_id)
    grupo = get_grupo_dispositivos_by_id(db, grupo_id)
    
    if not dispositivo or not grupo:
        return None
    
    if grupo in dispositivo.grupos:
        dispositivo.grupos.remove(grupo)
        db.commit()
        db.refresh(dispositivo)
    
    return dispositivo

# ---- Operaciones CRUD para Sensor ----

def create_sensor(db: Session, dispositivo_id: int, tipo_sensor: str, unidad_medida: str, umbral_alerta: Optional[float] = None):
    """Añade un sensor a un dispositivo existente"""
    db_sensor = models.Sensor(
        dispositivo_id=dispositivo_id,
        tipo_sensor=tipo_sensor,
        unidad_medida=unidad_medida,
        umbral_alerta=umbral_alerta
    )
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def get_sensores_by_dispositivo(db: Session, dispositivo_id: int):
    """Obtiene todos los sensores de un dispositivo específico"""
    return db.query(models.Sensor).filter(models.Sensor.dispositivo_id == dispositivo_id).all()

def get_sensor_by_id(db: Session, sensor_id: int):
    """Obtiene un sensor por ID"""
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

def create_lectura_dato(db: Session, sensor_id: int, valor_leido: Union[str, float], timestamp: Optional[datetime] = None):
    """Registra una nueva lectura de datos para un sensor"""
    # Convertir float a string si es necesario
    if isinstance(valor_leido, float):
        valor_leido = str(valor_leido)
        
    db_lectura = models.LecturaDato(
        sensor_id=sensor_id,
        valor_leido=valor_leido
    )
    
    if timestamp:
        db_lectura.timestamp = timestamp
        
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura

def get_ultimas_lecturas(db: Session, sensor_id: int, limit: int = 10):
    """Obtiene las últimas N lecturas de datos de un sensor específico"""
    return db.query(models.LecturaDato)\
             .filter(models.LecturaDato.sensor_id == sensor_id)\
             .order_by(desc(models.LecturaDato.timestamp))\
             .limit(limit).all()

def create_log_estado(db: Session, dispositivo_id: int, estado: str, mensaje_opcional: Optional[str] = None):
    """Registra un log de estado del dispositivo cuando cambia su estado"""
    db_log = models.LogEstadoDispositivo(
        dispositivo_id=dispositivo_id,
        estado=estado,
        mensaje_opcional=mensaje_opcional
    )
    db.add(db_log)
    
    # Actualizar el estado_actual en el Dispositivo
    dispositivo = get_dispositivo_by_id(db, dispositivo_id)
    if dispositivo:
        dispositivo.estado_actual = estado
    
    db.commit()
    db.refresh(db_log)
    return db_log

def get_historial_estado(db: Session, dispositivo_id: int, skip: int = 0, limit: int = 100):
    """Obtiene el historial de estado para un dispositivo específico"""
    return db.query(models.LogEstadoDispositivo)\
             .filter(models.LogEstadoDispositivo.dispositivo_id == dispositivo_id)\
             .order_by(desc(models.LogEstadoDispositivo.timestamp))\
             .offset(skip).limit(limit).all()