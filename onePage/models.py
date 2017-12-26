from django.db import models


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')


class Script:

    def __init__(self, ujnum=''):

        self.uj = str(ujnum)
        self.text = ''

    def get_string(self):

        try:
            with open(f'/home/lucas/Desktop/uj{self.uj}.py', 'r') as f:
                self.text = f.read()
        except FileNotFoundError:
            self.text = "File not found."