from flask_restful import reqparse, Resource
from app.models import db
from app.models.product import Product

class ProductGetResource(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('Item_Name', type=str, location='args')
        parser.add_argument('Item_SKU', type=int, location='args')
        args = parser.parse_args()

        if args["Item_SKU"] and not args["Item_Name"]:
            product = Product.query.get(args["Item_SKU"])
            if product:
                return {"message": {"SKU": product.Item_SKU, "Name": product.Item_Name, "Description": product.Item_Description, "Price": product.Item_Price, "Quantity": product.Item_Qty}}, 200

        elif args["Item_Name"] and not args["Item_SKU"]:
            products = Product.query.filter_by(Item_Name=args["Item_Name"]).all()
            if products:
                if len(products) == 1:
                    product = products[0]
                    return {"message": {"SKU": product.Item_SKU, "Name": product.Item_Name, "Description": product.Item_Description, "Price": product.Item_Price, "Quantity": product.Item_Qty}}, 200
                else:
                    result = {i+1: {"SKU": item.Item_SKU, "Name": item.Item_Name, "Description": item.Item_Description, "Price": item.Item_Price, "Quantity": item.Item_Qty} for i, item in enumerate(products)}
                    return {"message": result}, 200

        elif args["Item_Name"] and args["Item_SKU"]:
            product = Product.query.filter_by(Item_Name=args["Item_Name"], Item_SKU=args["Item_SKU"]).first()
            if product:
                return {"message": {"SKU": product.Item_SKU, "Name": product.Item_Name, "Description": product.Item_Description, "Price": product.Item_Price, "Quantity": product.Item_Qty}}, 200

        return {"message": "Product not found"}, 404
