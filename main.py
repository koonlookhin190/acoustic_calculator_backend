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
        db.session.add(FrontWall(name, selected, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านซ้าย":
        db.session.add(LeftWall(name, selected, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านขวา":
        db.session.add(RightWall(name, selected, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านหลัง":
        db.session.add(BehindWall(name, selected, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "พื้น":
        db.session.add(Floor(name, selected, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "เพดาน":
        db.session.add(Ceiling(name, selected, input, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    return jsonify({'hz250': hz250, 'hz500': hz500, 'k1': k1, 'k2': k2, 'k4': k4}), 200


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


@app.route('/deleteMaterial', methods=['POST'])
def DeleteMaterial():
    name = request.get_json()['name']
    id = request.get_json()['id']

    if name == "ผนังด้านหน้า":
        search = FrontWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "ผนังด้านซ้าย":
        search = LeftWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "ผนังด้านขวา":
        search = RightWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "ผนังด้านหลัง":
        search = BehindWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "พื้น":
        search = Floor.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "เพดาน":
        search = Ceiling.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    return jsonify({'name': name, 'id': id}), 200


@app.route('/calculateAll', methods=['POST'])
def CalculateAll():
    volume = request.get_json()['volume']
    frontwall = FrontWall.query.all()
    frontwall_hz250_total = 0
    frontwall_hz500_total = 0
    frontwall_k1_total = 0
    frontwall_k2_total = 0
    frontwall_k4_total = 0

    for fw in frontwall:
        frontwall_hz250_total += fw.hz250
        frontwall_hz500_total += fw.hz500
        frontwall_k1_total += fw.k1
        frontwall_k2_total += fw.k2
        frontwall_k4_total += fw.k4

    leftwall = LeftWall.query.all()
    leftwall_hz250_total = 0
    leftwall_hz500_total = 0
    leftwall_k1_total = 0
    leftwall_k2_total = 0
    leftwall_k4_total = 0

    for lw in leftwall:
        leftwall_hz250_total += lw.hz250
        leftwall_hz500_total += lw.hz500
        leftwall_k1_total += lw.k1
        leftwall_k2_total += lw.k2
        leftwall_k4_total += lw.k4

    rightwall = RightWall.query.all()
    rightwall_hz250_total = 0
    rightwall_hz500_total = 0
    rightwall_k1_total = 0
    rightwall_k2_total = 0
    rightwall_k4_total = 0

    for rw in rightwall:
        rightwall_hz250_total += rw.hz250
        rightwall_hz500_total += rw.hz500
        rightwall_k1_total += rw.k1
        rightwall_k2_total += rw.k2
        rightwall_k4_total += rw.k4

    rightwall = RightWall.query.all()
    rightwall_hz250_total = 0
    rightwall_hz500_total = 0
    rightwall_k1_total = 0
    rightwall_k2_total = 0
    rightwall_k4_total = 0

    for rw in rightwall:
        rightwall_hz250_total += rw.hz250
        rightwall_hz500_total += rw.hz500
        rightwall_k1_total += rw.k1
        rightwall_k2_total += rw.k2
        rightwall_k4_total += rw.k4

    behindwall = BehindWall.query.all()
    behindwall_hz250_total = 0
    behindwall_hz500_total = 0
    behindwall_k1_total = 0
    behindwall_k2_total = 0
    behindwall_k4_total = 0

    for bw in behindwall:
        behindwall_hz250_total += bw.hz250
        behindwall_hz500_total += bw.hz500
        behindwall_k1_total += bw.k1
        behindwall_k2_total += bw.k2
        behindwall_k4_total += bw.k4

    floor = Floor.query.all()
    floor_hz250_total = 0
    floor_hz500_total = 0
    floor_k1_total = 0
    floor_k2_total = 0
    floor_k4_total = 0

    for f in floor:
        floor_hz250_total += f.hz250
        floor_hz500_total += f.hz500
        floor_k1_total += f.k1
        floor_k2_total += f.k2
        floor_k4_total += f.k4

    ceilling = Ceiling.query.all()
    ceilling_hz250_total = 0
    ceilling_hz500_total = 0
    ceilling_k1_total = 0
    ceilling_k2_total = 0
    ceilling_k4_total = 0

    for ce in ceilling:
        ceilling_hz250_total += ce.hz250
        ceilling_hz500_total += ce.hz500
        ceilling_k1_total += ce.k1
        ceilling_k2_total += ce.k2
        ceilling_k4_total += ce.k4

    final_hz250 = frontwall_hz250_total+leftwall_hz250_total+rightwall_hz250_total+behindwall_hz250_total+floor_hz250_total+ceilling_hz250_total

    final_hz500 = frontwall_hz500_total+leftwall_hz500_total+rightwall_hz500_total+behindwall_hz500_total+floor_hz500_total+ceilling_hz500_total

    final_k1 = frontwall_k1_total + leftwall_k1_total + rightwall_k1_total + behindwall_k1_total + floor_k1_total + ceilling_k1_total

    final_k2 = frontwall_k2_total + leftwall_k2_total + rightwall_k2_total + behindwall_k2_total + floor_k2_total + ceilling_k2_total

    final_k4 = frontwall_k4_total + leftwall_k4_total + rightwall_k4_total + behindwall_k4_total + floor_k4_total + ceilling_k4_total

    at250 = 0.161 * volume / final_hz250
    at250 = round(at250,2)
    at500 = 0.161 * volume / final_hz500
    at500 = round(at500, 2)
    atK1 = 0.161 * volume / final_k1
    atK1 = round(atK1, 2)
    atK2 = 0.161 * volume / final_k2
    atK2 = round(atK2, 2)
    atK4 = 0.161 * volume / final_k4
    atK4 = round(atK4, 2)

    print(at250)
    print(at500)
    print(atK1)
    print(atK2)
    print(atK4)
    return jsonify({'at250': at250, 'at500': at500, 'atK1': atK1, 'atK2': atK2, 'atK4': atK4}), 200


if __name__ == '__main__':
    app.run(debug=True)
