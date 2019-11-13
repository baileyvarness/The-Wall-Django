from django.db import models

class UserManager(models.Manager):
    def validator(self, post_data):
        print('post_data: ', post_data)
        errors = {}

        if len(post_data['first_name']) < 2:
            errors["first_name"] = "your first name is too short"
        if len(post_data['last_name']) < 2:
            errors["last_name"] = "your last name is too short"
        if len(post_data['email']) < 5:
            errors["email"] = "your email is too short"
        if len(post_data['password']) < 8:
            errors["password"] = "your password is too short"
        if (post_data['password'] != post_data['password_confirm']):
            errors['password_confirm'] = 'your password doesn\'t match'

        return errors

class User(models.Model):
    email = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    user = models.ForeignKey(User, related_name="message")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comment")
    message = models.ForeignKey(Message, related_name="comment")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()