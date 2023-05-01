from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database

from models import Product
from models.frontwall import FrontWall
from models.behindWall import BehindWall
from models.leftWall import LeftWall
from models.productFrontWall import ProductFrontWall
from models.productLeftWall import ProductLeftWall
from models.productRightWall import ProductRightWall
from models.productBehindWall import ProductBehindWall
from models.productFloor import ProductFloor
from models.productCeiling import ProductCeiling
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
        total_wall_area=total_wall_area,
        right_wall = right_wall,
        left_wall = left_wall,
        front_wall = front_wall,
        behind_wall = behind_wall
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


@app.route('/getProduct', methods=['GET'])
def GetProduct():
    product = Product.query.all()
    product = Product.read_list(product)
    return jsonify(product)


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


@app.route('/calculateProduct', methods=['POST'])
def CalculateProduct():
    name = request.get_json()['name']
    selected = request.get_json()['selected']
    material = request.get_json()['material']
    search = Product.query.filter_by(name=selected).first()
    hz250 = search.hz250
    hz500 = search.hz500
    area = search.area
    k1 = search.k1
    k2 = search.k2
    k4 = search.k4
    #
    alpha250 = area * hz250
    alpha500 = area * hz500
    alphak1 = area * k1
    alphak2 = area * k2
    alphak4 = area * k4

    if name == "ผนังด้านหน้า":
        db.session.add(ProductFrontWall(name, selected, area,material, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านซ้าย":
        db.session.add(ProductLeftWall(name, selected, area,material, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านขวา":
        db.session.add(ProductRightWall(name, selected, area,material, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "ผนังด้านหลัง":
        db.session.add(ProductBehindWall(name, selected, area,material, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "พื้น":
        db.session.add(ProductFloor(name, selected, area,material, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    if name == "เพดาน":
        db.session.add(ProductCeiling(name, selected, area,material, alpha250, alpha500, alphak1, alphak2, alphak4))
        db.session.commit()
    return jsonify({'hz250': hz250, 'hz500': hz500, 'k1': k1, 'k2': k2, 'k4': k4}), 200


@app.route('/getProductFrontWall', methods=['GET'])
def GetProductFrontWall():
    frontwall = ProductFrontWall.query.all()
    frontwall = ProductFrontWall.read_list(frontwall)
    print(frontwall)
    return jsonify(frontwall)


@app.route('/getProductLeftWall', methods=['GET'])
def GetProductLeftWall():
    leftwall = ProductLeftWall.query.all()
    leftwall = ProductLeftWall.read_list(leftwall)
    print(leftwall)
    return jsonify(leftwall)


@app.route('/getProductRightWall', methods=['GET'])
def GetProductRightWall():
    rightwall = ProductRightWall.query.all()
    rightwall = ProductRightWall.read_list(rightwall)
    print(rightwall)
    return jsonify(rightwall)


@app.route('/getProductBehindWall', methods=['GET'])
def GetProductBehindWall():
    behindwall = ProductBehindWall.query.all()
    behindwall = ProductBehindWall.read_list(behindwall)
    print(behindwall)
    return jsonify(behindwall)


@app.route('/getProductCeiling', methods=['GET'])
def GetProductCeiling():
    ceiling = ProductCeiling.query.all()
    ceiling = ProductCeiling.read_list(ceiling)
    print(ceiling)
    return jsonify(ceiling)


@app.route('/getProductFloor', methods=['GET'])
def GetProductFloor():
    floor = ProductFloor.query.all()
    floor = ProductFloor.read_list(floor)
    print(floor)
    return jsonify(floor)


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


@app.route('/deleteProduct', methods=['POST'])
def DeleteProduct():
    name = request.get_json()['name']
    id = request.get_json()['id']

    if name == "ผนังด้านหน้า":
        search = ProductFrontWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "ผนังด้านซ้าย":
        search = ProductLeftWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "ผนังด้านขวา":
        search = ProductRightWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "ผนังด้านหลัง":
        search = ProductBehindWall.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "พื้น":
        search = ProductFloor.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
    if name == "เพดาน":
        search = ProductCeiling.query.filter_by(id=id).first()
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

    final_hz250 = frontwall_hz250_total + leftwall_hz250_total + rightwall_hz250_total + behindwall_hz250_total + floor_hz250_total + ceilling_hz250_total

    final_hz500 = frontwall_hz500_total + leftwall_hz500_total + rightwall_hz500_total + behindwall_hz500_total + floor_hz500_total + ceilling_hz500_total

    final_k1 = frontwall_k1_total + leftwall_k1_total + rightwall_k1_total + behindwall_k1_total + floor_k1_total + ceilling_k1_total

    final_k2 = frontwall_k2_total + leftwall_k2_total + rightwall_k2_total + behindwall_k2_total + floor_k2_total + ceilling_k2_total

    final_k4 = frontwall_k4_total + leftwall_k4_total + rightwall_k4_total + behindwall_k4_total + floor_k4_total + ceilling_k4_total

    at250 = 0.161 * volume / final_hz250
    at250 = round(at250, 2)
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


@app.route('/calculatePro', methods=['POST'])
def CalculatePro():
    volume = request.get_json()['volume']
    frontwall = FrontWall.query.all()
    frontwall_area = 0
    frontwall_hz250_total = 0
    frontwall_hz500_total = 0
    frontwall_k1_total = 0
    frontwall_k2_total = 0
    frontwall_k4_total = 0

    for fw in frontwall:
        frontwall_area += fw.input
        frontwall_hz250_total += fw.hz250
        frontwall_hz500_total += fw.hz500
        frontwall_k1_total += fw.k1
        frontwall_k2_total += fw.k2
        frontwall_k4_total += fw.k4

    leftwall = LeftWall.query.all()
    leftwall_area = 0
    leftwall_hz250_total = 0
    leftwall_hz500_total = 0
    leftwall_k1_total = 0
    leftwall_k2_total = 0
    leftwall_k4_total = 0

    for lw in leftwall:
        leftwall_area += lw.input
        leftwall_hz250_total += lw.hz250
        leftwall_hz500_total += lw.hz500
        leftwall_k1_total += lw.k1
        leftwall_k2_total += lw.k2
        leftwall_k4_total += lw.k4

    rightwall = RightWall.query.all()
    rightwall_area = 0
    rightwall_hz250_total = 0
    rightwall_hz500_total = 0
    rightwall_k1_total = 0
    rightwall_k2_total = 0
    rightwall_k4_total = 0

    for rw in rightwall:
        rightwall_area += rw.input
        rightwall_hz250_total += rw.hz250
        rightwall_hz500_total += rw.hz500
        rightwall_k1_total += rw.k1
        rightwall_k2_total += rw.k2
        rightwall_k4_total += rw.k4

    behindwall = BehindWall.query.all()
    behindwall_area = 0
    behindwall_hz250_total = 0
    behindwall_hz500_total = 0
    behindwall_k1_total = 0
    behindwall_k2_total = 0
    behindwall_k4_total = 0

    for bw in behindwall:
        behindwall_area += bw.input
        behindwall_hz250_total += bw.hz250
        behindwall_hz500_total += bw.hz500
        behindwall_k1_total += bw.k1
        behindwall_k2_total += bw.k2
        behindwall_k4_total += bw.k4

    floor = Floor.query.all()
    floor_area = 0
    floor_hz250_total = 0
    floor_hz500_total = 0
    floor_k1_total = 0
    floor_k2_total = 0
    floor_k4_total = 0

    for f in floor:
        floor_area += f.input
        floor_hz250_total += f.hz250
        floor_hz500_total += f.hz500
        floor_k1_total += f.k1
        floor_k2_total += f.k2
        floor_k4_total += f.k4

    ceilling = Ceiling.query.all()
    ceilling_area = 0
    ceilling_hz250_total = 0
    ceilling_hz500_total = 0
    ceilling_k1_total = 0
    ceilling_k2_total = 0
    ceilling_k4_total = 0

    for ce in ceilling:
        ceilling_area += ce.input
        ceilling_hz250_total += ce.hz250
        ceilling_hz500_total += ce.hz500
        ceilling_k1_total += ce.k1
        ceilling_k2_total += ce.k2
        ceilling_k4_total += ce.k4
    # -------------------------------------------------
    profrontwall = ProductFrontWall.query.all()
    profrontwall_hz250_total = 0
    profrontwall_hz500_total = 0
    profrontwall_k1_total = 0
    profrontwall_k2_total = 0
    profrontwall_k4_total = 0
    profrontwall_alpha250 = 0
    profrontwall_alpha500 = 0
    profrontwall_alphak1 = 0
    profrontwall_alphak2 = 0
    profrontwall_alphak4 = 0
    keep_allarea = 0
    for fw in profrontwall:
        search = FrontWall.query.filter_by(selected=fw.material).first()
        area = search.input
        keepinput = 0
        for r in profrontwall:
            if fw.material == r.material:
                keepinput += r.input

        area = area - keepinput
        keep_allarea += area
        keep_allarea += keepinput
        search2 = Material.query.filter_by(name=fw.material).first()
        hz250 = search2.hz250
        hz500 = search2.hz500
        k1 = search2.k1
        k2 = search2.k2
        k4 = search2.k4
        if keep_allarea <= frontwall_area:
            print(keep_allarea)
            profrontwall_alpha250 = profrontwall_alpha250+(area * hz250)
            profrontwall_alpha500 = profrontwall_alpha500+(area * hz500)
            profrontwall_alphak1 = profrontwall_alphak1+(area * k1)
            profrontwall_alphak2 = profrontwall_alphak2+(area * k2)
            profrontwall_alphak4 = profrontwall_alphak4+(area * k4)

        profrontwall_hz250_total += fw.hz250
        profrontwall_hz500_total += fw.hz500
        profrontwall_k1_total += fw.k1
        profrontwall_k2_total += fw.k2
        profrontwall_k4_total += fw.k4

    proleftwall = ProductLeftWall.query.all()
    proleftwall_hz250_total = 0
    proleftwall_hz500_total = 0
    proleftwall_k1_total = 0
    proleftwall_k2_total = 0
    proleftwall_k4_total = 0
    proleftwall_alpha250 = 0
    proleftwall_alpha500 = 0
    proleftwall_alphak1 = 0
    proleftwall_alphak2 = 0
    proleftwall_alphak4 = 0
    keep_allarea2 = 0

    for lw in proleftwall:
        search = LeftWall.query.filter_by(selected=lw.material).first()
        area = search.input
        keepinput = 0
        for r in proleftwall:
            if lw.material == r.material:
                keepinput += r.input

        area = area - keepinput
        keep_allarea2 += area
        keep_allarea2 += keepinput
        search2 = Material.query.filter_by(name=lw.material).first()
        hz250 = search2.hz250
        hz500 = search2.hz500
        k1 = search2.k1
        k2 = search2.k2
        k4 = search2.k4
        print(keep_allarea2)
        if keep_allarea2 <= leftwall_area:
            proleftwall_alpha250 += area * hz250
            proleftwall_alpha500 = proleftwall_alpha500 + (area * hz500)
            proleftwall_alphak1 = proleftwall_alphak1 + (area * k1)
            proleftwall_alphak2 = proleftwall_alphak2 + (area * k2)
            proleftwall_alphak4 = proleftwall_alphak4 + (area * k4)

        proleftwall_hz250_total += lw.hz250
        proleftwall_hz500_total += lw.hz500
        proleftwall_k1_total += lw.k1
        proleftwall_k2_total += lw.k2
        proleftwall_k4_total += lw.k4

    prorightwall = ProductRightWall.query.all()
    prorightwall_hz250_total = 0
    prorightwall_hz500_total = 0
    prorightwall_k1_total = 0
    prorightwall_k2_total = 0
    prorightwall_k4_total = 0
    prorightwall_alpha250 = 0
    prorightwall_alpha500 = 0
    prorightwall_alphak1 = 0
    prorightwall_alphak2 = 0
    prorightwall_alphak4 = 0
    keep_allarea3 = 0
    for rw in prorightwall:
        search = RightWall.query.filter_by(selected=rw.material).first()
        area = search.input
        keepinput = 0
        for r in prorightwall:
            if rw.material == r.material:
                keepinput += r.input

        area = area - keepinput
        keep_allarea3 += area
        keep_allarea3 += keepinput
        search2 = Material.query.filter_by(name=rw.material).first()
        hz250 = search2.hz250
        hz500 = search2.hz500
        k1 = search2.k1
        k2 = search2.k2
        k4 = search2.k4
        if keep_allarea3 <= rightwall_area:
            print(keep_allarea3)
            prorightwall_alpha250 = prorightwall_alpha250 + (area * hz250)
            prorightwall_alpha500 = prorightwall_alpha500 + (area * hz500)
            prorightwall_alphak1 = prorightwall_alphak1 + (area * k1)
            prorightwall_alphak2 = prorightwall_alphak2 + (area * k2)
            prorightwall_alphak4 = prorightwall_alphak4 + (area * k4)

        prorightwall_hz250_total += rw.hz250
        prorightwall_hz500_total += rw.hz500
        prorightwall_k1_total += rw.k1
        prorightwall_k2_total += rw.k2
        prorightwall_k4_total += rw.k4

    probehindwall = ProductBehindWall.query.all()
    probehindwall_hz250_total = 0
    probehindwall_hz500_total = 0
    probehindwall_k1_total = 0
    probehindwall_k2_total = 0
    probehindwall_k4_total = 0
    probehindwall_alpha250 = 0
    probehindwall_alpha500 = 0
    probehindwall_alphak1 = 0
    probehindwall_alphak2 = 0
    probehindwall_alphak4 = 0
    keep_allarea4 = 0
    for bw in probehindwall:
        search = BehindWall.query.filter_by(selected=bw.material).first()
        area = search.input
        keepinput = 0
        for r in probehindwall:
            if bw.material == r.material:
                keepinput += r.input

        area = area - keepinput
        keep_allarea4 += area
        keep_allarea4 += keepinput
        search2 = Material.query.filter_by(name=bw.material).first()
        hz250 = search2.hz250
        hz500 = search2.hz500
        k1 = search2.k1
        k2 = search2.k2
        k4 = search2.k4
        if keep_allarea4 <= behindwall_area:
            print(keep_allarea4)
            probehindwall_alpha250 = probehindwall_alpha250 + (area * hz250)
            probehindwall_alpha500 = probehindwall_alpha500 + (area * hz500)
            probehindwall_alphak1 = probehindwall_alphak1 + (area * k1)
            probehindwall_alphak2 = probehindwall_alphak2 + (area * k2)
            probehindwall_alphak4 = probehindwall_alphak4 + (area * k4)

        probehindwall_hz250_total += bw.hz250
        probehindwall_hz500_total += bw.hz500
        probehindwall_k1_total += bw.k1
        probehindwall_k2_total += bw.k2
        probehindwall_k4_total += bw.k4

    profloor = ProductFloor.query.all()
    profloor_hz250_total = 0
    profloor_hz500_total = 0
    profloor_k1_total = 0
    profloor_k2_total = 0
    profloor_k4_total = 0
    profloor_alpha250 = 0
    profloor_alpha500 = 0
    profloor_alphak1 = 0
    profloor_alphak2 = 0
    profloor_alphak4 = 0
    keep_allarea5 = 0
    for fl in profloor:
        search = Floor.query.filter_by(selected=fl.material).first()
        area = search.input
        keepinput = 0
        for r in profloor:
            if fl.material == r.material:
                keepinput += r.input

        area = area - keepinput
        keep_allarea5 += area
        keep_allarea5 += keepinput
        search2 = Material.query.filter_by(name=fl.material).first()
        hz250 = search2.hz250
        hz500 = search2.hz500
        k1 = search2.k1
        k2 = search2.k2
        k4 = search2.k4
        if keep_allarea5 <= floor_area:
            print(keep_allarea5)
            profloor_alpha250 = profloor_alpha250 + (area * hz250)
            profloor_alpha500 = profloor_alpha500 + (area * hz500)
            profloor_alphak1 = profloor_alphak1 + (area * k1)
            profloor_alphak2 = profloor_alphak2 + (area * k2)
            profloor_alphak4 = profloor_alphak4 + (area * k4)

        profloor_hz250_total += fl.hz250
        profloor_hz500_total += fl.hz500
        profloor_k1_total += fl.k1
        profloor_k2_total += fl.k2
        profloor_k4_total += fl.k4

    proceilling = ProductCeiling.query.all()
    proceilling_hz250_total = 0
    proceilling_hz500_total = 0
    proceilling_k1_total = 0
    proceilling_k2_total = 0
    proceilling_k4_total = 0
    proceilling_alpha250 = 0
    proceilling_alpha500 = 0
    proceilling_alphak1 = 0
    proceilling_alphak2 = 0
    proceilling_alphak4 = 0
    keep_allarea6 = 0
    for ce in proceilling:
        search = Ceiling.query.filter_by(selected=ce.material).first()
        area = search.input
        keepinput = 0
        for r in proceilling:
            if ce.material == r.material:
                keepinput += r.input

        area = area - keepinput
        keep_allarea6 += area
        keep_allarea6 += keepinput
        search2 = Material.query.filter_by(name=ce.material).first()
        hz250 = search2.hz250
        hz500 = search2.hz500
        k1 = search2.k1
        k2 = search2.k2
        k4 = search2.k4
        if keep_allarea6 <= ceilling_area:
            print(keep_allarea6)
            proceilling_alpha250 = proceilling_alpha250 + (area * hz250)
            proceilling_alpha500 = proceilling_alpha500 + (area * hz500)
            proceilling_alphak1 = proceilling_alphak1 + (area * k1)
            proceilling_alphak2 = proceilling_alphak2 + (area * k2)
            proceilling_alphak4 = proceilling_alphak4 + (area * k4)

        print("Text4")
        print(proceilling_alpha250)
        proceilling_hz250_total += ce.hz250
        proceilling_hz500_total += ce.hz500
        proceilling_k1_total += ce.k1
        proceilling_k2_total += ce.k2
        proceilling_k4_total += ce.k4


    profinal_hz250 = profrontwall_hz250_total + proleftwall_hz250_total + prorightwall_hz250_total + probehindwall_hz250_total + profloor_hz250_total + proceilling_hz250_total
    print("text")
    print(profinal_hz250)
    profinal_hz500 = profrontwall_hz500_total + proleftwall_hz500_total + prorightwall_hz500_total + probehindwall_hz500_total + profloor_hz500_total + proceilling_hz500_total
    print("text77")
    print(profinal_hz500)
    profinal_k1 = profrontwall_k1_total + proleftwall_k1_total + prorightwall_k1_total + probehindwall_k1_total + profloor_k1_total + proceilling_k1_total

    profinal_k2 = profrontwall_k2_total + proleftwall_k2_total + prorightwall_k2_total + probehindwall_k2_total + profloor_k2_total + proceilling_k2_total

    profinal_k4 = profrontwall_k4_total + proleftwall_k4_total + prorightwall_k4_total + probehindwall_k4_total + profloor_k4_total + proceilling_k4_total

    finalAlpa250 = profrontwall_alpha250 + proleftwall_alpha250 + prorightwall_alpha250 + probehindwall_alpha250 + profloor_alpha250 + proceilling_alpha250

    print(finalAlpa250)
    finalAlpa500 = profrontwall_alpha500 + proleftwall_alpha500 + prorightwall_alpha500 + probehindwall_alpha500 + profloor_alpha500 + proceilling_alpha500
    print(finalAlpa500)
    print("text2")
    finalAlpa1k = profrontwall_alphak1 + proleftwall_alphak1 + prorightwall_alphak1 + probehindwall_alphak1 + profloor_alphak1 + proceilling_alphak1

    finalAlpa2k = profrontwall_alphak2 + proleftwall_alphak2 + prorightwall_alphak2 + probehindwall_alphak2 + profloor_alphak2 + proceilling_alphak2
    finalAlpa4k = profrontwall_alphak4 + proleftwall_alphak4 + prorightwall_alphak4 + probehindwall_alphak4 + profloor_alphak4 + proceilling_alphak4

    print("text3")
    plusat250 = finalAlpa250+profinal_hz250
    print(plusat250)
    dividedat250 = volume/plusat250
    at250 = 0.161 * dividedat250
    at250 = round(at250, 2)
    plusat500 = finalAlpa500+profinal_hz500
    dividedat500 = volume / plusat500
    at500 = 0.161 * dividedat500
    print("rt500")
    print(at500)
    at500 = round(at500, 2)
    plusat1k = finalAlpa1k + profinal_k1
    dividedat1k = volume / plusat1k
    at1k = 0.161 * dividedat1k
    at1k = round(at1k, 2)
    plusat2k = finalAlpa2k + profinal_k2
    dividedat2k = volume / plusat2k
    at2k = 0.161 * dividedat2k
    at2k = round(at2k, 2)
    plusat4k = finalAlpa4k + profinal_k4
    dividedat4k = volume / plusat4k
    at4k = 0.161 * dividedat4k
    at4k = round(at4k, 2)

    return jsonify({'at250': at250, 'at500': at500, 'atK1': at1k, 'atK2': at2k, 'atK4': at4k}), 200


if __name__ == '__main__':
    app.run(debug=True)
