from flask import Flask
from config import Config
from extensions import mysql, login_manager
from routes import bp as routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(routes_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
