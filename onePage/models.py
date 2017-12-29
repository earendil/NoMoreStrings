import os
import subprocess
from subprocess import CalledProcessError
import requests
import re
from django.db import models


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')


class Script:

    def __init__(self):

        self.uj = ''
        self.text = ''
        self.path = ''
        self.string_list = []
        self.status = 'Ready'
        self.flow = True

    def update(self, uj_number):

        self.uj = str(uj_number)
        self.path = self.get_path()
        self.update_folder()
        self.text = self.get_source()
        self.string_list = self.get_strings()

    def get_path(self):

        response = requests.post('https://tools.scivisumltd.co.uk/couchdb_filter/run_query',
                                 json={"UJs": [f"{self.uj}"], "Step code": "", "Injector": "", "Injector_main": "",
                                       "Injector_backup": "", "Portal": "", "Customer": "", "Browser": "",
                                       "monPeriodOK": "", "monPeriodError": "", "running_yes": True,
                                       "running_no": False, "obsolete_yes": False, "obsolete_no": False,
                                       "True": False, "engine_version_1": False, "engine_version_2": False})

        try:
            self.uj = re.findall(r"client\.[^.]+.([^.]+)", str(response.content))[0]
        except IndexError:
            pass

        path = subprocess.check_output(f'find ~/cvs -name {self.uj}.py', shell=True)[:-1]

        if not path:
            self.status = 'User Journey not found.'
            self.flow = False

        string_path = path.decode('ascii')
        client_folder = os.path.dirname(string_path)

        return client_folder

    def update_folder(self):
        if not self.path:
            print("No path specified")
            return

        print(f"Updating path: {self.path}")
        update = subprocess.call(['cvs', 'up', '-C', '-d'], cwd=self.path)

        print("Successfully updated repository" if not update else "Failed to update repository")

    # TO-DO: Implement show diff instead of showing the whole script.
    def show_diff(self):
        try:
            output = subprocess.check_output(['cvs', 'diff', self.uj + '.py'], cwd=self.path)[:-1]
        except CalledProcessError as e:
            output = e.output

        return output

    def commit(self, text='', case=''):

        message = f"[#{case}] {text}"

        try:
            output = subprocess.check_output(['cvs', 'commit', '-m', message, '-f', self.uj + '.py'], cwd=self.path)[:-1]
        except CalledProcessError as e:
            output = e.output

        return output

    def get_source(self):

        try:
            with open(self.path + "/" + self.uj + ".py", 'r') as f:
                return f.read()
        except FileNotFoundError:
            if self.flow:
                self.status = "File not found on repository."
                self.flow = False
            return ''

    def set_source(self):
        try:
            with open(self.path + "/" + self.uj + ".py", 'w') as f:
                f.truncate()
                f.write(self.text)
        except FileNotFoundError:
            self.text = "File not found."

    def get_strings(self):

        string_tests_list = re.findall(r"\sStringTest\((.*)\)", self.text)

        if not string_tests_list:
            if self.flow:
                self.status = 'No strings found.'
                self.flow = False
        return string_tests_list

    def replace_text(self, old_string, new_string):

        self.text = self.text.replace(old_string, f'"{new_string}"')
        self.set_source()


