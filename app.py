from flask import Flask
from application.database import db


app=None   #for local module scoping

def create_app():          # for better confiurations
    app=Flask(__name__)
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///lmsdata.sqlite3"
    db.init_app(app)
    app.app_context().push()

    return app

app=create_app()   # from None now its done

from application.controllers import *
#from application.models import *

if __name__=="__main__":
    app.run()