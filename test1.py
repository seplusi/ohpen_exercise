import unittest
import requests
import json
import calendar
import time

import xmlrunner as xmlrunner
from ddt import ddt, data


class TestUnnaxContactForm(unittest.TestCase):
    """A sample test class to show how page object works"""

    token = "5b0ca5ff96e15fa53b30a3e7690acf642fb1dce0"
    headers = {'Content-Type': 'application/json', "Accept": "application/json", "Authorization": "token %s" %token}
    url = "https://api.github.com/"

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_get_all_repos_from_user(self):
        url = "%susers/seplusi/repos" %self.url
        response = requests.get(url=url, headers=self.headers)
        assert response.status_code == 200
        assert len(json.loads(response.text)) == 16

    def test_get_repo_properties(self):
        url = "%srepos/seplusi/ohpen_exercise" % self.url
        response = requests.get(url=url, headers=self.headers)
        assert response.status_code == 200
        assert json.loads(response.text)['name'] == "ohpen_exercise"
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise"

    def test_update_repository11(self):
        url = "%srepos/seplusi/ohpen_exercise" % self.url
        ts = calendar.timegm(time.gmtime())
        data = {'description': 'test_%s' %ts}
        response = requests.patch(url=url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(response.text)['name'] == "ohpen_exercise"
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise"
        assert json.loads(response.text)['description'] == "test_%s" %ts

        for _ in range(10):
            response = requests.get(url=url, headers=self.headers)
            assert response.status_code == 200
            if json.loads(response.text)['description'] == "test_%s" % ts:
                break
            print("Going fo another loop")
            time.sleep(0.5)

        assert json.loads(response.text)['name'] == "ohpen_exercise"
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise"
        assert json.loads(response.text)['description'] == "test_%s" % ts


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()

