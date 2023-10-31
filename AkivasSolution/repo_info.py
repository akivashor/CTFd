import requests


class RepoInfo:
    def __init__(self, token: str):
        """
        Initialize a RepoInfo instance.

        :param token: GitHub Personal Access Token.
        """
        self.pull_request_count = None
        self.contributors_count = None
        self.sorted_contributors = None
        self.pull_requests_data = None
        self.last_releases_names = []
        self.pull_requests_count = None
        self.repo_stars = None
        self.forks_count = None
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}'
        }
        self.base_url = 'https://api.github.com/repos/CTFd/CTFd'
        self.response_data = None

    def get_repo_info(self):
        """
        Retrieve and analyze repository information.
        """
        self.get_repo_response()
        if self.response_data:
            self.analyze_repo_data()

    def get_repo_response(self):
        """
        Send a GET request to the GitHub API to fetch repository information.
        """
        try:
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code == 200:
                self.response_data = response.json()
            else:
                print(f"Failed to retrieve repository information. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def analyze_repo_data(self):
        """
        Analyze the retrieved repository data.
        """
        self.get_last_releases()
        self.get_forks_count()
        self.get_repo_stars_info()
        self.get_contributors_and_pull_requests_info()

    def get_sort_contributors_by_pull_requests(self):
        """
        Count and sort contributors based on the number of pull requests.
        """
        contributors = {}  # Dictionary to store contributor information

        for pr in self.pull_requests_data:
            contributor_login = pr['user']['login']

            if contributor_login in contributors:
                contributors[contributor_login] += 1
            else:
                contributors[contributor_login] = 1

        # Sort contributors by the number of pull requests in descending order
        self.sorted_contributors = sorted(contributors.items(), key=lambda x: x[1], reverse=True)

    def get_contributors_and_pull_requests_info(self):
        """
        Get contributors and pull requests information.
        """
        self.get_pull_requests_info()
        self.pull_request_count = len(self.pull_requests_data)
        self.get_sort_contributors_by_pull_requests()
        self.contributors_count = len(self.sorted_contributors)

    def get_pull_requests_info(self):
        """
        Fetch pull request information.
        """
        self.get_pull_requests_response()
        self.pull_requests_count = len(self.pull_requests_data)

    def get_pull_requests_response(self):
        """
        Send a GET request to retrieve pull requests.
        """
        pulls_url = self.response_data['pulls_url']
        stripped_url = pulls_url.replace('{/number}', '')
        params = {'per_page': 1000}  # Specify a large per_page value to retrieve all pull requests

        try:
            response = requests.get(stripped_url, headers=self.headers, params=params)
            if response.status_code == 200:
                self.pull_requests_data = response.json()
            else:
                print(f"Failed to retrieve pull request information. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_repo_stars_info(self):
        """
        Fetch and store the number of stars (stargazers) for the repository.
        """
        self.repo_stars = self.response_data['stargazers_count']

    def get_forks_count(self):
        """
        Fetch and store the number of forks for the repository.
        """
        self.forks_count = self.response_data['forks_count']

    def get_last_releases(self, amount=3):
        """
        Fetch the last releases of the repository.

        :param amount: Number of releases to retrieve (default is 3).
        """
        releases_url = f"{self.base_url}/releases"
        try:
            response = requests.get(releases_url, headers=self.headers)
            if response.status_code == 200:
                releases_data = response.json()
                last_releases = releases_data[:amount]  # Get the last releases
                for release in last_releases:
                    self.last_releases_names.append(release['name'])
            else:
                print(f"Failed to retrieve releases information. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def print_repo_data(self):
        """
        Print the retrieved repository data.
        """
        print("Latest releases of CTFd:")
        for release_name in self.last_releases_names:
            print(f"- {release_name}")

        print(f"Number of forks: {self.forks_count}")
        print(f"Number of stars: {self.repo_stars}")
        print(f"Number of contributors: {self.contributors_count}")
        print(f"Number of pull requests: {self.pull_request_count}")

        print("Descending order list of contributors per amount of pull requests:")
        for contributor, pull_request_count in self.sorted_contributors:
            print(f"{contributor}: {pull_request_count}")