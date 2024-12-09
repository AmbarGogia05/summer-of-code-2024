from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product

class ProductGetResource(Resource):
    def get(self, Item_SKU): #to retrieve a product with given ID
        product = Product.query.get(Item_SKU) #get searches by primary key, else filter_by is used
        
        if product:
            return {"SKU": product.Item_SKU, "Name": product.Item_Name, "Description": product.Item_Description, "Price": product.Item_Price, "Quantity": product.Item_Qty}
        return {"message": "Product not found"}, 404