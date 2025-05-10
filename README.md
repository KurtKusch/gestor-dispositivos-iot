# 📡 Gestor de Dispositivos IoT

Este proyecto es un sistema backend para la gestión de dispositivos IoT. Está desarrollado en Python utilizando **SQLAlchemy** como ORM y **Alembic** para el control de versiones del esquema de base de datos. El objetivo es registrar y administrar dispositivos físicos, sensores y los datos que generan.

---

## 📁 Estructura del Proyecto

```
gestor_iot/
├── app/
│   ├── __init__.py
│   ├── models.py             # Modelos de SQLAlchemy
│   ├── database.py           # Configuración de la base de datos
│   ├── crud.py               # Funciones CRUD
│   └── main.py               # Script para pruebas
├── alembic/                  # Migraciones automáticas de Alembic
│   ├── versions/             # Archivos de migraciones
│   └── env.py                # Configuración de Alembic
├── alembic.ini               # Configuración general de Alembic
├── .gitignore
├── pyproject.toml            # Archivo de dependencias
├── uv.lock                   # Archivo de lock para poetry
├── .python-version           # Versión de Python usada en el proyecto
└── README.md
```

---

## 🧱 Requisitos del Proyecto

- Python 3.11+
- PostgreSQL
- SQLAlchemy
- Alembic
- poetry o pip para gestión de dependencias

---

## ⚙️ Configuración Inicial

1. Clona el repositorio:

```bash
git clone https://github.com/KurtKusch/gestor-dispositivos-iot.git
cd gestor-dispositivos-iot
```

2. Crea el entorno virtual e instala dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> *O si usas `poetry`:*
```bash
poetry install
```

---
