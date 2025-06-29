from ..views import *

@swagger_auto_schema(
    method='post',
    request_body=CriarCategoriasSerializer,
    operation_description="Insere uma nova categoria",
    responses={201: "Categoria criada com sucesso", 400: "Erro de validação"}
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_categorias(request):
    serializer = CriarCategoriasSerializer(data=request.data)
    if serializer.is_valid():
        nome = serializer.validated_data['nome']

        query = "INSERT INTO categorias (nome) VALUES (%s) RETURNING id"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [nome])
                categoria_id = cursor.fetchone()[0]

            return Response({'id': categoria_id, 'mensagem': 'Categoria criada com sucesso'}, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({'erro': 'Categoria já existe ou erro na inserção.'}, status=status.HTTP_400_BAD_REQUEST)


    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
