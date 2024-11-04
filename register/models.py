from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='TIPO')

    class Meta:
        ordering = ['name']
        verbose_name = 'Tipo'

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=15, verbose_name='PREFIXO')

    class Meta:
        ordering = ['name']
        verbose_name = 'Equipe'

    def __str__(self):
        return self.name
    
# Tipo padrão (UC)      
def get_default_service_type():
    return Type.objects.get(pk=1)

# Validador que permite apenas números
numeric_validator = RegexValidator(r'^\d+$', 'O campo deve conter apenas números.')

# Redutor de hora
def diminuir_hora():
    return timezone.now() - timedelta(hours=3)


class Service(models.Model):
    attendant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Atendente', editable=False)
    service_type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Tipo', default=get_default_service_type)
    number = models.CharField(max_length=20, validators=[numeric_validator], verbose_name='Número')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Equipe')
    installment = models.BooleanField(choices=[(True, 'SIM'), (False, 'NÃO')], default=False, verbose_name='Parcelamento')
    first_service = models.BooleanField(default=False, editable=False, verbose_name='Primeiro Atendimento')
    timestamp = models.DateTimeField(default=diminuir_hora, verbose_name='Data e Hora')

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Atendimento'

    def __str__(self):
        return f'{self.attendant} - {self.service_type} - {self.team} - {self.timestamp}'

    def save(self, *args, **kwargs):
        if self.pk is None:  # Se o objeto está sendo criado
        # Obtém a data atual no fuso horário correto
            today = timezone.localtime(timezone.now()).date()
        
        # Faz uma consulta para encontrar o atendimento mais antigo do dia
            earliest_service = Service.objects.filter(
                team=self.team,
                timestamp__date=today
            ).order_by('timestamp').first()
    
        # Define o first_service como True se não houver atendimento anterior ou se este for o mais antigo
            if earliest_service is None or self.timestamp < earliest_service.timestamp:
                self.first_service = True
            else:
                self.first_service = False

        super().save(*args, **kwargs)