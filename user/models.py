from django.db import models

class User(models.Model):
    email         = models.EmailField(max_length = 200)
    password      = models.CharField(max_length = 200, null = True)
    first_name    = models.CharField(max_length = 50)
    last_name     = models.CharField(max_length = 50)
    birth_date    = models.DateField(null = True)
    is_host       = models.BooleanField()
    platform      = models.ForeignKey('LoginPlatform', on_delete = models.CASCADE, null = True)
    created_at    = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user          = models.ForeignKey('User', on_delete = models.CASCADE)
    introduction  = models.TextField(null = True)
    location      = models.CharField(max_length = 50, null = True)
    profile_image = models.URLField(null = True)
    gender        = models.ForeignKey('Gender', on_delete = models.CASCADE, null = True)
    phone_number  = models.CharField(max_length = 50, null = True)
    language      = models.ManyToManyField('Language', through = 'UserLanguage')

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return self.user.email

class Host(models.Model):
    user          = models.ForeignKey('User', on_delete = models.CASCADE)
    is_super_host = models.BooleanField()

    class Meta:
        db_table = "hosts"

class Language(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "languages"

    def __str__(self):
        return self.name

class UserLanguage(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete = models.CASCADE)
    language     = models.ForeignKey('Language', on_delete = models.CASCADE)

    class Meta:
        db_table = "user_languages"

class Gender(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "genders"

    def __str__(self):
        return self.name

class LoginPlatform(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "login_platforms"

    def __str__(self):
        return self.name