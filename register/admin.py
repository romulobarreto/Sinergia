from django.contrib import admin
from .models import Type, Team, Service, CustomUser
import csv
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# ================== EXPORTAÇÃO CSV ==================
def export_service_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=atendimentos.csv'
    response.write(u'\ufeff'.encode('utf8'))  # BOM para UTF-8

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
            f"'{service.number}",  # Mantém o zero à esquerda
            service.team.name,
            'SIM' if service.installment else 'NÃO',
            'SIM' if service.first_service else 'NÃO',
            service.timestamp.strftime('%d/%m/%Y %H:%M'),
        ])

    return response

export_service_csv.short_description = "Exportar Selecionados para CSV"


# ================== ADMIN MODELS ==================
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'regional')
    search_fields = ('name',)
    list_filter = ('regional',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(regional=request.user.regional)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'get_attendant_full_name', 'service_type', 'number',
        'team', 'installment', 'first_service', 'timestamp',
    )
    search_fields = (
        'attendant__username', 'attendant__first_name', 'attendant__last_name',
        'number', 'team__name', 'timestamp',
    )
    list_filter = ('installment', 'first_service',)
    autocomplete_fields = ['team']
    list_per_page = 15
    actions = [export_service_csv]

    # ================== CAMPOS CUSTOMIZADOS ==================
    def get_attendant_full_name(self, obj):
        return f"{obj.attendant.first_name} {obj.attendant.last_name}"
    get_attendant_full_name.short_description = 'Atendente'

    # ================== FILTRAR POR REGIONAL ==================
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team__regional=request.user.regional)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filtra os times disponíveis de acordo com a regional do usuário"""
        if db_field.name == "team" and not request.user.is_superuser:
            kwargs["queryset"] = Team.objects.filter(regional=request.user.regional)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Força que o atendente seja sempre o user logado
        e valida se a equipe pertence à mesma regional do atendente."""
        if not obj.pk:
            obj.attendant = request.user

        # 🔒 Segurança extra: impede registrar em equipe de outra regional
        if not request.user.is_superuser and obj.team.regional != request.user.regional:
            raise ValidationError("Você não pode registrar atendimento para uma equipe de outra regional.")

        super().save_model(request, obj, form, change)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Quais campos aparecem na tabela de listagem
    list_display = ("username", "first_name", "last_name", "email", "regional", "is_staff")

    # Filtros laterais
    list_filter = ("regional", "is_staff", "is_superuser", "groups")

    # Campos para busca
    search_fields = ("username", "first_name", "last_name", "email")

    # Campos exibidos ao editar usuário
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações Pessoais", {"fields": ("first_name", "last_name", "email", "regional")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos exibidos ao adicionar novo usuário
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "regional", "password1", "password2"),
        }),
    )