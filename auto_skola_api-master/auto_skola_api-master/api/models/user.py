import uuid
from typing import Optional

from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth import models as auth_models
from django.db.models import Q

from api.utils.error_handler import WrapperException


class UserManager(auth_models.BaseUserManager):

    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)

    def create_user(self, **fields):
        now = timezone.now()
        create_fields = {
            "is_staff": False,
            "is_superuser": False,
            "is_active": False,
            "verification_token": uuid.uuid4().hex
        }

        email = fields.pop("email", None)
        password = fields.pop("password", None)
        email = UserManager.normalize_email(email)
        email = email.lower()
        if len(email) == 0:
            email = None

        create_fields["email"] = email
        for elem in fields:
            create_fields[elem] = fields[elem]

        user = self.model(**create_fields)
        if password:
            user.set_password(password)

        user.save()
        return user
    ###########################################################################
    ###########################################################################

    def create_superuser(self, **extra_fields):
        superuser = self.create_user(**extra_fields)
        superuser.is_staff = True
        superuser.is_active = False
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser

    ###########################################################################
    def activate_user(self, verification_token):
        user = PlatformUser.objects.filter(verification_token=verification_token).first()
        if not user:
            raise ValueError("User already verified")

        user.last_login = timezone.now()
        user.verification_token = None
        user.is_active = True
        user.save()
        return user

    def cancel_activation_user(self, verification_token):
        user = PlatformUser.objects.filter(verification_token=verification_token).first()
        if not user:
            raise ValueError("User already verified")

        user.delete()
        return None

    ###########################################################################
    def is_already_activated(self, email):
        return self.is_user_name_taken(email)

    def is_user_name_taken(self, username_or_email):
        return self.filter(Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)).exists()

    def get_email_from_username(self, username_or_email):
        username_or_email_filter = self.filter(Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email))
        if username_or_email_filter.exists():
            return username_or_email_filter.first().email
        return username_or_email

    def get(self, *args, **kwargs):
        # Django auth backend handles User.DoesNotExist exception
        class DynamicWrappedDoesNotExist(WrapperException, PlatformUser.DoesNotExist):
            pass

        try:
            return super().get(*args, **kwargs)
        except ObjectDoesNotExist:
            raise DynamicWrappedDoesNotExist("userDoesNotExists", "User does not exists")


class PlatformUser(auth_models.User):
    is_login_blocked = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=32, null=True, blank=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return f"([{self.id}] {self.username} {self.email} | {self.first_name} {self.last_name})"

    class Meta:
        app_label = 'api'