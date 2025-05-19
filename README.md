# Gestor de Dispositivos IoT con SQLAlchemy y Alembic

Este proyecto implementa un sistema de gestión de dispositivos IoT utilizando SQLAlchemy como ORM y Alembic para el control de versiones del esquema de base de datos.

## Diseño

El sistema está diseñado para gestionar una flota de dispositivos IoT, sus sensores, lecturas de datos y estados. La estructura de datos incluye:

- **TipoDispositivo**: Representa un tipo o modelo de dispositivo (ej. 'Raspberry Pi 4', 'ESP32 Temp Sensor v2').
- **GrupoDispositivos**: Representa una agrupación lógica de dispositivos (ej. 'Sensores Edificio A', 'Monitores Ambientales').
- **Dispositivo**: Representa una instancia física de un dispositivo con su información de identificación y ubicación.
- **Sensor**: Representa un sensor específico dentro de un dispositivo.
- **LecturaDato**: Almacena una lectura de datos de un sensor.
- **LogEstadoDispositivo**: Registra cambios en el estado de un dispositivo.

## Configuración del Entorno

### Requisitos

- Python 3.8 o superior
- PostgreSQL
- uv (gestor de paquetes para Python)

### Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/KurtKusch/gestor-dispositivos-iot.git
cd gestor-dispositivos-iot
```

2. Instalar uv (si no lo tienes):

```bash
pip install uv
```

3. Crear un entorno virtual e instalar las dependencias usando uv:

```bash
uv venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
uv pip install -r pyproject.toml
```

Alternativamente, puedes usar el modo editable:

```bash
uv pip install -e .
```

O si prefieres usar pip tradicional:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e .
```

4. Configurar la base de datos:

Crea una base de datos PostgreSQL llamada `iot_devices` y configura las credenciales en el archivo `.env`:

```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/iot_devices
```

## Ejecución

### Aplicar Migraciones

Para crear las tablas en la base de datos:

```bash
alembic upgrade head
```

### Ejecutar el Script de Demostración

Para ejecutar el script que demuestra la funcionalidad del sistema:

```bash
python -m app.main
```

## Estructura del Proyecto

```
.
├── alembic/                  # Configuración y scripts de Alembic
│   ├── versions/             # Scripts de migración
│   │   ├── initial_schema.py # Migración inicial
│   │   └── schema_modifications.py # Modificaciones al esquema
│   ├── env.py                # Configuración del entorno de Alembic
│   └── script.py.mako        # Plantilla para scripts de migración
├── app/                      # Código fuente de la aplicación
│   ├── __init__.py           # Inicialización del paquete
│   ├── database.py           # Configuración de la base de datos
│   ├── models.py             # Definición de modelos SQLAlchemy
│   ├── crud.py               # Operaciones CRUD
│   └── main.py               # Script principal de demostración
├── .env                      # Variables de entorno
├── .python-version           # Versión de Python
├── pyproject.toml            # Configuración del proyecto y dependencias
├── database_dump.sql         # Dump de la base de datos en formato SQL
├── uv.lock                   # Archivo de bloqueo de dependencias de uv
└── README.md                 # Documentación del proyecto
```

## Operaciones CRUD Implementadas

- Gestión de Tipos de Dispositivo: crear, consultar
- Gestión de Grupos de Dispositivos: crear, consultar
- Gestión de Dispositivos: crear, asociar a grupos, desasociar de grupos, consultar
- Gestión de Sensores: crear, consultar
- Gestión de Lecturas de Datos: registrar, consultar
- Gestión de Logs de Estado: registrar, consultar

## Modificaciones de Esquema

Se han implementado las siguientes modificaciones al esquema original:

1. Adición de la columna `umbral_alerta` (Float, nullable) al modelo Sensor.
2. Adición de la columna `estado_actual` al modelo Dispositivo para un acceso más rápido al estado.
3. Reestructuración de la ubicación: renombrado de `ubicacion` a `descripcion_ubicacion` y adición de `coordenadas_gps` (String, opcional) para almacenar coordenadas GPS.