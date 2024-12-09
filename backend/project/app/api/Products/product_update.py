from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product
from flask import jsonify

class ProductUpdateResource(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Item_SKU', type=str, required=True)
        parser.add_argument('Item_Name', type=str, required=False)
        parser.add_argument('Item_Description', type=str, required=False)
        parser.add_argument('Item_Price', type=float, required=False)
        parser.add_argument('Item_Qty', type=int, required=False)
        args = parser.parse_args()

        prod = Product.query.get(args['Item_SKU'])
        
        if not prod:
            return {"message": "Product not found"}, 404
        
        if args['Item_Name']:
            prod.Item_Name = args['Item_Name']
        if args['Item_Description']:
            prod.Item_Description = args['Item_Description']
        if args['Item_Price']:
            prod.Item_Price = args['Item_Price']
        if args['Item_Qty']:
            prod.Item_Qty = args['Item_Qty']

        db.session.commit()

        return{'message':'Product entry updated', 'product':{'SKU':prod.Item_SKU, 'Name': prod.Item_Name, 'Desc': prod.Item_Description if not None else "", 'Price': prod.Item_Price, 'Qty': prod.Item_Qty}}, 200