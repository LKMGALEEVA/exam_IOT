import unittest
import json
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        # Восстанавливаем исходные данные перед каждым тестом
        app.items = {
            1: {"name": "Course 1", "teacher": "Ivan", "longitude": 64, "status": "active", "max_numb_students": 20},
            2: {"name": "Course 2", "teacher": "Kolya", "longitude": 100, "status": "active", "max_numb_students": 25},
            3: {"name": "Course 3", "teacher": "Masha", "longitude": 333, "status": "inactive", "max_numb_students": 100}
        }

    # GET /courses
    def test_get_all_items_success(self):
        response = self.app.get('/courses')
        self.assertEqual(response.status_code, 200)

    def test_get_all_items_not_empty(self):
        response = self.app.get('/courses')
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)

    # GET /courses/active
    def test_get_active_items(self):
        response = self.app.get('/courses/active')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for item in data.values():
            self.assertEqual(item["status"], "active")

    # GET /courses/<id>
    def test_get_item_success(self):
        response = self.app.get('/courses/1')
        self.assertEqual(response.status_code, 200)

    def test_get_item_not_found(self):
        response = self.app.get('/courses/999')
        self.assertEqual(response.status_code, 404)

    # POST /courses
    def test_create_item_success(self):
        payload = json.dumps({"name": "Course NEW", "teacher": "Slava", "longitude": 100, "status": "active", "max_numb_students": 99})
        response = self.app.post('/courses', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_item_invalid_input(self):
        payload = json.dumps({"name": "NewItem"})
        response = self.app.post('/courses', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # DELETE /courses/<id>
    def test_delete_item_success(self):
        response = self.app.delete('/courses/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_item_not_found(self):
        response = self.app.delete('/courses/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()