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

    @staticmethod
    def get_path(uj=''):

        response = requests.post('https://tools.scivisumltd.co.uk/couchdb_filter/run_query',
                                 json={"UJs": [f"{uj}"], "Step code": "", "Injector": "", "Injector_main": "",
                                       "Injector_backup": "", "Portal": "", "Customer": "", "Browser": "",
                                       "monPeriodOK": "", "monPeriodError": "", "running_yes": True,
                                       "running_no": False, "obsolete_yes": False, "obsolete_no": False,
                                       "True": False, "engine_version_1": False, "engine_version_2": False})

        true_uj_script = re.findall(r"client\.[^.]+.([^.]+)", str(response.content))[0]

        path = subprocess.check_output(f'find ~/cvs -name {true_uj_script}.py', shell=True)[:-1]

        return path

    def get_source(self):

        try:
            with open(self.get_path(self.uj), 'r') as f:
                self.text = f.read()
        except IndexError:
            self.text = "File not found."

    def get_strings(self):

        string_tests_list = re.findall(r"\sStringTest\((.*)\)", self.text)

        return string_tests_list if string_tests_list else [self.text]
