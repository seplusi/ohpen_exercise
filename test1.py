import unittest
import requests
import json
import calendar
import time
from ddt import ddt, data


@ddt
class TestGitHubApi(unittest.TestCase):
    """A sample test class to show how page object works"""

    headers = {'Content-Type': 'application/json', "Accept": "application/json"}
    url = "https://api.github.com/"

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_get_all_repos_from_user(self):
        url = "%susers/seplusi/repos" %self.url
        response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 200
        assert len(json.loads(response.text)) == 16

    def test_get_repo_properties(self):
        url = "%srepos/seplusi/ohpen_exercise" % self.url
        response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 201, 'Expected STATUS_CODE=200. Got STATUS_CODE:%d' %response.status_code
        assert json.loads(response.text)['name'] == "ohpen_exercise", 'Expected repo name = ohpen_exercise. Got: %s' \
                                                                      %json.loads(response.text)['name']
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise", 'Expected repo full name = seplusi/ohpen_exercise. Got: %s' %json.loads(response.text)['full_name']

    @data(1, 2)
    def test_update_repository11(self, value):
        url = "%srepos/seplusi/ohpen_exercise" % self.url
        ts = calendar.timegm(time.gmtime())
        data = {'description': 'test_%s' %ts}
        response = requests.patch(url=url, headers=self.headers, data=json.dumps(data), auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 200
        assert json.loads(response.text)['name'] == "ohpen_exercise"
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise"
        assert json.loads(response.text)['description'] == "test_%s" %ts

        for _ in range(10):
            response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
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

