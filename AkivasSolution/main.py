import argparse
from repo_info import RepoInfo


def main():
    parser = argparse.ArgumentParser(description="Get GitHub repository information and last releases")
    parser.add_argument('-token', required=True, help="GitHub Personal Access Token")
    args = parser.parse_args()

    repo_info = RepoInfo(args.token)
    repo_info.get_repo_info()
    repo_info.print_repo_data()


if __name__ == '__main__':
    main()
