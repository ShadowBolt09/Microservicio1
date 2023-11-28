from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL 
from app import mysql

coord_bp = Blueprint('coord_bp', __name__)

@coord_bp.route('/event', methods=['POST'])
def getCordinatesByEvent():
    event_data = request.get_json()
    event_id = event_data['id']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT idBoleto, long_stop.latitude, long_stop.longitude FROM Boletos INNER JOIN identity INNER JOIN identity_company INNER JOIN company INNER JOIN sample INNER JOIN route INNER JOIN long_stop ON Boletos.idUsuario=identity.id AND identity.id=identity_company.identity_id AND identity_company.company_id=company.id AND company.id=sample.company_id AND sample.route_id=route.id AND route.end_stop_id=long_stop.id WHERE idEvento = %s", (event_id,))
    boletos_data = cursor.fetchall()
    cursor.close()

    if boletos_data:
        boletos_dict = [{
            'id_boleto': boleto[0],
            'latitud': boleto[1],
            'longitud': boleto[2]
        } for boleto in boletos_data ]
        return jsonify(boletos_dict)
    else:
        return jsonify({'message': 'Error al obtener los boletos con coordenadas del evento'}), 404
    

@coord_bp.route("/ticket", methods=["POST"])
def getCordinatesByTicket():
    ticket_data = request.get_json()
    ticket_id = ticket_data["id"]

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT long_stop.latitude, long_stop.longitude FROM Boletos INNER JOIN identity INNER JOIN identity_company INNER JOIN company INNER JOIN sample INNER JOIN route INNER JOIN long_stop ON Boletos.idUsuario=identity.id AND identity.id=identity_company.identity_id AND identity_company.company_id=company.id AND company.id=sample.company_id AND sample.route_id=route.id AND route.end_stop_id=long_stop.id WHERE idBoleto = %s",
        (ticket_id,),
    )
    boleto_data = cursor.fetchone()
    cursor.close()

    if boleto_data:
        boleto_dict = {"latitud": boleto_data[0], "longitud": boleto_data[1]}
        return jsonify(boleto_dict)
    else:
        return (
            jsonify(
                {"message": "Error al obtener los boletos con coordenadas del evento"}
            ),
            404,
        )