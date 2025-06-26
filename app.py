from flask import Flask, request, jsonify

app = Flask(__name__)

# Временное хранилище данных
items = {
    1: {"name": "Item 1", "value": 10},
    2: {"name": "Item 2", "value": 20}
}

@app.route('/api/items', methods=['GET'])
def get_all_items():
    return jsonify(items), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"status": "running"}), 200

@app.route('/api/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route('/api/item', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_id = max(items.keys(), default=0) + 1
    items[new_id] = data
    return jsonify({"id": new_id, **data}), 201

@app.route('/api/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in items:
        return jsonify({"error": "Item not found"}), 404
    del items[item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)