from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database
from models.database import db
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/acoustic_pj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/getCalculate', methods=['POST'])
def Calcuclate():
    width = request.get_json()['width']
    height = request.get_json()['height']
    length = request.get_json()['length']

    width = float(width)
    height = float(height)
    length = float(length)

    right_wall = length * height
    left_wall = length * height
    front_wall = width * height
    behind_wall = width * height

    volume = width*height*length
    total_floor_area = width*length
    total_celling_area = width*length
    total_wall_area = front_wall+behind_wall+right_wall+left_wall
    return jsonify(
        volume=volume,
        total_floor_area= total_floor_area,
        total_celling_area=total_celling_area,
        total_wall_area = total_wall_area
    )


if __name__ == '__main__':
    app.run(debug=True)
