from flask import Flask, request, jsonify

app = Flask(__name__)

# Временное хранилище данных
items = {
    1: {"name": "Course 1", "teacher": "Ivan", "longitude": 64, "status": "active", "max_numb_students": 20},
    2: {"name": "Course 2", "teacher": "Kolya", "longitude": 100, "status": "active", "max_numb_students": 25},
    3: {"name": "Course 3", "teacher": "Masha", "longitude": 333, "status": "inactive", "max_numb_students": 100}
}

@app.route('/courses', methods=['GET'])
def get_all_items():
    return jsonify(items), 200

@app.route('/courses/active', methods=['GET'])
def get_active_items():
    active_items = {k: v for k, v in items.items() if v['status'] == 'active'}
    return jsonify(active_items), 200

@app.route('/courses/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(item), 200

@app.route('/courses', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data or 'teacher' not in data or 'longitude' not in data or 'status' not in data or 'max_numb_students' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_id = max(items.keys(), default=0) + 1
    items[new_id] = data
    return jsonify({"id": new_id, **data}), 201

@app.route('/courses/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in items:
        return jsonify({"error": "Course not found"}), 404
    del items[item_id]
    return jsonify({"message": "Course deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)