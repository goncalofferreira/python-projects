from ..views import *

@swagger_auto_schema(
    method='get',
    responses={200: LivrosVendidosSerializer(many=True)},
    operation_description="Top 5 livros mais vendidos por categoria"
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_livros_vendidos(request):
    query = """
        SELECT l.id, l.titulo, c.nome as categoria, SUM(v.quantidade) as vendidos
        FROM vendas v
        JOIN livros l ON l.id = v.livro_id
        JOIN categorias c ON c.id = l.categoria_id
        GROUP BY l.id, l.titulo, c.nome
        ORDER BY vendidos DESC
        LIMIT 5
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = dictfetchall(cursor)

    return Response(results)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'categoria', openapi.IN_QUERY,
            description="Category Name",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: LivrosSerializer(many=True)},
    operation_description="Books by category"
)

@api_view(['GET'])
@throttle_classes([UserBurstThrottle, UserSustainedThrottle, AnonBurstThrottle, AnonSustainedThrottle, CustomUserThrottle])
def livros_por_categoria(request):

    serializer = CategoriaNomeSerializer(data=request.query_params)
    if serializer.is_valid():
        
        categoria = serializer.validated_data['categoria']

        query = """
            SELECT l.id, l.titulo, c.nome as categoria
            FROM livros l 
            JOIN categorias c ON c.id = l.categoria_id
            AND c.nome = %s
            ORDER BY l.titulo DESC            
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [categoria])
            results = dictfetchall(cursor)

        # Paginação manual: Como estou a usar uma query SQL direta, apesar que ter dinifido nos settings.py 'PAGE_SIZE': 5, o DRF não paginará automaticamente.
        paginator = PageNumberPagination()
        paginator.page_size = 5 
        resultados_paginados = paginator.paginate_queryset(results, request)

        data = {
            "total": paginator.page.paginator.count,
            "current_page": paginator.page.number,
            "results": resultados_paginados
        }
        
        if results:
            response = Response(data, status=status.HTTP_200_OK)
        else:
            response = Response({"detail": f"Books not found with category {categoria}"}, status=status.HTTP_200_OK)

        return add_user_throttle_headers(request, response, livros_por_categoria, CustomUserThrottle)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'titulo', openapi.IN_QUERY,
            description="Filter by part of the book title (e.g. 'Django')",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'categoria', openapi.IN_QUERY,
            description="Filter by exact category name (e.g. 'Python')",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: LivrosSerializer(many=True)},
    operation_description="Returns books that match the applied filters (title and category)."
)

@api_view(['GET'])
@throttle_classes([UserBurstThrottle, UserSustainedThrottle, AnonBurstThrottle, AnonSustainedThrottle])
def livros_filtrados(request):
    titulo = request.GET.get('titulo')
    categoria = request.GET.get('categoria')

    query = """
        SELECT l.id, l.titulo, c.nome as categoria
        FROM livros l 
        JOIN categorias c ON c.id = l.categoria_id
        WHERE 1=1
    """
    params = []

    if titulo:
        query += " AND LOWER(l.titulo) LIKE %s"
        params.append(f"%{titulo.lower()}%")
    
    if categoria:
        query += " AND LOWER(c.nome) = %s"
        params.append(categoria.lower())

    query += " ORDER BY l.titulo ASC"

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = dictfetchall(cursor)

    return Response(results)


@swagger_auto_schema(
    method='post',
    request_body=CriarLivrosSerializer,
    operation_description="Insert a new book",
    responses={201: "Book created successfully", 400: "Validation error"}
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([CreateBookThrottle])
def criar_livro(request):
    serializer = CriarLivrosSerializer(data=request.data)
    if serializer.is_valid():
        titulo = serializer.validated_data['titulo']
        categoria_id = serializer.validated_data['categoria_id']

        query = "INSERT INTO livros (titulo, categoria_id) VALUES (%s, %s) RETURNING id"

        with connection.cursor() as cursor:
            cursor.execute(query, [titulo, categoria_id])
            livro_id = cursor.fetchone()[0]

        return Response({'id': livro_id, 'mensagem': 'Book created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='patch',
    request_body=CriarLivrosSerializer,
    responses={200: "Book updated successfully", 404: "Book not found", 400: "Validation error"},
    operation_description="Updates a book (PATCH)"
)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@throttle_classes([UpdateBookThrottle])
def atualizar_livro(request, book_id):
    """
    Atualiza parcialmente o título ou categoria de um livro pelo ID.
    """
    serializer = CriarLivrosSerializer(data=request.data, partial=True)  # partial=True permite atualização parcial
    if serializer.is_valid():
        titulo = serializer.validated_data.get('titulo', None)
        categoria_id = serializer.validated_data.get('categoria_id', None)

        # Construir query dinâmica para atualização conforme campos enviados
        campos = []
        parametros = []
        if titulo is not None:
            campos.append("titulo = %s")
            parametros.append(titulo)
        if categoria_id is not None:
            campos.append("categoria_id = %s")
            parametros.append(categoria_id)

        if not campos:
            return Response({"detail": "Nenhum campo para atualizar."}, status=status.HTTP_400_BAD_REQUEST)

        parametros.append(book_id)

        query = f"UPDATE livros SET {', '.join(campos)} WHERE id = %s"
        print(query)

        with connection.cursor() as cursor:
            cursor.execute(query, parametros)
            if cursor.rowcount == 0:
                return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Book updated successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='delete',
    responses={204: "Book deleted successfully", 404: "Book not found"},
    operation_description="Delete a book by ID"
)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([DeleteBookThrottle])
def apagar_livro(request, book_id):
    """
    Delete a book by ID.
    """
    query = "DELETE FROM livros WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, [book_id])
        if cursor.rowcount == 0:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)
