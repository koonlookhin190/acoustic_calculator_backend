from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


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
