from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone
User = settings.AUTH_USER_MODEL


class MyAccountManager(BaseUserManager):
	def create_user(self, username, email, password, phone,**extra_fields):
		if not username:
			raise valueError("User must have username!")
		if not email:
			raise valueError("User must have email!")

		user = self.model(email=self.normalize_email(email),username=username,phone=phone,
							password=password, **extra_fields)
						
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, username, password, phone, **extra_fields):

		user = self.create_user(email=self.normalize_email(email), username=username, password=password,phone=phone, 
							**extra_fields)
		user.is_admin = True				
		user.is_staff = True				
		user.is_superuser = True				
		user.save(using=self._db)
		return user		


class UserProfile(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True, null=True, blank=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=20, default=None, null=True, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

	# All these field are required for custom user model
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	# other
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30, blank=True, null=True)
	dob = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
	gender = models.CharField(max_length=100, blank=True, null=True)
	profile_pic = models.ImageField(blank=True, null=True, upload_to='Profile_Pics')

	objects = MyAccountManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'phone']

	def __str__(self):
		try:
			return str(self.email)
		except:
			return "_"

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
	    return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
	    return True

def validate_file_size(value):
	from django.core.exceptions import ValidationError
	filesize = value.size
	if filesize > 512000: # maximum size 500 KB
		raise ValidationError("The maximum file size that can be uploaded is 500kb")


class ImageWareHouse(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="image_user")
	image = models.ImageField(blank=True, null=True, upload_to='image_warehouse/', validators=[validate_file_size])
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return str(self.user)