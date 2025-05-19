-- PostgreSQL database dump

-- Dumped from database version 14.10
-- Dumped by pg_dump version 14.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Create database
CREATE DATABASE iot_devices;
\connect iot_devices

-- Create schema
CREATE SCHEMA public;

-- Create tables
CREATE TABLE public.tipo_dispositivo (
    id SERIAL PRIMARY KEY,
    fabricante VARCHAR NOT NULL,
    modelo VARCHAR NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE public.grupo_dispositivos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE public.dispositivo (
    id SERIAL PRIMARY KEY,
    numero_serie VARCHAR NOT NULL UNIQUE,
    mac_address VARCHAR UNIQUE,
    version_firmware VARCHAR NOT NULL,
    descripcion_ubicacion VARCHAR NOT NULL,
    coordenadas_gps VARCHAR,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    tipo_dispositivo_id INTEGER NOT NULL REFERENCES public.tipo_dispositivo(id),
    estado_actual VARCHAR
);

CREATE TABLE public.dispositivo_grupo (
    dispositivo_id INTEGER NOT NULL REFERENCES public.dispositivo(id),
    grupo_id INTEGER NOT NULL REFERENCES public.grupo_dispositivos(id),
    PRIMARY KEY (dispositivo_id, grupo_id)
);

CREATE TABLE public.sensor (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES public.dispositivo(id),
    tipo_sensor VARCHAR NOT NULL,
    unidad_medida VARCHAR NOT NULL,
    umbral_alerta FLOAT
);

CREATE TABLE public.lectura_dato (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES public.sensor(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    valor_leido VARCHAR NOT NULL
);

CREATE TABLE public.log_estado_dispositivo (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES public.dispositivo(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    estado VARCHAR NOT NULL,
    mensaje_opcional TEXT
);

-- Create indexes
CREATE INDEX idx_dispositivo_tipo ON public.dispositivo(tipo_dispositivo_id);
CREATE INDEX idx_sensor_dispositivo ON public.sensor(dispositivo_id);
CREATE INDEX idx_lectura_sensor ON public.lectura_dato(sensor_id);
CREATE INDEX idx_log_dispositivo ON public.log_estado_dispositivo(dispositivo_id);
CREATE INDEX idx_lectura_timestamp ON public.lectura_dato(timestamp);
CREATE INDEX idx_log_timestamp ON public.log_estado_dispositivo(timestamp);

-- Grant permissions
ALTER TABLE public.tipo_dispositivo OWNER TO postgres;
ALTER TABLE public.grupo_dispositivos OWNER TO postgres;
ALTER TABLE public.dispositivo OWNER TO postgres;
ALTER TABLE public.dispositivo_grupo OWNER TO postgres;
ALTER TABLE public.sensor OWNER TO postgres;
ALTER TABLE public.lectura_dato OWNER TO postgres;
ALTER TABLE public.log_estado_dispositivo OWNER TO postgres;

-- Sample data
-- Insert sample data for tipo_dispositivo
INSERT INTO public.tipo_dispositivo (fabricante, modelo, descripcion) VALUES
('Raspberry Pi Foundation', 'Raspberry Pi 4', 'Ordenador de placa única con capacidades IoT'),
('Espressif', 'ESP32 Temp Sensor v2', 'Microcontrolador con sensores de temperatura integrados');

-- Insert sample data for grupo_dispositivos
INSERT INTO public.grupo_dispositivos (nombre, descripcion) VALUES
('Sensores Edificio A', 'Dispositivos instalados en el Edificio A'),
('Monitores Ambientales', 'Dispositivos que monitorean condiciones ambientales');

-- Insert sample data for dispositivo
INSERT INTO public.dispositivo (numero_serie, mac_address, version_firmware, descripcion_ubicacion, coordenadas_gps, tipo_dispositivo_id, estado_actual) VALUES
('RPI-001', 'AA:BB:CC:DD:EE:FF', '1.0.0', 'Sala de servidores, Edificio A', '40.4168,-3.7038', 1, 'online'),
('ESP-001', '11:22:33:44:55:66', '2.1.0', 'Laboratorio, Edificio A', '40.4169,-3.7039', 2, NULL),
('ESP-002', 'AA:22:33:44:55:77', '2.1.0', 'Oficina principal, Edificio B', '40.4170,-3.7040', 2, NULL);

-- Insert sample data for dispositivo_grupo
INSERT INTO public.dispositivo_grupo (dispositivo_id, grupo_id) VALUES
(1, 1),
(2, 1),
(2, 2),
(3, 2);

-- Insert sample data for sensor
INSERT INTO public.sensor (dispositivo_id, tipo_sensor, unidad_medida, umbral_alerta) VALUES
(1, 'temperatura', '°C', 30.0),
(1, 'humedad', '%', 80.0),
(2, 'temperatura', '°C', 28.0),
(3, 'temperatura', '°C', 28.0),
(3, 'movimiento', 'boolean', NULL);

-- Insert sample data for log_estado_dispositivo
INSERT INTO public.log_estado_dispositivo (dispositivo_id, estado, mensaje_opcional, timestamp) VALUES
(1, 'online', NULL, NOW()),
(1, 'offline', NULL, NOW() - INTERVAL '6 HOURS'),
(1, 'error', 'Error de conexión detectado', NOW() - INTERVAL '12 HOURS'),
(1, 'mantenimiento', 'Mantenimiento programado', NOW() - INTERVAL '18 HOURS'),
(1, 'online', NULL, NOW() - INTERVAL '24 HOURS');

-- Insert sample data for lectura_dato (just a few examples)
INSERT INTO public.lectura_dato (sensor_id, valor_leido, timestamp) VALUES
(1, '22.5', NOW()),
(1, '23.1', NOW() - INTERVAL '1 HOUR'),
(1, '22.8', NOW() - INTERVAL '2 HOURS'),
(2, '45.0', NOW()),
(2, '46.5', NOW() - INTERVAL '1 HOUR'),
(3, '19.5', NOW()),
(4, '24.2', NOW()),
(5, 'true', NOW());