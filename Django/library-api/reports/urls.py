from django.urls import path
from .views.v_categorias import *
from .views.v_livros import *

urlpatterns = [
    path('books/best_sellers/', top_livros_vendidos),
    path('books/by_category/', livros_por_categoria),
    path('books/new/', criar_livro),
    path('books/<int:livro_id>/update/', atualizar_livro), 
    path('books/<int:livro_id>/delete/', apagar_livro), 
    #
    path('categories/new/', criar_categorias),

]
