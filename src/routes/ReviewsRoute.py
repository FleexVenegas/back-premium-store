from flask import Blueprint, request, jsonify
from flask_cors import CORS
from utilities.Tools import Tools

# Modelos
from models.ReviewsModel import ReviewsModel

#Intities
from models.entities.Reviews import Reviews


import uuid


main = Blueprint("reviews_blueprint", __name__)
CORS(main, supports_credentials=True)


@main.route('/', methods=['POST'])
def add_review():
    try:
        dataReview_str = request.form['dataReview']
        dataReview_json = Tools.convert_json(dataReview_str)

        if 'file' not in request.files:
            return jsonify({"message": "Not file"})
        
          # Verificamos si los datos no llegan vacios o en None
        if all(value is not None and value != '' for value in dataReview_json.values()):

            reviewID = uuid.uuid4()

            # Obtenemos el file
            _file = request.files['file']

            # Le pasamos los datos al modelo
            review = Reviews(str(reviewID), **dataReview_json)

            affected_row = ReviewsModel.add_review(review, _file)

            if affected_row == 1:
                return jsonify({"message": "Review successfully added"}), 200
            
            return jsonify({'message': "Error en agregar los datos a la base de datos"}), 500

    except Exception as ex:
        return jsonify(str(ex))
    

@main.route('/', methods=['GET'])
def get_reviews():
    try:
        reviews = ReviewsModel.get_reviews()
        return jsonify({"message": "ok", "data": reviews, "status": 200}), 200

    except Exception as ex:
        return jsonify(str(ex)), 500