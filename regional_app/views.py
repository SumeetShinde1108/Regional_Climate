from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound , ValidationError 
from rest_framework.decorators import api_view 
from rest_framework import status
from django.db.models import Prefetch
from .models import Region, Parameter, Year, MonthlyData, SeasonalData, AnnualData
from .serializers import MonthlyDataSerializer, SeasonalDataSerializer, AnnualDataSerializer

class WeatherDataView(APIView):
    def get(self, request):
        region_name = request.query_params.get('region')
        parameter_name = request.query_params.get('parameter')
        year_value = request.query_params.get('year')

        if not (region_name and parameter_name and year_value):
            return Response({"error": "region, parameter, and year query parameters are required."}, status=400)

        try:
            region = Region.objects.get(name=region_name)
            parameter = Parameter.objects.get(name=parameter_name)
            year = Year.objects.get(year=year_value)
        except (Region.DoesNotExist, Parameter.DoesNotExist, Year.DoesNotExist):
            raise NotFound("Region, Parameter, or Year not found.")

        include_monthly = request.query_params.get('month', 'true').lower() == 'true'
        include_seasonal = request.query_params.get('season', 'true').lower() == 'true'
        include_annual = request.query_params.get('annual', 'true').lower() == 'true'

        response_data = {
            'region': region.name,
            'parameter': parameter.name,
            'year': year.year,
        }

        if include_monthly:
            monthly_data = MonthlyData.objects.filter(region=region, parameter=parameter, year=year)
            months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_data_dict = {month.lower(): None for month in months_order}
            for entry in monthly_data:
                monthly_data_dict[entry.month.lower()] = entry.value
            response_data['monthly_data'] = monthly_data_dict

        if include_seasonal:
            seasonal_data = SeasonalData.objects.filter(region=region, parameter=parameter, year=year)
            seasons_order = ['Winter', 'Spring', 'Summer', 'Autumn']
            seasonal_data_dict = {season.lower(): None for season in seasons_order}
            for entry in seasonal_data:
                seasonal_data_dict[entry.season.lower()] = entry.value
            response_data['seasonal_data'] = seasonal_data_dict

        if include_annual:
            annual_data = AnnualData.objects.filter(region=region, parameter=parameter, year=year).first()
            response_data['annual_data'] = annual_data.annual_value if annual_data else None

        return Response(response_data)

@api_view(['GET'])
def get_years(request):
    years = Year.objects.values_list('year',flat=True).order_by('year')
    return Response(years)

@api_view(['GET'])
def get_parameters(request):
    parameters = Parameter.objects.values_list('name',flat=True)
    return Response(parameters)

@api_view(['GET'])
def get_regions(request):
    regions = Region.objects.values_list('name',flat=True)
    return Response(regions)

class WeatherDataCreateView(APIView):
    def post(self, request):
        region_name = request.data.get('region')
        parameter_name = request.data.get('parameter')
        year_value = request.data.get('year')

        if not (region_name and parameter_name and year_value):
            return Response({"error": "region, parameter, and year fields are required."}, status=400)

        try:
            region, _ = Region.objects.get_or_create(name=region_name)
            parameter, _ = Parameter.objects.get_or_create(name=parameter_name)
            year, _ = Year.objects.get_or_create(year=year_value)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        monthly_data = request.data.get('monthly_data', [])
        for entry in monthly_data:
            month = entry.get('month')
            value = entry.get('value')
            if month and value is not None:
                MonthlyData.objects.update_or_create(
                    region=region,
                    parameter=parameter,
                    year=year,
                    month=month,
                    defaults={'value': value}
                )

        seasonal_data = request.data.get('seasonal_data', [])

        for entry in seasonal_data:
            season = entry.get('season')
            value = entry.get('value')

            if season and value is not None:
                SeasonalData.objects.update_or_create(
                    region=region,
                    parameter=parameter,
                    year=year,
                    season=season,
                    defaults={'value': value}
                )

        annual_value = request.data.get('annual_data', {}).get('annual_value')
        if annual_value is not None:
            AnnualData.objects.update_or_create(
                region=region,
                parameter=parameter,
                year=year,
                defaults={'annual_value': annual_value}
            )

        return Response({"message": "Data successfully created/updated."}, status=201)

class WeatherAnalyticsView(APIView):
    def get(self, request):
        region_name = request.query_params.get('region')
        parameter_name = request.query_params.get('parameter')
        year_value = request.query_params.get('year')

        if not (region_name and parameter_name and year_value):
            return Response({"error": "region, parameter, and year query parameters are required."}, status=400)

        try:
            region = Region.objects.get(name=region_name)
            parameter = Parameter.objects.get(name=parameter_name)
            year = Year.objects.get(year=year_value)
        except (Region.DoesNotExist, Parameter.DoesNotExist, Year.DoesNotExist):
            raise NotFound("Region, Parameter, or Year not found.")

        monthly_data = MonthlyData.objects.filter(region=region, parameter=parameter, year=year)

        if not monthly_data.exists():
            return Response({"error": "No data found for the specified criteria."}, status=404)

        max_temp= monthly_data.order_by('-value').first()
        min_temp= monthly_data.order_by('value').first()

        
        analytics_data = {
            "region": region_name,
            "parameter": parameter_name,
            "year": year_value,
            "maximum_temp": {
                "month": max_temp.month,
                "value": max_temp.value,
            },
            "minimum_temp": {
                "month": min_temp.month,
                "value": min_temp.value,
            }
        }

        return Response(analytics_data)

def home(request):
    regions = Region.objects.values_list('name', flat=True)
    parameters = Parameter.objects.values_list('name', flat=True)
    years = Year.objects.values_list('year', flat=True).order_by('year')
    
    return render(request, 'home.html', {
        'regions': regions,
        'parameters': parameters,
        'years': years,
    })

def weather_data(request):
    view = WeatherDataView.as_view()
    response = view(request).data 
    return render(request, 'weather_data.html', response)

def analytical_data(request):
    view = WeatherAnalyticsView.as_view()
    response=view(request).data
    return render(request,'weather_analysis.html', response)




    