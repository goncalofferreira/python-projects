from django.urls import path
from .views.v_categories import *
from .views.v_books import *

urlpatterns = [
    path('books/best_sellers/', top_livros_vendidos),
    path('books/by_category/', livros_por_categoria),
    path('books/filtered/', livros_filtrados),
    path('books/new/', criar_livro),
    path('books/<int:book_id>/update/', atualizar_livro), 
    path('books/<int:book_id>/delete/', apagar_livro), 
    #
    path('categories/new/', criar_categorias),

]
