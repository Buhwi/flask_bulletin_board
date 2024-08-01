from flask import Flask, g
from extensions import login_manager
import pymysql
from config import Config
from routes import bp as routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    def get_db():
        if 'db' not in g:
            g.db = pymysql.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                db=app.config['MYSQL_DB'],
                cursorclass=pymysql.cursors.DictCursor
            )
        return g.db

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    app.get_db = get_db
    app.register_blueprint(routes_bp, url_prefix='/')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)