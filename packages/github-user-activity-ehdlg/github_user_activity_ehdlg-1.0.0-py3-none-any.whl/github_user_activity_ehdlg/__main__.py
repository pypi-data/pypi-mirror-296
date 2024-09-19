from sys import argv

from requests import get

from github_user_activity_ehdlg.utils import get_user_action

username = None

try:
    username = argv[1]
except IndexError:
    print("An username is required!")
    exit()

LIMIT = argv[2] if len(argv) > 2 else 30
URL = f"https://api.github.com/users/{username}/events?per_page={LIMIT}"

request = get(URL)

if request.status_code == 404:
    print(f"The user {username} does not exist!")

    exit()
elif request.status_code != 200:
    print("There was an error connecting to the GitHub API")

    exit()

data = request.json()

print("Output:\n")

for event in data:
    action = get_user_action(event)

    print(action, end="\n")

exit()
