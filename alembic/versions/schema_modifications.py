"""Schema modifications

Revision ID: schema_modifications
Revises: initial_schema
Create Date: 2025-05-18 14:02:10.683954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'schema_modifications'
down_revision = 'initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('sensor', sa.Column('umbral_alerta', sa.Float(), nullable=True))
    
    op.add_column('dispositivo', sa.Column('estado_actual', sa.String(), nullable=True))
    
    op.alter_column('dispositivo', 'ubicacion', new_column_name='descripcion_ubicacion')
    op.add_column('dispositivo', sa.Column('coordenadas_gps', sa.String(), nullable=True))
    
    conn = op.get_bind()
    conn.execute(
        sa.text("""
        UPDATE dispositivo d
        SET estado_actual = subquery.estado
        FROM (
            SELECT DISTINCT ON (dispositivo_id) dispositivo_id, estado
            FROM log_estado_dispositivo
            ORDER BY dispositivo_id, timestamp DESC
        ) AS subquery
        WHERE d.id = subquery.dispositivo_id
        """)
    )


def downgrade() -> None:
    op.drop_column('dispositivo', 'coordenadas_gps')
    
    op.alter_column('dispositivo', 'descripcion_ubicacion', new_column_name='ubicacion')
    
    op.drop_column('dispositivo', 'estado_actual')
    
    op.drop_column('sensor', 'umbral_alerta')