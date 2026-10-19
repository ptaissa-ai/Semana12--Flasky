"""Estrutura inicial da Semana 12: roles, users e emails_enviados.

Revision ID: 20261019_init
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = '20261019_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
    )
    op.create_table(
        'emails_enviados',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('destinatario', sa.String(length=120), nullable=False),
        sa.Column('assunto', sa.String(length=200), nullable=False),
        sa.Column('usuario', sa.String(length=80), nullable=False),
        sa.Column('prontuario', sa.String(length=30), nullable=False),
        sa.Column('nome_aluno', sa.String(length=120), nullable=False),
        sa.Column('data_envio', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade():
    op.drop_table('emails_enviados')
    op.drop_table('users')
    op.drop_table('roles')
