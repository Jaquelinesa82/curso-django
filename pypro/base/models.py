from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Crie e salve um usuário com o nome de usuário, e-mail e senha fornecidos.
        """
        if not username:
            raise ValueError('O nome de usuário fornecido deve ser definido')
        #  Normalize o endereço de e-mail colocando em letras minúsculas a parte do domínio dele.
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Classe de usuário base do aplicativo.

    E-mail e senha são obrigatórios. Outros campos são opcionais.
    """

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    #  is_staff => defina os usuários que podem acessar o admin do django
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('indica se o usuário pode fazer login neste site de administração.'),
    )
    #  is_active => define o usuário que pode se logar dentro do sistema.
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designa se este usuário deve ser tratado como ativo. '
            'Desmarque isto em vez de deletar contas.'
        ),
    )
    #  date_joined => define quando o usuário entrou no sistema.
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #  class Meta => define algunas classe global no caso essa será uma concreta.
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Retorne o first_name mais o último_name, com um espaço no meio.
        """
        full_name = '%s' % (self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """Retorne o nome abreviado do usuário."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envie um email para este usuário."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
