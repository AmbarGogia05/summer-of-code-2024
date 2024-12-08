from flask import Blueprint
from flask_restful import Api
from .product import ProductResource
#import resource classes here

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(ProductResource, '/products', '/products/<int:Item_SKU>')

#register API resources below