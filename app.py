from flask import Flask
from flask_mysqldb import MySQL 
from flask_cors import CORS
import os

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuración de la base de datos
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'srv_user'
    app.config['MYSQL_PASSWORD'] = '666'
    app.config['MYSQL_DB'] = 'Conciertos2'

    # Inicializa MySQL con la aplicación
    mysql.init_app(app)

    # Registrar los blueprints
    from controllers.mainController import coord_bp
    app.register_blueprint(coord_bp, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

