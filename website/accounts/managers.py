from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, *args, **kwargs):
        now = timezone.now()
    def create_user(self, email, password, *args, **kwargs):
    
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def _create_user(
        self, 
        email, 
        password,
        is_staff,
        is_superuser,
        **kwargs,
    ):
        user = self.model(
            email = self.normalize_email(email),
            is_active = True,
            is_staff = is_staff,
            is_superuser = is_superuser,
            date_joined = timezone.now(),
            **kwargs,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, False, False, **kwargs)
    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, True, **kwargs)
        
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)