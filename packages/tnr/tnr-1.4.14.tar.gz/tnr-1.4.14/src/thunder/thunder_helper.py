import os
from os.path import join
import sys
import click
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from thunder.get_latest import get_latest

# URLs for cloud functions
CREATE_SESSION_USER_URL = "https://create-session-user-b7ngwrgpka-uc.a.run.app"
DELETE_SESSION_USER_URL = "https://delete-session-user-b7ngwrgpka-uc.a.run.app"


# Helper to call cloud functions
def call_firebase_function(url, id_token, payload=None):
    try:
        headers = {
            "Authorization": "Bearer " + id_token,
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload, timeout=5)
        return response
    except Exception as _:
        msg = "Failed to create a session on the thunder network. Please report this issue to the developers!"
        click.echo(click.style(msg, fg='white', bg='red'))
        exit(1)


class Task:
    def __init__(self, args: tuple, uid: str):
        self.args = args # args[0].split(" ")
        self.username = uid
        self.password = None
        self.topic = None

    # set environment variable for
    # use firebase credentials to retrieve session password
    def get_password(self, id_token: str) -> bool:
        payload = {}
        response = call_firebase_function(CREATE_SESSION_USER_URL, id_token, payload)
        if response.status_code != 200:
            click.echo("Failed to create user.")
            return False
        response = response.json()
        if not isinstance(response, dict):
            click.echo("Failed to create user.")
            return False

        password = response.get("password")

        if not password:
            click.echo("Invalid response: Password missing.")
            return False

        self.password = password
        return True
    
    def get_ip_address(self):
        return requests.get('https://api.ipify.org').content.decode('utf8')

    def execute_task(self, id_token: str) -> bool:
        device_file = join(join(os.path.expanduser("~"), ".thunder"), 'dev')
        with open(device_file, 'r') as f:
            device = f.read()
        
        binary = get_latest("client", "~/.thunder/libthunder.so")
        if binary == None:
            print("Failed to download binary")
            return False

        os.environ["SESSION_USERNAME"] = self.username
        os.environ["TOKEN"] = id_token
        os.environ["__TNR_RUN"] = "true"
        os.environ["IP_ADDR"] = self.get_ip_address()
        if device.lower() != 'cpu':
            os.environ["LD_PRELOAD"] = f'{binary}'
        
        # This should never return
        try:
            os.execvp(self.args[0], self.args)
        except FileNotFoundError:
            click.echo(click.style(f"The following command could not be found: {' '.join(self.args)}", fg='red', bold=True))
        except Exception as e:
            print(e)
        return False

    def close_session(self, id_token: str) -> bool:
        # to implement, communicate to manager computation is done, triggering exit_user
        click.echo("finishing task")
        return True
