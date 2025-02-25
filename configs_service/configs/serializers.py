from rest_framework import serializers


class CreateConfigSerializer(serializers.Serializer):
    """ Сериализатор для создания конфигов """
    project_id = serializers.UUIDField()
    account_id = serializers.UUIDField(required=False)
    object_type = serializers.CharField()
    data = serializers.JSONField()


class CreateConfigResponseSerializer(serializers.Serializer):
    """ Сериализатор для документации ответа при создании конфигов """
    id = serializers.UUIDField()
    created_date = serializers.DateField()
    modified_date = serializers.DateField()
    project_id = serializers.UUIDField()
    account_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    object_type = serializers.CharField()
    object_item = serializers.UUIDField()
    object_code = serializers.CharField()
    name = serializers.CharField()
    meta = serializers.JSONField()
    data = serializers.JSONField()


class DetailSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    """ Сериализатор для общего ответа об ошибке """
    detail = DetailSerializer()


class HeadersSerializer(serializers.Serializer):
    """ Сериализатор для валидации заголовков Project-ID и Account-ID """
    project_id = serializers.UUIDField()
    account_id = serializers.UUIDField(allow_null=True)

