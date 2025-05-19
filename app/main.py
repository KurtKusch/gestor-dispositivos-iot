import sys
import os
from datetime import datetime, timedelta
import random
from sqlalchemy.exc import IntegrityError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models, crud
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_tipo_dispositivo_by_modelo(db: Session, modelo: str):
    return db.query(models.TipoDispositivo).filter(models.TipoDispositivo.modelo == modelo).first()

def get_grupo_dispositivos_by_nombre(db: Session, nombre: str):
    return db.query(models.GrupoDispositivos).filter(models.GrupoDispositivos.nombre == nombre).first()

def get_dispositivo_by_numero_serie(db: Session, numero_serie: str):
    return db.query(models.Dispositivo).filter(models.Dispositivo.numero_serie == numero_serie).first()

def get_sensor_by_dispositivo_and_tipo(db: Session, dispositivo_id: int, tipo_sensor: str):
    return db.query(models.Sensor).filter(
        models.Sensor.dispositivo_id == dispositivo_id,
        models.Sensor.tipo_sensor == tipo_sensor
    ).first()

def main():
    db = SessionLocal()
    
    try:
        print(" Demostración del Sistema de Gestión de Dispositivos IoT ")        
        print("\n1. Creando/recuperando tipos de dispositivos...")
        
        tipo1 = get_tipo_dispositivo_by_modelo(db, "Raspberry Pi 4")
        if not tipo1:
            tipo1 = crud.create_tipo_dispositivo(
                db, fabricante="Raspberry Pi Foundation", 
                modelo="Raspberry Pi 4", 
                descripcion="Ordenador de placa única con capacidades IoT"
            )
            print(f"  - Creado: {tipo1}")
        else:
            print(f"  - Recuperado existente: {tipo1}")
        
        # Buscar o crear tipo2
        tipo2 = get_tipo_dispositivo_by_modelo(db, "ESP32 Temp Sensor v2")
        if not tipo2:
            tipo2 = crud.create_tipo_dispositivo(
                db, fabricante="Espressif", 
                modelo="ESP32 Temp Sensor v2", 
                descripcion="Microcontrolador con sensores de temperatura integrados"
            )
            print(f"  - Creado: {tipo2}")
        else:
            print(f"  - Recuperado existente: {tipo2}")
        
        # 2. Crear o recuperar grupos de dispositivos
        print("\n2. Creando/recuperando grupos de dispositivos...")
        
        # Buscar o crear grupo1
        grupo1 = get_grupo_dispositivos_by_nombre(db, "Sensores Edificio A")
        if not grupo1:
            grupo1 = crud.create_grupo_dispositivos(
                db, nombre="Sensores Edificio A", 
                descripcion="Dispositivos instalados en el Edificio A"
            )
            print(f"  - Creado: {grupo1}")
        else:
            print(f"  - Recuperado existente: {grupo1}")
        
        # Buscar o crear grupo2
        grupo2 = get_grupo_dispositivos_by_nombre(db, "Monitores Ambientales")
        if not grupo2:
            grupo2 = crud.create_grupo_dispositivos(
                db, nombre="Monitores Ambientales", 
                descripcion="Dispositivos que monitorean condiciones ambientales"
            )
            print(f"  - Creado: {grupo2}")
        else:
            print(f"  - Recuperado existente: {grupo2}")
        
        # 3. Crear o recuperar dispositivos
        print("\n3. Creando/recuperando dispositivos...")
        
        # Buscar o crear dispositivo1
        dispositivo1 = get_dispositivo_by_numero_serie(db, "RPI-001")
        if not dispositivo1:
            dispositivo1 = crud.create_dispositivo(
                db, tipo_dispositivo_id=tipo1.id,
                numero_serie="RPI-001",
                mac_address="AA:BB:CC:DD:EE:FF",
                version_firmware="1.0.0",
                descripcion_ubicacion="Sala de servidores, Edificio A",
                coordenadas_gps="40.4168,-3.7038"
            )
            print(f"  - Creado: {dispositivo1}")
        else:
            print(f"  - Recuperado existente: {dispositivo1}")
        
        # Buscar o crear dispositivo2
        dispositivo2 = get_dispositivo_by_numero_serie(db, "ESP-001")
        if not dispositivo2:
            dispositivo2 = crud.create_dispositivo(
                db, tipo_dispositivo_id=tipo2.id,
                numero_serie="ESP-001",
                mac_address="11:22:33:44:55:66",
                version_firmware="2.1.0",
                descripcion_ubicacion="Laboratorio, Edificio A",
                coordenadas_gps="40.4169,-3.7039"
            )
            print(f"  - Creado: {dispositivo2}")
        else:
            print(f"  - Recuperado existente: {dispositivo2}")
        
        # Buscar o crear dispositivo3
        dispositivo3 = get_dispositivo_by_numero_serie(db, "ESP-002")
        if not dispositivo3:
            dispositivo3 = crud.create_dispositivo(
                db, tipo_dispositivo_id=tipo2.id,
                numero_serie="ESP-002",
                mac_address="AA:22:33:44:55:77",
                version_firmware="2.1.0",
                descripcion_ubicacion="Oficina principal, Edificio B",
                coordenadas_gps="40.4170,-3.7040"
            )
            print(f"  - Creado: {dispositivo3}")
        else:
            print(f"  - Recuperado existente: {dispositivo3}")
        
        # 4. Asociar dispositivos a grupos (idempotente)
        print("\n4. Asociando dispositivos a grupos...")
        
        # Verificar si dispositivo1 ya está en grupo1
        if grupo1 not in dispositivo1.grupos:
            crud.add_dispositivo_to_grupo(db, dispositivo1.id, grupo1.id)
            print(f"  - Dispositivo {dispositivo1.numero_serie} añadido al grupo {grupo1.nombre}")
        else:
            print(f"  - Dispositivo {dispositivo1.numero_serie} ya estaba en el grupo {grupo1.nombre}")
        
        # Verificar si dispositivo2 ya está en grupo1
        if grupo1 not in dispositivo2.grupos:
            crud.add_dispositivo_to_grupo(db, dispositivo2.id, grupo1.id)
            print(f"  - Dispositivo {dispositivo2.numero_serie} añadido al grupo {grupo1.nombre}")
        else:
            print(f"  - Dispositivo {dispositivo2.numero_serie} ya estaba en el grupo {grupo1.nombre}")
        
        # Verificar si dispositivo2 ya está en grupo2
        if grupo2 not in dispositivo2.grupos:
            crud.add_dispositivo_to_grupo(db, dispositivo2.id, grupo2.id)
            print(f"  - Dispositivo {dispositivo2.numero_serie} añadido al grupo {grupo2.nombre}")
        else:
            print(f"  - Dispositivo {dispositivo2.numero_serie} ya estaba en el grupo {grupo2.nombre}")
        
        # Verificar si dispositivo3 ya está en grupo2
        if grupo2 not in dispositivo3.grupos:
            crud.add_dispositivo_to_grupo(db, dispositivo3.id, grupo2.id)
            print(f"  - Dispositivo {dispositivo3.numero_serie} añadido al grupo {grupo2.nombre}")
        else:
            print(f"  - Dispositivo {dispositivo3.numero_serie} ya estaba en el grupo {grupo2.nombre}")
        
        # 5. Crear sensores para los dispositivos (si no existen)
        print("\n5. Creando/recuperando sensores para los dispositivos...")
        
        # Buscar o crear sensor1
        sensor1 = get_sensor_by_dispositivo_and_tipo(db, dispositivo1.id, "temperatura")
        if not sensor1:
            sensor1 = crud.create_sensor(
                db, dispositivo_id=dispositivo1.id,
                tipo_sensor="temperatura",
                unidad_medida="°C",
                umbral_alerta=30.0  # Alerta si la temperatura supera los 30°C
            )
            print(f"  - Creado: {sensor1}")
        else:
            print(f"  - Recuperado existente: {sensor1}")
        
        # Buscar o crear sensor2
        sensor2 = get_sensor_by_dispositivo_and_tipo(db, dispositivo1.id, "humedad")
        if not sensor2:
            sensor2 = crud.create_sensor(
                db, dispositivo_id=dispositivo1.id,
                tipo_sensor="humedad",
                unidad_medida="%",
                umbral_alerta=80.0  # Alerta si la humedad supera el 80%
            )
            print(f"  - Creado: {sensor2}")
        else:
            print(f"  - Recuperado existente: {sensor2}")
        
        # Buscar o crear sensor3
        sensor3 = get_sensor_by_dispositivo_and_tipo(db, dispositivo2.id, "temperatura")
        if not sensor3:
            sensor3 = crud.create_sensor(
                db, dispositivo_id=dispositivo2.id,
                tipo_sensor="temperatura",
                unidad_medida="°C",
                umbral_alerta=28.0  # Alerta si la temperatura supera los 28°C
            )
            print(f"  - Creado: {sensor3}")
        else:
            print(f"  - Recuperado existente: {sensor3}")
        
        # Buscar o crear sensor4
        sensor4 = get_sensor_by_dispositivo_and_tipo(db, dispositivo3.id, "temperatura")
        if not sensor4:
            sensor4 = crud.create_sensor(
                db, dispositivo_id=dispositivo3.id,
                tipo_sensor="temperatura",
                unidad_medida="°C",
                umbral_alerta=28.0  # Alerta si la temperatura supera los 28°C
            )
            print(f"  - Creado: {sensor4}")
        else:
            print(f"  - Recuperado existente: {sensor4}")
        
        # Buscar o crear sensor5
        sensor5 = get_sensor_by_dispositivo_and_tipo(db, dispositivo3.id, "movimiento")
        if not sensor5:
            sensor5 = crud.create_sensor(
                db, dispositivo_id=dispositivo3.id,
                tipo_sensor="movimiento",
                unidad_medida="boolean"
                # No umbral_alerta para sensores de movimiento
            )
            print(f"  - Creado: {sensor5}")
        else:
            print(f"  - Recuperado existente: {sensor5}")
        
        # 6. Registrar lecturas de datos para los sensores
        print("\n6. Registrando lecturas de datos para los sensores...")
        print("  (Nota: Se crearán nuevas lecturas cada vez que se ejecute este script)")
        
        # Generar algunas lecturas de temperatura para la última hora
        now = datetime.now()
        for i in range(6):  # Limitado a 6 lecturas
            timestamp = now - timedelta(minutes=i*10)
            
            # Lecturas para sensor1 (temperatura en Raspberry Pi)
            temp_value = round(random.uniform(20.0, 25.0), 1)
            lectura = crud.create_lectura_dato(db, sensor1.id, temp_value, timestamp)
            print(f"  - Lectura para sensor {sensor1.id}: {lectura.valor_leido} {sensor1.unidad_medida} en {lectura.timestamp}")
            
            # Lecturas para sensor2 (humedad en Raspberry Pi)
            humidity_value = round(random.uniform(40.0, 60.0), 1)
            lectura = crud.create_lectura_dato(db, sensor2.id, humidity_value, timestamp)
            print(f"  - Lectura para sensor {sensor2.id}: {lectura.valor_leido} {sensor2.unidad_medida} en {lectura.timestamp}")
            
            # Lecturas para sensor3 (temperatura en ESP32)
            temp_value = round(random.uniform(18.0, 22.0), 1)
            lectura = crud.create_lectura_dato(db, sensor3.id, temp_value, timestamp)
            print(f"  - Lectura para sensor {sensor3.id}: {lectura.valor_leido} {sensor3.unidad_medida} en {lectura.timestamp}")
            
            # Lecturas para sensor4 (temperatura en ESP32)
            temp_value = round(random.uniform(22.0, 26.0), 1)
            lectura = crud.create_lectura_dato(db, sensor4.id, temp_value, timestamp)
            print(f"  - Lectura para sensor {sensor4.id}: {lectura.valor_leido} {sensor4.unidad_medida} en {lectura.timestamp}")
            
            # Lecturas para sensor5 (movimiento en ESP32)
            movement_value = "true" if random.random() > 0.7 else "false"
            lectura = crud.create_lectura_dato(db, sensor5.id, movement_value, timestamp)
            print(f"  - Lectura para sensor {sensor5.id}: {lectura.valor_leido} en {lectura.timestamp}")
        
        # 7. Registrar cambios de estado para los dispositivos
        print("\n7. Registrando cambios de estado para los dispositivos...")
        
        # Verificar el estado actual del dispositivo1
        estado_actual = dispositivo1.estado_actual
        if estado_actual != "online":
            log = crud.create_log_estado(db, dispositivo1.id, "online")
            print(f"  - Log para dispositivo {dispositivo1.numero_serie}: {log.estado} en {log.timestamp}")
        else:
            print(f"  - Dispositivo {dispositivo1.numero_serie} ya está en estado 'online'")
        
        # 8. Consultar información
        print("\n8. Consultando información...")
        
        # Consultar todos los dispositivos de un tipo específico
        print("\n  a. Dispositivos de tipo ESP32 Temp Sensor v2:")
        dispositivos_tipo2 = crud.get_dispositivos_by_tipo(db, tipo2.id)
        for disp in dispositivos_tipo2:
            print(f"    - {disp.numero_serie} (Ubicación: {disp.descripcion_ubicacion}, Coordenadas: {disp.coordenadas_gps})")
        
        # Consultar todos los dispositivos de un grupo específico
        print("\n  b. Dispositivos en el grupo Monitores Ambientales:")
        dispositivos_grupo2 = crud.get_dispositivos_by_grupo(db, grupo2.id)
        for disp in dispositivos_grupo2:
            print(f"    - {disp.numero_serie} (Tipo: {disp.tipo_dispositivo.modelo}, Estado: {disp.estado_actual})")
        
        # Consultar los grupos a los que pertenece un dispositivo específico
        print(f"\n  c. Grupos a los que pertenece el dispositivo {dispositivo2.numero_serie}:")
        grupos_disp2 = crud.get_grupos_by_dispositivo(db, dispositivo2.id)
        for grupo in grupos_disp2:
            print(f"    - {grupo.nombre}")
        
        # Consultar los sensores de un dispositivo específico
        print(f"\n  d. Sensores del dispositivo {dispositivo1.numero_serie}:")
        sensores_disp1 = crud.get_sensores_by_dispositivo(db, dispositivo1.id)
        for sensor in sensores_disp1:
            umbral = f", Umbral de alerta: {sensor.umbral_alerta} {sensor.unidad_medida}" if sensor.umbral_alerta else ""
            print(f"    - {sensor.tipo_sensor} ({sensor.unidad_medida}{umbral})")
        
        # Consultar las últimas lecturas de un sensor específico
        print(f"\n  e. Últimas 5 lecturas del sensor de temperatura del dispositivo {dispositivo1.numero_serie}:")
        ultimas_lecturas = crud.get_ultimas_lecturas(db, sensor1.id, 5)
        for lectura in ultimas_lecturas:
            print(f"    - {lectura.timestamp}: {lectura.valor_leido} {sensor1.unidad_medida}")
        
        # Consultar el historial de estado de un dispositivo específico
        print(f"\n  f. Historial de estado del dispositivo {dispositivo1.numero_serie}:")
        historial_estado = crud.get_historial_estado(db, dispositivo1.id)
        for log in historial_estado:
            mensaje = f" - {log.mensaje_opcional}" if log.mensaje_opcional else ""
            print(f"    - {log.timestamp}: {log.estado}{mensaje}")
        
        print("\n Fin de la demostración \n")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()