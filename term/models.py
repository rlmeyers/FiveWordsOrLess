from django.db import models

class Term(models.model):
    term_content = models.CharField(max_length = 200)

