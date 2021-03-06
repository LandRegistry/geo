from flask import Response
from flask.ext.restful import Resource, fields, marshal_with, abort, reqparse
from geo import models
from geo import app, db
from sqlalchemy.exc import DataError


class TitleListResource(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str, location='args')

        super(TitleListResource, self).__init__()

    def get(self):

        args = self.parser.parse_args()
        result = []

        method = args.get('method', None)
        location = args.get('location', None)

        if method == 'near':
            titles =  models.Title.query.all()
        else:
            titles =  models.Title.query.all()

        for title in titles:
            result.append(title.to_dict())

        return result


class TitleResource(Resource):

    resource_fields = {'title_number': fields.String, 'extent': fields.String}

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('extent', type=str, location='json')

        super(TitleResource, self).__init__()

    def get(self, title_number):

        title = models.Title.query.filter_by(title_number=title_number).first()
        if title:
            return title.to_dict()
        else:
            abort(404, message="Title number %s doesn't exist" % title_number)


    def put(self, title_number):

        app.logger.info("PUTing a title")

        status = 201
        args = self.parser.parse_args()

        #try and get existing title, create if not
        title = models.Title.query.filter_by(title_number=title_number).first()
        if not title:
            app.logger.info("Title number does not exist, creating a new one")
            status = 200
            title = models.Title()
            title.title_number = title_number

        #set extent from geojson
        title.set_extent_from_geojson(args['extent'])
        try:
            db.session.add(title)
            db.session.commit()
        except DataError:
            status = 400
        return None, status

