#username : movier
#pass : pass123456
# Create your models here.


from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    userid = models.IntegerField(db_column='id', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.NullBooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.NullBooleanField()
    is_active = models.NullBooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'



class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Movies(models.Model):
    movieid = models.TextField(db_column='movieId', primary_key=True)  # Field name made lowercase. This field type is a guess.
    title = models.TextField(blank=True, null=True)  # This field type is a guess.
    genres = models.TextField(blank=True, null=True)  # This field type is a guess.
    overview = models.CharField(max_length=2000, blank=True, null=True)
    poster = models.CharField(max_length=300, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)  # This field type is a guess.
    trailer = models.CharField(max_length=100, blank=True, null=True)
    rate = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'movies'


class Ratings(models.Model):
    userid = models.TextField(db_column='userId', primary_key=True)  # Field name made lowercase. This field type is a guess.
    movieid = models.TextField(db_column='movieId', primary_key=True)  # Field name made lowercase. This field type is a guess.
    rating = models.TextField(blank=True, null=True)  # This field type is a guess.
    timestamp = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ratings'
        unique_together = (('userid', 'movieid'),)


class Users(models.Model):
    userid = models.TextField(db_column='userId', primary_key=True)  # Field name made lowercase. This field type is a guess.
    username = models.TextField(blank=True, null=True)  # This field type is a guess.
    password = models.TextField(blank=True, null=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    favgenres = models.TextField(db_column='favGenres', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'users'



class Followuser(models.Model):
    userid = models.IntegerField(db_column='userid', primary_key=True)
    userfollowid = models.IntegerField(db_column='userfollowid', primary_key=True)
    isfollow = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'followuser'
        unique_together = (('userid', 'userfollowid'),)








# after making any change you have to "makemigrations" and then "migrate"
# >>>> python manage.py makemigrations movies
# >>>> python manage.py migrate