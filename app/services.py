# Importa a classe base de serviço do framework gRPC
from djangogrpcframework.services import Service
# Importa nossos modelos Django
from .models import Project
# Importa o código gRPC que geramos
from . import projetos_pb2
from . import projetos_pb2_grpc

class ProjetoService(Service):

    def ListarProjetos(self, request, context):
        # 1. Buscamos os projetos do banco de dados, já com a otimização de performance.
        projetos_queryset = Project.objects.all().prefetch_related('members')
        
        # 2. Preparamos uma lista para guardar os projetos no formato Protobuf.
        projetos_proto_list = []

        # 3. Iteramos sobre os projetos do Django e os "traduzimos" para o formato Protobuf.
        for projeto in projetos_queryset:
            membros_proto_list = []
            for membro in projeto.members.all():
                membros_proto_list.append(projetos_pb2.Usuario(id=membro.id, username=membro.username))

            projeto_proto = projetos_pb2.Projeto(
                id=projeto.id,
                title=projeto.title,
                description=projeto.description or "", # Garante que não enviamos None
                members=membros_proto_list
            )
            projetos_proto_list.append(projeto_proto)

        # 4. Criamos a mensagem de resposta final e retornamos.
        response = projetos_pb2.ListarProjetosResponse(projetos=projetos_proto_list)
        return response