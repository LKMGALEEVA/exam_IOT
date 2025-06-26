import unittest
import json
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        # Восстанавливаем исходные данные перед каждым тестом
        app.items = {
            1: {"name": "Item 1", "value": 10},
            2: {"name": "Item 2", "value": 20}
        }

    # GET /api/items
    def test_get_all_items_success(self):
        response = self.app.get('/api/items')
        self.assertEqual(response.status_code, 200)

    def test_get_all_items_not_empty(self):
        response = self.app.get('/api/items')
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)

    # GET /api/status
    def test_get_status_success(self):
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)

    def test_get_status_correct_response(self):
        response = self.app.get('/api/status')
        data = json.loads(response.data)
        self.assertEqual(data["status"], "running")

    # GET /api/item/<id>
    def test_get_item_success(self):
        response = self.app.get('/api/item/1')
        self.assertEqual(response.status_code, 200)

    def test_get_item_not_found(self):
        response = self.app.get('/api/item/999')
        self.assertEqual(response.status_code, 404)

    # POST /api/item
    def test_create_item_success(self):
        payload = json.dumps({"name": "NewItem", "value": 30})
        response = self.app.post('/api/item', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_item_invalid_input(self):
        payload = json.dumps({"name": "NewItem"})
        response = self.app.post('/api/item', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # DELETE /api/item/<id>
    def test_delete_item_success(self):
        response = self.app.delete('/api/item/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_item_not_found(self):
        response = self.app.delete('/api/item/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()