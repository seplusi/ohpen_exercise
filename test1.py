import unittest
import requests
import json
import time
from ddt import ddt, data


@ddt
class TestGitHubApi(unittest.TestCase):
    """A sample test class to show how page object works"""

    headers = {'Content-Type': 'application/json', "Accept": "application/json"}
    url = "https://api.github.com/"

    @classmethod
    def setUpClass(cls):
        if "Hello-World" in cls._get_all_repos():
            cls._delete_one_repos("Hello-World")

        if "repo_2_be_deleted" not in cls._get_all_repos():
            cls._create_repo("repo_2_be_deleted")

        if "one_repo" not in cls._get_all_repos():
            cls._create_repo("one_repo")

    def setUp(self):
        pass

    def test_get_all_repos_from_user(self):
        url = "%susers/seplusi/repos" %self.url
        response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 200
        assert len(json.loads(response.text)) > 0
        assert "one_repo" in [repo['name'] for repo in  json.loads(response.text)]

    def test_get_repo_properties(self):
        url = "%srepos/seplusi/ohpen_exercise" % self.url
        response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 200, 'Expected STATUS_CODE=200. Got STATUS_CODE:%d' %response.status_code
        assert json.loads(response.text)['name'] == "ohpen_exercise", 'Expected repo name = ohpen_exercise. Got: %s' \
                                                                      %json.loads(response.text)['name']
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise", 'Expected repo full name = seplusi/ohpen_exercise. Got: %s' %json.loads(response.text)['full_name']

    @data(1, 2)
    def test_update_repository11(self, value):
        url = "%srepos/seplusi/ohpen_exercise" % self.url
        data = {'description': 'test_%s' %value}
        response = requests.patch(url=url, headers=self.headers, data=json.dumps(data), auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 200
        assert json.loads(response.text)['name'] == "ohpen_exercise"
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise"
        assert json.loads(response.text)['description'] == "test_%s" %value

        for _ in range(10):
            response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
            assert response.status_code == 200
            if json.loads(response.text)['description'] == "test_%s" % value:
                break
            time.sleep(0.5)
        else:
            assert False, 'Timeout. Update repo\'s description = \'test_%s\' did not happer' %value

        assert json.loads(response.text)['name'] == "ohpen_exercise"
        assert json.loads(response.text)['full_name'] == "seplusi/ohpen_exercise"
        assert json.loads(response.text)['description'] == "test_%s" % value

    def test_create_repo(self):
        new_repo_data = {
            "name": "Hello-World",
            "description": "This is your first repository",
            "homepage": "https://github.com",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }
        url = "%suser/repos" %self.url
        response = requests.post(url=url, headers=self.headers, data=json.dumps(new_repo_data), auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 201

        for _ in range(10):
            if "Hello-World" in self._get_all_repos():
                break
            time.sleep(0.5)
        else:
            assert False, 'Timeout. Hello-world repo was never created. Current list of repos is: %s'\
                          %str(self._get_all_repos())

    def test_delete_repo(self):
        url = '%srepos/seplusi/Hello-World' %self.url
        response = requests.delete(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 204

        for _ in range(10):
            if "Hello-World" not in self._get_all_repos():
                break
            time.sleep(0.5)
        else:
            assert False, 'Timeout. Hello-world repo was not deleted. Current list of repos is: %s'\
                          %str(self._get_all_repos())

    @classmethod
    def _create_repo(self, repo_name):
        new_repo_data = {
            "name": repo_name,
            "description": "This is your first repository",
            "homepage": "https://github.com",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }
        url = "%suser/repos" %self.url
        response = requests.post(url=url, headers=self.headers, data=json.dumps(new_repo_data), auth=('seplusi', 'Luis!23$'))
        assert response.status_code == 201

        for _ in range(10):
            if repo_name in self._get_all_repos():
                break
            time.sleep(0.5)
        else:
            assert False, 'Timeout. %s repo was never created. Current list of repos is: %s'\
                          %(repo_name, str(self._get_all_repos()))

    @classmethod
    def _get_all_repos(self):
        url = "%susers/seplusi/repos" % self.url
        response = requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        return [repo['name'] for repo in  json.loads(response.text)]

    @classmethod
    def _delete_one_repos(self, repo_name, timeout=10):
        url = '%srepos/seplusi/%s' %(self.url, repo_name)
        requests.delete(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
        for _ in range(timeout):
            requests.get(url=url, headers=self.headers, auth=('seplusi', 'Luis!23$'))
            if repo_name not in self._get_all_repos():
                break
            time.sleep(0.5)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()

