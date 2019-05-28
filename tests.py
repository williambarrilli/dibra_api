import unittest
import json
from main import app
from db import db
from models.artist import ArtistModel


class AlunoTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data_test2.db'
        self.app_context = app.app_context()
        self.app_context.push()
        db.init_app(app)
        db.create_all()
        self.app = app.test_client()

        self.artist1 = ArtistModel(name="Luciano")
        self.artist2 = ArtistModel(name="Fabiana")
        db.session.add(self.artist1)
        db.session.add(self.artist2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_artists(self):
        pass

    def test_get_artist_by_id(self):
        pass

    def test_get_artist(self):
        response = self.app.get('/artist/{}'.format(self.artist1.name))
        self.assertEqual(response.status_code, 200)
        artist = response.get_json()
        self.assertEqual(artist.get('name'), self.artist1.name)
        self.assertEqual(artist.get('id'), self.artist1.id)

        response = self.app.get('/artist/ACDC')
        artist = response.get_json()
        self.assertEqual(artist.get('message'), 'artist not found')

    def test_create_artist(self):
        artist = {"name": "LucianoCamargo"}
        response = self.app.post(
            '/artist',
            data=json.dumps(artist),
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 201)
        artist = response.get_json()
        self.assertEqual(artist.get('name'), 'LucianoCamargo')

    def test_update_artist_name(self):
        pass

    def test_delete_artist(self):
        pass

if __name__ == "__main__":
    unittest.main()
