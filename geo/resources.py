from flask import Response
from flask.ext.restful import Resource, fields, marshal_with, abort, reqparse
from geo.models import Title
from geo import app, db

class TitleResource(Resource):

    resource_fields = {'title_number': fields.String, 'extent': fields.String}

    def __init__(self):
        self.parser = reqparse.RequestParser()
        for key, val in TitleResource.resource_fields.items():
            self.parser.add_argument(key, type=str)

    @marshal_with(resource_fields)
    def get(self, title_number):
        title = Title.query.filter_by(title_number=title_number).first()
        if title:
            return title
        else:
            abort(404, message="Title number %s doesn't exist" % title_number)

    def put(self, title_number):
        
        args = self.parser.parse_args()
        existing_title = Title.query.filter_by(title_number=args['title_number']).first()
        extent = geojson.loads(args['extent'])

        status = 201
        if existing_title:
            app.logger.info('Title number %s already exists. Replace with %s' % (args['title_number'], args))
            db.session.delete(existing_title)
            db.session.commit()
            status = 200

        app.logger.info('Create title with args %s' % args)
        title = Title(title_number=args['title_number'], extent=extent)
        db.session.add(title)
        db.session.commit()
        return Response(status=status)

