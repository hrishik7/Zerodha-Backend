from equity_data.models import EquityData
from rest_framework import serializers


class EquityDataSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    close = serializers.FloatField()
    # class Meta:
    #     model = EquityData
    #     fields = ['code' , 'name', 'open', 'high' , 'low' , 'close']
