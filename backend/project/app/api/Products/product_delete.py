from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product

class ProductDeleteResource(Resource):
    def delete(self, Item_SKU):
        prod = Product.query.get(Item_SKU)

        if not prod:
            return {'message': 'No such product'}, 404
        
        db.session.delete(prod)
        db.session.commit()

        return {'message': f'Product with SKU {Item_SKU} deleted successfully'}, 200