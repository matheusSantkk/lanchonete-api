from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, MunicipiosView

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('produtos', ProdutoViewSet)

urlpatterns = [
    path('municipios/', MunicipiosView.as_view()),
    path('', include(router.urls)),
]