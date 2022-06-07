import binascii
import os

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from datetime import date


# Create your models here.

class UserProfile(AbstractUser):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    identity_num = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    province_info = models.CharField(max_length=50)
    district_info = models.CharField(max_length=50)
    ward_info = models.CharField(max_length=50)

    token = models.CharField(max_length=200, db_column='account_token', blank=True, null=True, verbose_name='Token')
    token_date = models.DateField(db_column='account_token_date', blank=True, null=True, verbose_name=('Token Date'))
    # Reset
    account_token_reset_pass = models.CharField(max_length=200, db_column='account_token_reset_pass',
                                                blank=True, null=True)
    account_token_reset_pass_time = models.DateTimeField(db_column='account_token_reset_pass_time',
                                                         blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at', blank=True, null=True,
                                      verbose_name=('Created at'))
    updated_at = models.DateTimeField(auto_now=True, db_column='modified_at', blank=True, null=True,
                                      verbose_name=('Updated at'))
    created_by = models.CharField(max_length=100, db_column='created_by', blank=True, null=True, default='',
                                  verbose_name=('Created by'))
    updated_by = models.CharField(max_length=100, db_column='modified_by', blank=True, null=True, default='',
                                  verbose_name=('Updated by'))

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
            self.token_date = date.today()
        return super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def get_key(self):
        import base64

        key = '{}:{}'.format(self.id, self.token)
        key = key.encode()

        try:
            return base64.b64encode(key).decode('utf-8')
        except:
            return None

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def reset_key(self, _date):
        if self.token_date != _date:
            self.token_date = _date
            self.token = self.generate_key()
            self.save()

        return self.get_key

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    # def verify_permission(self, codename) -> None:
    #     if self.is_superuser == False:
    #         permission = UserRolePermission.objects.filter(user_id=self.id, permission_codename=codename).values('permission_codename')
    #         if not permission:
    #             raise CustomAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Authorization required")


class LogSearch(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=20)
    real_estate_type = models.CharField(max_length=200, null=True)
    province_search = models.CharField(max_length=200, null=True)
    district_search = models.CharField(max_length=200, null=True)
    price_search = models.FloatField(default=0, null=True)
    squad_search = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at', blank=True, null=True,
                                      verbose_name=('Created at'))
    created_by = models.CharField(max_length=100, db_column='created_by', blank=True, null=True, default='',
                                  verbose_name=('Created by'))


class LogPosts(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=20)
    object_id_post = models.CharField(max_length=50)
    province_search = models.CharField(max_length=200, null=True)
    district_search = models.CharField(max_length=200, null=True)
    price_search = models.FloatField(default=0, null=True)
    squad_search = models.CharField(max_length=100, null=True)
