from django.contrib import admin
from .models import Categoria, Produto

admin.site.site_header = 'Lanchonete - Painel Administrativo'


class ProdutoInline(admin.TabularInline):
    model = Produto
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    inlines = [ProdutoInline]


@admin.action(description='Marcar como indisponível')
def marcar_indisponivel(modeladmin, request, queryset):
    queryset.update(disponivel=False)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria', 'disponivel')
    list_filter = ('categoria', 'disponivel')
    search_fields = ('nome',)
    list_editable = ('disponivel',)
    actions = [marcar_indisponivel]