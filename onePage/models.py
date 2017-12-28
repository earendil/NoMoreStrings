import subprocess
import requests
import re
from django.db import models


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')


class Script:

    def __init__(self, ujnum=''):

        self.uj = str(ujnum)
        self.text = ''
        self.path = self.get_path()

    def get_path(self):

        response = requests.post('https://tools.scivisumltd.co.uk/couchdb_filter/run_query',
                                 json={"UJs": [f"{self.uj}"], "Step code": "", "Injector": "", "Injector_main": "",
                                       "Injector_backup": "", "Portal": "", "Customer": "", "Browser": "",
                                       "monPeriodOK": "", "monPeriodError": "", "running_yes": True,
                                       "running_no": False, "obsolete_yes": False, "obsolete_no": False,
                                       "True": False, "engine_version_1": False, "engine_version_2": False})

        try:
            true_uj_number = re.findall(r"client\.[^.]+.([^.]+)", str(response.content))[0]
        except IndexError:
            true_uj_number = "000"

        path = subprocess.check_output(f'find ~/cvs -name {true_uj_number}.py', shell=True)[:-1]

        return path

    def update_path(self):

        update = 1

        if self.path != b'':
            string_path = self.path.decode('ascii')
            client_folder = string_path.rsplit('/', 1)[0]
            print(f"Updating path: {client_folder}")
            update = subprocess.call(f'cd {client_folder}; cvs up -C -d', shell=True)
        else:
            print("No path specified")

        print("Successfully updated repository" if not update else "Failed to update repository")

    def get_source(self):

        try:
            with open(self.path, 'r') as f:
                self.text = f.read()
        except FileNotFoundError:
            self.text = "File not found."

    def set_source(self):
        try:
            with open(self.path, 'w') as f:
                f.truncate()
                f.write(self.text)
        except FileNotFoundError:
            self.text = "File not found."

    def get_strings(self):

        string_tests_list = re.findall(r"\sStringTest\((.*)\)", self.text)

        return string_tests_list if string_tests_list else [self.text]
