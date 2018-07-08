from django.db import models
from django.utils import timezone

class blog(models.Model):
    content = models.CharField('内容', max_length=20)
    created_at = models.DateTimeField('作成日', default=timezone.now)
