from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date 


class Product(db.Model):
    __tablename__ = "Product"

    Item_SKU = Column(Integer, primary_key=True)
    Item_Name = Column(String(80), nullable=False)
    Item_Description = Column(String(200), nullable=True)
    Item_Price = Column(Float, nullable=False)
    Item_Qty = Column(Integer, nullable=False)
    purchases = db.relationship("TransactionItem", back_populates="product")

    def total_val(self):
        pricesandqty = Product.query.with_entities(Product.Item_Price, Product.Item_Qty).all()
        sum = 0
        return sum(price * qty for price, qty in pricesandqty)
    
    def validate_price_and_qty(self):
        if self.Item_Price <= 0:
            raise ValueError("Price must be positive")
        if self.Item_Qty < 0:
            raise ValueError("Quantity must be non-negative")