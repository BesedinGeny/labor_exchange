"""Добавлены таблицы Users, Jobs, Responses

Revision ID: e6b667630d8a
Revises: 
Create Date: 2022-08-29 13:58:36.233861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6b667630d8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Идентификатор задачи'),
    sa.Column('email', sa.String(), nullable=True, comment='Email адрес'),
    sa.Column('name', sa.String(), nullable=True, comment='Имя пользователя'),
    sa.Column('hashed_password', sa.String(), nullable=True, comment='Зашифрованный пароль'),
    sa.Column('is_company', sa.Boolean(), nullable=True, comment='Флаг компании'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='Время создания записи'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Идентификатор вакансии'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='Идентификатор пользователя'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('responses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Идентификатор отклика'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='Идентификатор пользователя'),
    sa.Column('job_id', sa.Integer(), nullable=True, comment='Идентификатор вакансии'),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('responses')
    op.drop_table('jobs')
    op.drop_table('users')
    # ### end Alembic commands ###
