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
        self.database_name = 'driver_timesheet'
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

   #  def test_empty_users(self):
   #      response = self.client().get("/users")
   #      data = json.loads(response.data.decode())
   #      self.assertEqual(response.status_code, 200)
   #      self.assertEqual(data["total_users"], 0)

    """
    test to implements                  | expected results
    1. user add timesheet               | 200
                                          approval with timesheetid newly created is empty
    
    2. nobody add record in timesheet   | 422
    
    3. user approve timesheet           | 200
                                          count timesheetid in approval == 1

    4. user re(approve) timesheet       | 422

    5. view timesheets                  | 200
                                          count all timesheets record > 0

    6. view timesheets page 100         | 404
                                          count all timesheets records < 8 * 100
     

    """
    
    def test_view_timesheets(self):
        response = self.client().get("/timesheets")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertGreater(data['total_records'], 0)
    
    def test_404_request_beyond_valid_page(self):
        response = self.client().get('/timesheets?page=100')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # def test_add_record_intimesheets(self):
    #     response = self.client().post("/timesheets", json={'userid': 23 })

    def test_add_approvals_already_approved(self):
        response = self.client().post("/approvals/23", json={"timesheetid":2})
        data = json.loads(response.data.decode())
        self.assertEqual(data['status_code'], 422)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
