from django.db import models

import django.contrib.auth.models as auth_models


class Micropost(models.Model):
    content = models.TextField(max_length=140)
    user = models.ForeignKey(auth_models.User)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
