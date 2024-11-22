from rest_framework import serializers
from .models import Log, SourceLog

class SourceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceLog
        fields = ['url', 'is_digital', 'text', 'meta_data']

class LogSerializer(serializers.ModelSerializer):
    sources = SourceLogSerializer(many=True)

    class Meta:
        model = Log
        fields = ['description', 'category', 'log_key', 'start_time', 'end_time', 'is_public', 'sources']

    def create(self, validated_data):
        sources_data = validated_data.pop('sources')
        log = Log.objects.create(**validated_data)
        for source_data in sources_data:
            SourceLog.objects.create(log=log, **source_data)
        return log
