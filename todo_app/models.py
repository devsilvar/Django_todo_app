from django.db import models
from django.contrib.auth.models import User

import uuid
# Create your models here.

class todo_table(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE , default='null' )
    todo_name = models.CharField(max_length=500)
    todo_id = models.UUIDField(default=uuid.uuid4 , editable=True)
    todo_status = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True , editable=True )

    def __str__(self) -> str:
        return self.todo_name 


class customersResetsId(models.Model):
    # the user requesting to reset his pasword
    # the time it was created
    # resetId generated
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4 , unique=True , editable=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)


    def __str__(self):
        return f"{self.user} resetId generated at  {self.created}"







