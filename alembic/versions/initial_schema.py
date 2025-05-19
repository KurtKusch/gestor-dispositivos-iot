"""Initial schema

Revision ID: initial_schema
Revises: 
Create Date: 2025-05-18 14:02:10.683954

"""
from alembic import op
import sqlalchemy as sa


revision = 'initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tipo_dispositivo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fabricante', sa.String(), nullable=False),
        sa.Column('modelo', sa.String(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('modelo')
    )
    
    op.create_table('grupo_dispositivos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    
    op.create_table('dispositivo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_serie', sa.String(), nullable=False),
        sa.Column('mac_address', sa.String(), nullable=True),
        sa.Column('version_firmware', sa.String(), nullable=False),
        sa.Column('ubicacion', sa.String(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('tipo_dispositivo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tipo_dispositivo_id'], ['tipo_dispositivo.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('mac_address'),
        sa.UniqueConstraint('numero_serie')
    )
    
    op.create_table('dispositivo_grupo',
        sa.Column('dispositivo_id', sa.Integer(), nullable=False),
        sa.Column('grupo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivo.id'], ),
        sa.ForeignKeyConstraint(['grupo_id'], ['grupo_dispositivos.id'], ),
        sa.PrimaryKeyConstraint('dispositivo_id', 'grupo_id')
    )
    
    op.create_table('sensor',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dispositivo_id', sa.Integer(), nullable=False),
        sa.Column('tipo_sensor', sa.String(), nullable=False),
        sa.Column('unidad_medida', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivo.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('log_estado_dispositivo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dispositivo_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('estado', sa.String(), nullable=False),
        sa.Column('mensaje_opcional', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivo.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('lectura_dato',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sensor_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('valor_leido', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('lectura_dato')
    op.drop_table('log_estado_dispositivo')
    op.drop_table('sensor')
    op.drop_table('dispositivo_grupo')
    op.drop_table('dispositivo')
    op.drop_table('grupo_dispositivos')
    op.drop_table('tipo_dispositivo')