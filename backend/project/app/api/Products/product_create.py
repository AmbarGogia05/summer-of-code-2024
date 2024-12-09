from flask import render_template
from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product

class ProductCreateResource(Resource):
    
    def post(self): #to create a new product
        parser = reqparse.RequestParser()
        parser.add_argument('Item_Name', type=str, required=True, help='Item name is required')
        parser.add_argument('Item_Description', type=str, default="")
        parser.add_argument('Item_Price', type=float, required=True, help='Price is required')
        parser.add_argument('Item_Qty', type=int, required=True, help='Please mention quantity')
        args = parser.parse_args()

        new_prod = Product(Item_Name=args['Item_Name'], Item_Description=args['Item_Description'], Item_Price=args['Item_Price'], Item_Qty=args['Item_Qty'])
        
        db.session.add(new_prod)
        db.session.commit()

        return {'message':'Product entry created', 'SKU':new_prod.Item_SKU}, 201