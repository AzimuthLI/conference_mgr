import unittest
import os
import json
from app import create_app, db

class ConferenceTestCase(unittest.TestCase):
    """This class represents the Conference test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.conference = {'name': 'National Celebration'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_conference_creation(self):
        """Test API can create a conference (POST request)"""
        res = self.client().post('/conferences/', data=self.conference)
        self.assertEqual(res.status_code, 201)
        self.assertIn('National', str(res.data))

    def test_api_can_get_all_conferences(self):
        """Test API can get a conference (GET request)."""
        res = self.client().post('/conferences/', data=self.conference)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/conferences/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('National', str(res.data))

    def test_api_can_get_conference_by_id(self):
        """Test API can get a single conference by using it's id."""
        rv = self.client().post('/conferences/', data=self.conference)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/conferences/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('National', str(result.data))

    def test_conference_can_be_edited(self):
        """Test API can edit an existing conference. (PUT request)"""
        rv = self.client().post(
            '/conferences/',
            data={'name': 'National Party Big'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/conferences/1',
            data={
                "name": "New Years Celebration"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/conferences/1')
        self.assertIn('New Years', str(results.data))

    def test_conference_deletion(self):
        """Test API can delete an existing conference. (DELETE request)."""
        rv = self.client().post(
            '/conferences/',
            data={'name': 'National Party Big'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/conferences/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/conferences/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()