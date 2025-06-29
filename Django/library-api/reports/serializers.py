from rest_framework import serializers

class LivrosSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    titulo = serializers.CharField()
    categoria = serializers.CharField()

class LivrosVendidosSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    titulo = serializers.CharField()
    categoria = serializers.CharField()
    vendidos = serializers.IntegerField()

class CriarLivrosSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=255)
    categoria_id = serializers.IntegerField()

class CategoriasSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()    

class CriarCategoriasSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255)

class CategoriaNomeSerializer(serializers.Serializer):
    categoria = serializers.CharField()
                