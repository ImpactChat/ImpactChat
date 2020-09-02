from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# pylint: disable=no-member

class User(AbstractUser):
    avatar = models.CharField(max_length=1,
                              default="U")
    locale = models.CharField(max_length=2,
                              default="en",
                              choices=settings.LANGUAGES)

    user_role = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    role_data = GenericForeignKey('user_role', 'object_id')


    def getJSON(self):
        return {"username": self.username, "avatar": "U"}


class GetRelatedUserMixin(object):
    @property
    def user(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        try:
            user = User.objects.get(user_role__pk=ctype.id, object_id=self.id)
        except User.DoesNotExist:
            return None 
        return user

class Student(GetRelatedUserMixin, models.Model):
    """
    Represents a student in the school
    """

    def __str__(self):
        print(self.user)
        return f"student-{self.user.username}-{self.pk}"


class Teacher(GetRelatedUserMixin, models.Model):
    """
    Represents a teacher in the school
    """

    def __str__(self):
        return f"teacher-{self.user.username}-{self.pk}"



class Staff(GetRelatedUserMixin, models.Model):
    """
    Represents a staff in the school
    """

    def __str__(self):
        return f"staff-{self.user.username}-{self.pk}"



class Parent(GetRelatedUserMixin, models.Model):
    """
    Represents a parent in the school
    """
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"parent-{self.user.username}-{self.pk}"



class Class(GetRelatedUserMixin, models.Model):
    """
    Represents a class in the school  
    Each class can have multiple students and teachers
    """
    class Meta:
        verbose_name_plural = "Classes"

    name = models.CharField(max_length=32, help_text="Name of the class (ex: French, Math ...)")
    students = models.ManyToManyField(Student)
    teachers = models.ManyToManyField(Teacher)


class Classroom(models.Model):
    """
    Represents a physical classroom in the school
    """
    room_name = models.CharField(max_length=128, 
                                 verbose_name="Room name",
                                 help_text="The name of the room, this is commonly the room number (ex: 216) or name (ex: Entrance)")
