# database models
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
	pass


class ProductType(Base):
	"""Тип продукта"""
	__tablename__ = 'product_type'

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
	name: Mapped[str]

	products: Mapped[list["Product"]] = relationship(
		back_populates='product_type',
		primaryjoin='and_(ProductType.id == Product.product_type_id)',
		order_by='Product.id.asc()'
	)


class Product(Base):
	"""Представление продукта"""
	__tablename__ = 'product'

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
	name: Mapped[str]

	# Связь с ProductType
	product_type_id: Mapped[int] = mapped_column(ForeignKey('product_type.id', ondelete='CASCADE'))
	product_type: Mapped["ProductType"] = relationship(back_populates='products', lazy='joined')
