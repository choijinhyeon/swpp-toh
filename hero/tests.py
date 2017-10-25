from django.test import TestCase, Client
import json
from .models import Hero
from django.forms.models import model_to_dict
# Create your tests here.
class HeroTestCase(TestCase):
    def setUp(self):
        Hero.objects.create(name='Superman')
        Hero.objects.create(name='Batman')
        Hero.objects.create(name='Joker')

        self.client = Client()

    def test_hero_list(self):
        response = self.client.get('/api/hero')
        data = json.loads(response.content.decode())
        self.assertEqual(len(data), 3)


    def test_hero_create(self):
        response = self.client.post('/api/hero', json.dumps({'name':'kk'}), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_hero_false(self):
        response = self.client.put('/api/hero', json.dumps({'name':'kk'}), content_type = 'application/json')
        self.assertEqual(response.status_code, 405)


    def test_hero_str(self):
        batman = Hero.objects.get(name='Batman')
        self.assertEqual(str(batman),'Batman')

    def test_hero_detail_get(self):
        response = self.client.get('/api/hero/3')

        data = json.loads(response.content.decode())
        self.assertEqual(data['name'], 'Joker')
        self.assertEqual(response.status_code, 200)

    def test_hero_detail_put(self):
        response = self.client.put('/api/hero/1', json.dumps({'name':'kk'}), content_type = 'application/json')
        data = json.loads(self.client.get('/api/hero/1').content.decode())
        self.assertEqual(data['name'],'kk')
        self.assertEqual(response.status_code, 204)

    def test_hero_detail_delete(self):
        response = self.client.delete('/api/hero/1')
        self.assertEqual(response.status_code, 204)

    def test_hero_detail_get_not_found(self):
        response = self.client.get('/api/hero/4')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_put_not_found(self):
        response = self.client.put('/api/hero/4', json.dumps({'name':'kk'}), content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_delete_not_found(self):
        response = self.client.delete('/api/hero/4')
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_false(self):
        response = self.client.post('/api/hero/1', json.dumps({'name':'kk'}), content_type = 'application/json')
        self.assertEqual(response.status_code, 405)
