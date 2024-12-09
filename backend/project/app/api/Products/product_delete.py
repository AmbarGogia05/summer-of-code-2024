from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product

class ProductDeleteResource(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Item_SKU', type=int, required=True)
        args = parser.parse_args()

        prod = Product.query.get(args['Item_SKU'])

        if not prod:
            return {'message': 'No such product'}, 404
        
        db.session.delete(prod)
        db.session.commit()

        return {'message': f'Product with SKU {args["Item_SKU"]} deleted successfully'}, 200