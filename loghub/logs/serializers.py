from rest_framework import serializers
from .models import Log, SourceLog
from django.utils import timezone

class SourceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceLog
        fields = ['url', 'is_digital', 'text', 'meta_data']


class LogSerializer(serializers.ModelSerializer):
    source = SourceLogSerializer(many=True)

    class Meta:
        model = Log
        fields = ['description', 'category', 'log_key', 'start_time', 'end_time', 'is_public', 'source']
        extra_kwargs = {
            'log_key': {'read_only': True},
        }
    def create(self, validated_data):
        source_data = validated_data.pop('source', [])
        log = Log.objects.create(**validated_data)

        for source in source_data:
            SourceLog.objects.create(log=log, **source)

        return log

    def validate(self, attrs):
        start_time = attrs.get('start_time', timezone.now())
        end_time = attrs.get('end_time')

        if end_time and end_time < start_time:
            raise serializers.ValidationError("End time must be greater than or equal to start time.")

        return attrs