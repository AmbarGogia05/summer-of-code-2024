from flask import Blueprint, render_template
from flask_restful import Api
from .Products.product_create import ProductCreateResource
from .Products.product_delete import ProductDeleteResource
from .Products.product_get import ProductGetResource
from .Products.product_update import ProductUpdateResource

#import resource classes here

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(ProductGetResource, '/products/get')
api.add_resource(ProductCreateResource, '/products/add')
api.add_resource(ProductDeleteResource, '/products/delete')
api.add_resource(ProductUpdateResource, '/products/update')

@api_blueprint.route('/products/add')
def product_add():
    return render_template("product_add.html")

@api_blueprint.route('/products/update')
def product_update():
    return render_template("product_update.html")

@api_blueprint.route('/products/delete')
def product_delete():
    return render_template("product_delete.html")

@api_blueprint.route('/products/view', methods=['GET'])
def product_query():
    return render_template("product_get.html")