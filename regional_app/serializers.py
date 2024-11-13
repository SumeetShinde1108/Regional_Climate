from rest_framework import serializers
from .models import Region, Parameter, Year, MonthlyData, SeasonalData, AnnualData


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'name']


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['id', 'year']

class MonthlyDataSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    parameter = ParameterSerializer()
    year = YearSerializer()

    class Meta:
        model = MonthlyData
        fields = ['region', 'parameter', 'year', 'month', 'value']


class SeasonalDataSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    parameter = ParameterSerializer()
    year = YearSerializer()

    class Meta:
        model = SeasonalData
        fields = ['region', 'parameter', 'year', 'season', 'value']


class AnnualDataSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    parameter = ParameterSerializer()
    year = YearSerializer()

    class Meta:
        model = AnnualData
        fields = ['region', 'parameter', 'year', 'annual_value']
