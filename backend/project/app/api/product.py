from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product

class ProductResource(Resource):
    def get(self, Item_SKU): #to retrieve a product with given ID
        product = Product.query.get(Item_SKU) #get searches by primary key, else filter_by is used
        
        if product:
            return {"SKU": product.Item_SKU, "Name": product.Item_Name, "Description": product.Item_Description, "Price": product.Item_Price, "Quantity": product.Item_Qty}
        return {"message": "Product not found"}, 404

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
    
    def put(self, Item_SKU):
        parser = reqparse.RequestParser()
        parser.add_argument('Item_Name', type=str, required=False)
        parser.add_argument('Item_Description', type=str, required=False)
        parser.add_argument('Item_Price', type=float, required=False)
        parser.add_argument('Item_Qty', type=int, required=False)
        args = parser.parse_args()

        prod = Product.query.get(Item_SKU)
        
        if not prod:
            return {"message": "product not found"}
        
        if args['Item_Name']:
            prod.Item_Name = args['Item_Name']
        if args['Item_Description']:
            prod.Item_Description = args['Item_Description']
        if args['Item_Price']:
            prod.Item_Price = args['Item_Price']
        if args['Item_Qty']:
            prod.Item_Qty = args['Item_Qty']

        db.session.commit()

        return{'message':'Product entry updated', 'product':{'SKU':prod.Item_SKU, 'Name': prod.Item_Name, 'Desc': prod.Item_Description, 'Price': prod.Item_Price, 'Qty': prod.Item_Qty}}, 200
    
    def delete(self, Item_SKU):
        prod = Product.query.get(Item_SKU)

        if not prod:
            return {'message': 'No such product'}, 404
        
        db.session.delete(prod)
        db.session.commit()

        return {'message': f'Product with SKU {Item_SKU} deleted successfully'}, 200