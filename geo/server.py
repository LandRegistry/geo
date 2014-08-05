from flask import jsonify,  abort, request, make_response
from geo import app, api
from geo import resources
from geo.models import Title

@app.route('/', methods=['GET'])
def index():
    return "Geo OK"

api.add_resource(resources.TitleResource, '/titles/<string:title_number>')
api.add_resource(resources.TitleListResource, '/titles')