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
            description="Nome da categoria",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: LivrosSerializer(many=True)},
    operation_description="Livros por categoria"
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def livros_por_categoria(request):

    serializer = CategoriaNomeSerializer(data=request.query_params)
    if serializer.is_valid():
        
        categoria = serializer.validated_data['categoria']

        query = """
            SELECT l.id, l.titulo, c.nome as categoria
            FROM livros l 
            JOIN categorias c ON c.id = l.categoria_id
            AND c.nome = %s
            GROUP BY l.id, l.titulo, c.nome
            ORDER BY l.titulo DESC
            LIMIT 10
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [categoria])
            results = dictfetchall(cursor)

        return Response(results, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=CriarLivrosSerializer,
    operation_description="Insere um novo livro",
    responses={201: "Livro criado com sucesso", 400: "Erro de validação"}
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_livro(request):
    serializer = CriarLivrosSerializer(data=request.data)
    if serializer.is_valid():
        titulo = serializer.validated_data['titulo']
        categoria_id = serializer.validated_data['categoria_id']

        query = "INSERT INTO livros (titulo, categoria_id) VALUES (%s, %s) RETURNING id"

        with connection.cursor() as cursor:
            cursor.execute(query, [titulo, categoria_id])
            livro_id = cursor.fetchone()[0]

        return Response({'id': livro_id, 'mensagem': 'Livro criado com sucesso'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='patch',
    request_body=CriarLivrosSerializer,
    responses={200: "Livro atualizado com sucesso", 404: "Livro não foi encontrado", 400: "Erro de validação"},
    operation_description="Atualiza um livro (PATCH)"
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def atualizar_livro(request, livro_id):
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

        parametros.append(livro_id)

        query = f"UPDATE livros SET {', '.join(campos)} WHERE id = %s"
        print(query)

        with connection.cursor() as cursor:
            cursor.execute(query, parametros)
            if cursor.rowcount == 0:
                return Response({"detail": "Livro não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Livro atualizado com sucesso."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='delete',
    responses={204: "Livro apagado com sucesso", 404: "Livro não foi encontrado"},
    operation_description="Apaga um livro através do ID"
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def apagar_livro(request, livro_id):
    """
    Apaga um livro através do ID.
    """
    query = "DELETE FROM livros WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, [livro_id])
        if cursor.rowcount == 0:
            return Response({"detail": "Livro não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)