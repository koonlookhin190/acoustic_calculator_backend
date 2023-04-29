from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database

from models.frontwall import FrontWall
from models.behindWall import BehindWall
from models.leftWall import LeftWall
from models.rightWall import RightWall
from models.ceilling import Ceiling
from models.floor import Floor

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

    volume = width * height * length
    total_floor_area = width * length
    total_celling_area = width * length
    total_wall_area = front_wall + behind_wall + right_wall + left_wall
    return jsonify(
        volume=volume,
        total_floor_area=total_floor_area,
        total_celling_area=total_celling_area,
        total_wall_area=total_wall_area
    )


@app.route('/getMaterial', methods=['GET'])
def GetMaterial():
    material = Material.query.all()
    material = Material.read_list(material)
    id = 'Cylence Zandera'
    test = Material.query.filter_by(name=id).first()
    name = test.hz250
    test_serialize = test.serialize
    return jsonify(material)


@app.route('/calculateMaterial', methods=['POST'])
def CalculateMaterial():
    name = request.get_json()['name']
    input = request.get_json()['input']
    selected = request.get_json()['selected']
    input = float(input)

    search = Material.query.filter_by(name=selected).first()
    hz250 = search.hz250
    hz500 = search.hz500
    k1 = search.k1
    k2 = search.k2
    k4 = search.k4
    #
    alpha250 = input * hz250
    alpha500 = input * hz500
    alphak1 = input * k1
    alphak2 = input * k2
    alphak4 = input * k4

    if name == "ผนังด้านหน้า":
        db.session.add(FrontWall(name, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านซ้าย":
        db.session.add(LeftWall(name, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านขวา":
        db.session.add(RightWall(name, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านหลัง":
        db.session.add(BehindWall(name, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "พื้น":
        db.session.add(Floor(name, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "เพดาน":
        db.session.add(Ceiling(name, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    return jsonify({'hz250': hz250,'hz500':hz500,'k1':k1,'k2':k2,'k4':k4}), 200


@app.route('/getFrontWall', methods=['GET'])
def GetFrontWall():
    frontwall = FrontWall.query.all()
    frontwall = FrontWall.read_list(frontwall)
    print(frontwall)
    return jsonify(frontwall)

@app.route('/getLeftWall', methods=['GET'])
def GetLeftWall():
    leftwall = LeftWall.query.all()
    leftwall = LeftWall.read_list(leftwall)
    print(leftwall)
    return jsonify(leftwall)

@app.route('/getRightWall', methods=['GET'])
def GetRightWall():
    rightwall = RightWall.query.all()
    rightwall = RightWall.read_list(rightwall)
    print(rightwall)
    return jsonify(rightwall)

@app.route('/getBehindWall', methods=['GET'])
def GetBehindWall():
    behindwall = BehindWall.query.all()
    behindwall = BehindWall.read_list(behindwall)
    print(behindwall)
    return jsonify(behindwall)

@app.route('/getCeiling', methods=['GET'])
def GetCeiling():
    ceiling = Ceiling.query.all()
    ceiling = Ceiling.read_list(ceiling)
    print(ceiling)
    return jsonify(ceiling)

@app.route('/getFloor', methods=['GET'])
def GetFloor():
    floor = Floor.query.all()
    floor = Floor.read_list(floor)
    print(floor)
    return jsonify(floor)

if __name__ == '__main__':
    app.run(debug=True)
