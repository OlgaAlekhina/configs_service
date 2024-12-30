from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter, inline_serializer
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ErrorResponseSerializer, HeadersSerializer, CreateConfigSerializer, DetailSerializer, \
    CreateConfigResponseSerializer
from .services import get_configs, create_config


class BaseContestView(APIView):
    """Родительский класс для исключения дублирования кода в части документация swagger."""

    COMMON_RESPONSES = {
        400:OpenApiResponse(
            description="Ошибка клиента при запросе данных",
            response=ErrorResponseSerializer()
        ),
        401: OpenApiResponse(
            description="Необходима аутентификация",
            response=ErrorResponseSerializer()
        ),
        403: OpenApiResponse(
            description="Доступ запрещён",
            response=ErrorResponseSerializer()
        ),
        404: OpenApiResponse(
            description="Не найдено",
            response=ErrorResponseSerializer()
        ),
        500: OpenApiResponse(
            description="Ошибка сервера при обработке запроса",
            response=ErrorResponseSerializer()
        ),
    }


class GetConfigView(BaseContestView):
    # permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Получение идентификаторов типа {config_type} из реестра",
        description="""Получение идентификаторов типа {config_type} из реестра. Можно запросить несколько типов конфигов через 
                    запятую без пробела. Все существующие типы конфигов можно посмотреть в методе GET /configs.""",
        parameters=[
            OpenApiParameter('Project-ID', OpenApiTypes.UUID, OpenApiParameter.HEADER, required=True),
            OpenApiParameter('Account-ID', OpenApiTypes.UUID, OpenApiParameter.HEADER)
        ],
        responses={
            200: OpenApiResponse(
                description="Successful Response",
                response=inline_serializer(name='Config', fields={'detail': DetailSerializer(), 'data': serializers.JSONField()})
            ),
            **BaseContestView.COMMON_RESPONSES
        },
        tags=['Configs']
    )
    def get(self, request, config_type):
        project_id = request.META.get('HTTP_PROJECT_ID') if request.META.get('HTTP_PROJECT_ID') else None
        account_id = request.META.get('HTTP_ACCOUNT_ID') if request.META.get('HTTP_ACCOUNT_ID') else None
        serializer = HeadersSerializer(data={'project_id': project_id, 'account_id': account_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        response_data = get_configs(project_id=project_id, account_id=account_id, configs=[config_type])
        if not response_data.get('data'):
            return Response({'detail': dict(code='NOT_FOUND', message='Конфиги не найдены.')},
                            status=status.HTTP_404_NOT_FOUND)
        response = {'detail': dict(code='OK', message=f'Данные по конфигам типа {config_type}.')}
        response.update(response_data)
        return Response(response)


class ConfigsView(BaseContestView):
    # permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        operation_id='get_all_configs', # чтобы убрать 'Warning: operationId  has collisions. resolving with numeral suffixes.'
        summary="Получение всех идентификаторов из реестра",
        description="Получение всех идентификаторов для данных Project-ID и Account-ID.",
        parameters=[
            OpenApiParameter('Project-ID', OpenApiTypes.UUID, OpenApiParameter.HEADER, required=True),
            OpenApiParameter('Account-ID', OpenApiTypes.UUID, OpenApiParameter.HEADER)
        ],
        responses={
            200: OpenApiResponse(
                description="Successful Response",
                response=inline_serializer(name='Configs', fields={'detail': DetailSerializer(), 'data': serializers.JSONField()})
            ),
            **BaseContestView.COMMON_RESPONSES
        },
        tags=['Configs']
    )
    def get(self, request):
        project_id = request.META.get('HTTP_PROJECT_ID') if request.META.get('HTTP_PROJECT_ID') else None
        account_id = request.META.get('HTTP_ACCOUNT_ID') if request.META.get('HTTP_ACCOUNT_ID') else None
        serializer = HeadersSerializer(data={'project_id': project_id, 'account_id': account_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        response_data = get_configs(project_id=project_id, account_id=account_id, configs=[])
        if not response_data.get('data'):
            return Response({'detail': dict(code='NOT_FOUND', message='Конфиги не найдены.')},
                            status=status.HTTP_404_NOT_FOUND)
        response = {'detail': dict(code='OK', message='Получены все конфиги для данных Project-ID и Account-ID.')}
        response.update(response_data)
        return Response(response)


    @extend_schema(
        summary="Добавление идентификаторов в реестр",
        description="Добавление идентификаторов в реестр",
        parameters=[
            OpenApiParameter('Project-ID', OpenApiTypes.UUID, OpenApiParameter.HEADER, required=True),
            OpenApiParameter('Account-ID', OpenApiTypes.UUID, OpenApiParameter.HEADER)
        ],
        request=CreateConfigSerializer,
        responses={
            201: OpenApiResponse(
                description="Successful Response",
                response=inline_serializer(name='CreateConfigs', fields={'detail': DetailSerializer(), 'data': CreateConfigResponseSerializer()})
            ),
            **BaseContestView.COMMON_RESPONSES
        },
        tags=['Configs']
    )
    def post(self, request):
        project_id = request.META.get('HTTP_PROJECT_ID') if request.META.get('HTTP_PROJECT_ID') else None
        account_id = request.META.get('HTTP_ACCOUNT_ID') if request.META.get('HTTP_ACCOUNT_ID') else None
        serializer = HeadersSerializer(data={'project_id': project_id, 'account_id': account_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        request_data = request.data
        serializer = CreateConfigSerializer(data=request_data)
        if serializer.is_valid():
            project_id = serializer.validated_data['project_id']
            account_id = serializer.validated_data['account_id'] if 'account_id' in serializer.validated_data else ''
            object_type = serializer.validated_data['object_type']
            data = serializer.validated_data['data']
            config_data = {
                "project_id": str(project_id),
                "account_id": str(account_id) if account_id else None,
                # "user_id": request.auth.get('user_id'),
                "object_type": object_type,
                "object_code": f"{project_id}:{account_id}:{object_type}",
                # "object_item": serializer.validated_data['object_item'],
                # "name": serializer.validated_data['name'],
                "data": data
            }
            response_data = create_config(config_data)
            return Response(response_data[0], response_data[1])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

