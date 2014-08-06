from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from geo.models import *

from geo import app, db
app.config.from_object(os.environ['SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()