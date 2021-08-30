import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db

class DriverTimesheetTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'driver_timesheet_test'
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', self.database_name) 
        setup_db(self.app, self.database_path)

        self.headers = {
                "Content-Type": "application/json", 
                "Accept": "application/json",
                }

        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_empty_users(self):
        response = self.client().get("/users")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["total_users"], 0)

if __name__ == "__main__":
    unittest.main()
