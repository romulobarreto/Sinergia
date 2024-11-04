from django.contrib import admin
from .models import Type, Team, Service
import csv
from django.http import HttpResponse

def export_service_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=atendimentos.csv'
    response.write(u'\ufeff'.encode('utf8'))  # Adiciona a marca de ordem de bytes (BOM) para UTF-8

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Atendente', 
        'Tipo de Serviço', 
        'Número', 
        'Equipe', 
        'Parcelamento', 
        'Primeiro Atendimento', 
        'Data e Hora'
    ])

    for service in queryset:
        writer.writerow([
            f"{service.attendant.first_name} {service.attendant.last_name}",
            service.service_type.name,
            f"'{service.number}",  # Mantém o zero à esquerda no CSV
            service.team.name,
            'SIM' if service.installment else 'NÃO',
            'SIM' if service.first_service else 'NÃO',
            service.timestamp.strftime('%d/%m/%Y %H:%M'),  # Formata data e hora sem timezone
        ]) 

    return response

export_service_csv.short_description = "Exportar Selecionados para CSV"


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('get_attendant_full_name', 'service_type', 'number', 'team', 'installment', 'first_service', 'timestamp',)
    search_fields = ('attendant__username', 'attendant__first_name', 'attendant__last_name', 'number', 'team__name', 'timestamp',)
    list_filter = ('installment', 'first_service',)
    autocomplete_fields = ['team']
    list_per_page = 15
    actions = [export_service_csv]

    def get_attendant_full_name(self, obj):
        return f"{obj.attendant.first_name} {obj.attendant.last_name}"
    
    get_attendant_full_name.short_description = 'Atendente'

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.attendant = request.user  
        super().save_model(request, obj, form, change)

    
