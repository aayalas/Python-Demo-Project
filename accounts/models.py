from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django.core.validators import RegexValidator

from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import pre_delete
# import cloudinary


class CustomUser(AbstractBaseUser, PermissionsMixin):
    DISABILITY_CHOICES = [
        (False, 'Not disabled'),
        (True, 'Disabled'),
    ]
    DISABILITY_TYPE = [
        ('blindness', 'Blindness'),
        ('deafness', 'Deafness'),
        ('physical', 'Physical'),
        ('mental', 'Mental'),
        ('visceral', 'Visceral'),
        ('other', 'Other'),
    ]    
    email = models.EmailField(verbose_name=_("Email"), blank=False, unique=True)    
    # new fields
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    signup_confirmation = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)
    display_name = models.CharField(verbose_name=_("Display name"), max_length=50, blank=True, help_text=_("Display name"))
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True, help_text=_("Date of birth"))
    address1 = models.CharField(verbose_name=_("Address line 1"), max_length=1024, blank=True, null=True)
    address2 = models.CharField(verbose_name=_("Address line 2"), max_length=1024, blank=True, null=True)
    zip_code = models.CharField(verbose_name=_("Postal code"), max_length=12, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=1024, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Enter a valid international mobile number"))
    mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17, blank=True, null=True)
    additional_information = models.TextField(verbose_name=_("Additional information"), max_length=4096, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_images/', default='//www.gravatar.com/avatar')
    cover_pic = models.ImageField(upload_to='cover_images/',default='defaults/cover.jpeg')
    is_disable = models.BooleanField(default=False, choices=DISABILITY_CHOICES)
    disability_type = models.CharField(max_length=100, blank=True, null=True, choices=DISABILITY_TYPE,)
                                        #choices=[('blindness', 'Blindness'), ('deafness', 'Deafness'), ('mobility', 'Mobility')])
    # End new fields
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_disabled(self):
        return self.is_disable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_disable:
            self.disability_type
            
            #_meta.get_field('disability_type').choices = [('blindness', 'Blindness'), ('deafness', 'Deafness'), ('mobility', 'Mobility')]
        else:
            None
            
            #_meta.get_field('disability_type').choices = []


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# """
# Here, there are two main fiels.
# user_id indicate user following and following_user_id indicate user followers.
# """


# class CustomUserFollowing(models.Model):
#     user_id = models.ForeignKey(CustomUser, related_name="following", on_delete=models.CASCADE)
#     following_user_id = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True, db_index=True)

#     class Meta:
#         ordering = ["-created"]
#         unique_together = [['user_id', 'following_user_id']]


#     def no_of_followers(self):
#         result = CustomUserFollowing.objects.filter(following_user_id=self.following_user_id)
#         return len(result)


# class WaitingList(models.Model):
#     user_id = models.ForeignKey(CustomUser, related_name="wait_following", on_delete=models.CASCADE)
#     following_user_id = models.ForeignKey(CustomUser, related_name="wait_followers", on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True, db_index=True)

#     class Meta:
#         ordering = ["-created"]
#         unique_together = [['user_id', 'following_user_id']]

#     def no_of_wait_followers(self):
#         result = WaitingList.objects.filter(following_user_id=self.following_user_id)
#         return len(result)