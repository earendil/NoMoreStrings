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

    def __init__(self, uj_number):

        self.uj_path = self.get_path(uj_number)
        self.update_folder()
        self.text = self.get_source()
        self.string_list = self.get_strings()

    def get_path(self, uj_number):

        response = requests.post('https://tools.scivisumltd.co.uk/couchdb_filter/run_query',
                                 json={"UJs": [f"{uj_number}"], "Step code": "", "Injector": "", "Injector_main": "",
                                       "Injector_backup": "", "Portal": "", "Customer": "", "Browser": "",
                                       "monPeriodOK": "", "monPeriodError": "", "running_yes": True,
                                       "running_no": False, "obsolete_yes": False, "obsolete_no": False,
                                       "True": False, "engine_version_1": False, "engine_version_2": False})

        try:
            uj_path = re.findall(r"(scivisum\.client\.[^<]+)\.[^.<]+", str(response.content))[0]
            uj_path = os.path.join(os.path.expanduser("~/cvs/scivisumv2/python"), uj_path.replace('.', '/') + ".py")
        except IndexError:
            raise Exception(f"User journey not found ({uj_number})")

        return uj_path

    def update_folder(self):

        uj_dir = os.path.dirname(self.uj_path)
        if not uj_dir:
            print("No path specified")
            return

        print(f"Updating path: {uj_dir}")
        update = subprocess.call(['cvs', 'up', '-C', '-d'], cwd=uj_dir)

        print("Successfully updated repository" if not update else "Failed to update repository")

    # TO-DO: Implement show diff instead of showing the whole script.
    def show_diff(self):

        uj_dir, uj_file = os.path.split(self.uj_path)
        try:
            output = subprocess.check_output(['cvs', 'diff', uj_file], cwd=uj_dir)[:-1]
        except CalledProcessError as e:
            output = e.output

        return output

    def commit(self, text='', case=''):

        uj_dir, uj_file = os.path.split(self.uj_path)

        message = f"[#{case}] {text}"

        try:
            output = subprocess.check_output(['cvs', 'commit', '-m', message, '-f', uj_file], cwd=uj_dir)[:-1]
        except CalledProcessError as e:
            output = e.output

        return output

    def get_source(self):

        try:
            with open(self.uj_path, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            raise Exception("File not found on repository.") from e

    def set_source(self):

        try:
            with open(self.uj_path, 'w') as f:
                f.write(self.text)
        except FileNotFoundError:
            self.text = "File not found."

    def get_strings(self):

        return re.findall(r"\bStringTest\((.*)\)", self.text)

    def replace_text(self, old_string, new_string):

        self.text = self.text.replace(old_string, repr(new_string))
        self.set_source()
