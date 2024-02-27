import uuid
import cloudinary.uploader
from flask_cors import CORS, cross_origin
from flask import Blueprint, jsonify, request

# Models
from models.FragranceModel import PerfumeRegistry

# CLoud
from cloud.Cloud import CloudConfig

# Intities
from models.entities.Fragrance import Fragrance

# Utilies
from utilities.Tools import Tools

main = Blueprint("fragrance_blueprint", __name__)
CORS(main, supports_credentials=True)

CloudConfig.get_connection_cloud()



@main.route('/', methods=['POST'])
def add_perfume():
    try:

        datas_perfume = request.form['data_perfume']

        # Convertimos en json
        datasPerfume = Tools.convert_json(datas_perfume)

        # Verificamos si hay una archivo .png etc
        if 'file' not in request.files:
            return jsonify({"message": "Not file"})
        
        # Verificamos si los datos no llegan vacios o en None
        if all(value is not None and value != '' for value in datasPerfume.values()):
        
            # Obtenemos el archivo
            _file = request.files['file']

            # Lo subimos a cloudinary
            cloud_path = cloudinary.uploader.upload(_file, folder='uploads')
            
            #Obtenemos la url del archivo y lo agregamos al dict
            datasPerfume.update({
                "imageURL": cloud_path.get('secure_url', ''),
                "public_id": cloud_path.get('public_id', '')
            })

            # Generamos un ID único
            perfumeID = uuid.uuid4()

            perfume_model = Fragrance(str(perfumeID), **datasPerfume)

            affected_row = PerfumeRegistry.add_perfume(perfume_model)

            if affected_row == 1:
                return jsonify({"message": "Perfume agregado con exito"}), 200
            
            else:
                return jsonify({"message": "Error en guardar el perfume"}), 50000
            
        else:
            return jsonify({"message": "Los datos estan vacios", "error": 400}), 400

    except Exception as ex:
        return jsonify({"message": str(ex)})
    


@main.route('/<id>', methods=['GET'])
def get_perfume(id):
    try:
        perfume = PerfumeRegistry.get_perfume(id)

        if perfume != None:
            return jsonify({"message": "OK", "status": 200, "data": perfume}), 200
        
        return jsonify({"message": "Error en obtener los datos de la base de datos"})
    
    except Exception as ex:
        return jsonify({"message": str(ex)})
    


@main.route('/type/<gender>', methods=['GET'])
def get_perfumeGender(gender):
    try:
        perfume = PerfumeRegistry.get_perfume_gender(gender)

        if perfume != None:
            return jsonify({"message": "OK", "status": 200, "data": perfume}), 200
        
        return jsonify({"message": "Error en obtener los datos de la base de datos"})
    
    except Exception as ex:
        return jsonify({"message": str(ex)})
    


@main.route('/', methods=['GET'])
def get_perfumes():
    try:
        perfume = PerfumeRegistry.get_perfumes()

        if perfume:
            return jsonify({"message": "OK", "status": 200, "data": perfume}), 200

        return jsonify({"message": "No hay datos que mostrar", "data": []}), 200

    except Exception as ex:
        return jsonify({"message": "Error en obtener los datos de la base de datos", "error": str(ex)}), 500
    



@main.route('/top', methods=['GET'])
def get_perfumes_top():
    try:
        perfume_top = PerfumeRegistry.get_perfumes_top()

        if perfume_top:
            return jsonify({"message": "OK", "status": 200, "data": perfume_top}), 200

        return jsonify({"message": "No hay datos que mostrar", "data": []}), 200

    except Exception as ex:
        return jsonify({"message": "Error en obtener los datos de la base de datos", "error": str(ex)}), 500

    
@main.route('/<id>', methods=['DELETE'])
def delete_perfume(id):
    try:

        affected_row = PerfumeRegistry.delete_perfume(id)

        if affected_row == 1:
            return jsonify({"message": "Registro eliminado correctamente"}), 200

        return jsonify({"message": "Error en eliminar el registro"}),  500
    
    except Exception as ex:
        return jsonify({"message": str(ex)})
    

    
@main.route('/<id>', methods=['PUT'])
def update_perfume(id):
    try:

        datas_string = request.form['data_perfume']
        datas_json = Tools.convert_json(datas_string)

        #Obtenemos el archivo, si existe alguno
        _file = None
        if 'file' in request.files:
            _file = request.files['file']

        if all(value is not None and value != '' for value in datas_json.values()):
            perfume = Fragrance(id, **datas_json)

            affected_row = PerfumeRegistry.update_perfume(perfume, _file)

            if affected_row == 1:
                return jsonify({"message": "Registro actualizado correctamente"}), 200
            
            elif affected_row == 0:
                return jsonify({"message": "No hay cambios realizados"}), 304

            else:
                return jsonify({"message": "No es posible realizar los cambios"}), 500
      
    except Exception as ex:
        return jsonify(str(ex))