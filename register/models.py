from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from datetime import timedelta

# =========================
# Custom User
# =========================
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    REGIONAL_CHOICES = [
        ('N', 'Norte'),
        ('S', 'Sul'),
    ]

    regional = models.CharField(
        max_length=1,
        choices=REGIONAL_CHOICES,
        default='S',
        verbose_name="Regional"
    )

    def __str__(self):
        return f"{self.username} - {self.get_regional_display()}"


# =========================
# Tipo
# =========================
class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='TIPO')

    class Meta:
        ordering = ['name']
        verbose_name = 'Tipo'

    def __str__(self):
        return self.name
    

# =========================
# Equipe
# =========================
class Team(models.Model):
    REGIONAL_CHOICES = [
        ('N', 'Norte'),
        ('S', 'Sul'),
    ]

    name = models.CharField(max_length=15, verbose_name='PREFIXO')
    regional = models.CharField(
        max_length=1,
        choices=REGIONAL_CHOICES,
        default='S',
        verbose_name="Regional"
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Equipe'

    def __str__(self):
        return f"{self.name} - {self.get_regional_display()}"


# =========================
# Helpers
# =========================
def get_default_service_type():
    return Type.objects.get(pk=1)

# Validador que permite apenas números
numeric_validator = RegexValidator(r'^\d+$', 'O campo deve conter apenas números.')

# Redutor de hora
def diminuir_hora():
    return timezone.now() - timedelta(hours=3)


# =========================
# Atendimento
# =========================
class Service(models.Model):
    attendant = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # 🔹 agora usa o CustomUser
        on_delete=models.CASCADE,
        verbose_name='Atendente',
        editable=False
    )
    service_type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        verbose_name='Tipo',
        default=get_default_service_type
    )
    number = models.CharField(
        max_length=20,
        validators=[numeric_validator],
        verbose_name='Número'
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Equipe')
    installment = models.BooleanField(
        choices=[(True, 'SIM'), (False, 'NÃO')],
        default=False,
        verbose_name='Parcelamento'
    )
    first_service = models.BooleanField(default=False, editable=False, verbose_name='Primeiro Atendimento')
    timestamp = models.DateTimeField(default=diminuir_hora, verbose_name='Data e Hora')

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Atendimento'

    def __str__(self):
        return f'{self.attendant} - {self.service_type} - {self.team} - {self.timestamp}'

    def save(self, *args, **kwargs):
        if self.pk is None:  # Se o objeto está sendo criado
            today = timezone.localtime(timezone.now()).date()
            earliest_service = Service.objects.filter(
                team=self.team,
                timestamp__date=today
            ).order_by('timestamp').first()

            if earliest_service is None or self.timestamp < earliest_service.timestamp:
                self.first_service = True
            else:
                self.first_service = False

        super().save(*args, **kwargs)
