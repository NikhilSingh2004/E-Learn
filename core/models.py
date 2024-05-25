from django.db import models
from courses.models import Topic
from django.utils.timezone import now
from django.contrib.auth.models import User

'''
    Model to Save Contact Info in the Contact Us Page!

    Contact Us
        - first Name : Ex Nikhil (Not Optional)
        - last Name : Ex Singh (Not Optional)
        - username : If the user is loged in then Foreign Key that will be the user model (auth_user). Else the field in optional
        - email : If the user is loged in then the user's email. If the user is guest then the Guest have to enter there mail! (Not Optional)
        - body : Mail Body (Not Optional)
        - footer : Footer note for the email if any! (Optional)
'''

class ContactUs(models.Model):
    
    first_name = models.CharField(max_length=128)

    last_name = models.CharField(max_length=128)

    username = models.CharField(max_length=128, null=True, blank=True)

    email = models.CharField(max_length=256)

    subject = models.CharField(max_length=1024)
    
    body = models.TextField()

    footer = models.TextField(max_length=128, null=True, blank=True)

'''
    If we want to add more fields to the default User Model (auth_user), then it can used my Monkey Patching.

    However, it's important to note that directly modifying Django's built-in models is generally not recommended as it can have unforeseen consequences and compatibility issues, especially during upgrades.

    In the models.py or any other file that gets loaded when Django starts
    from django.contrib.auth.models import User

    # Add custom fields directly to the User model
    User.add_to_class('custom_field1', models.CharField(max_length=100, blank=True))
    User.add_to_class('custom_field2', models.IntegerField(default=0))
    
'''

'''
    Need to Make Model Comment!s

    ID : Default Serial No. for Identification 
    User : Foreign Key User Model From auth_user
    Topic : The Specific Topic that the comment is associated with 
    Parent : If the Comment is an reply then it will contain the Comment Object under which the replay is given.
    Time : The Time of comment 
    Content : The Content Of the Comment!
'''

class Comment(models.Model):
    content = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    timestamp = models.DateTimeField(default=now)
