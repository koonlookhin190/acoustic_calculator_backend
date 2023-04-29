from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database
from models.database import db
from models.materialUse import Material
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@127.0.0.1:3306/acoustic_pj'
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
@app.route('/getMaterial', methods=['GET'])
def GetMaterial():
    material = Material.query.all()
    material = Material.read_list(material)
    id = 'Cylence Zandera'
    test = Material.query.filter_by(name=id).first()
    name = test.hz250
    test_serialize = test.serialize
    print(name)
    print(test_serialize)
    print(material)
    return jsonify(material)


if __name__ == '__main__':
    app.run(debug=True)
