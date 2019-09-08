from django.db import models


class News(models.Model):
    title = models.CharField(max_length = 200)
    source = models.CharField(max_length = 20)
    date = models.CharField(max_length = 25)
    content = models.CharField(max_length = 8000)
    def __str__(self):
        return self.title

class Team(models.Model):
    name = models.CharField(max_length = 20)
    city = models.CharField(max_length = 15, default = "")
    year = models.CharField(max_length = 10)
    def __str__(self):
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name_cn = models.CharField(max_length = 30)
    name_en = models.CharField(max_length = 30)
    def __str__(self):
        return self.name_cn