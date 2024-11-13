from .models import Year, MonthlyData, SeasonalData, AnnualData
from django.db import transaction

def parse_weather_data(data_text, region, parameter):
    lines = data_text.splitlines()[6:] 
    monthly_data_objects = []
    seasonal_data_objects = []
    annual_data_objects = []

    for line in lines:
        columns = line.split()
        
        if len(columns) < 13:
            print(f"Skipping malformed line: {line}")
            continue

        try:
            year = int(columns[0])
            year_obj, _ = Year.objects.get_or_create(year=year)
            
            monthly_values = [
                float(columns[i]) if columns[i] != "---" else None
                for i in range(1, 13)
            ]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for month, value in zip(months, monthly_values):
                monthly_data_objects.append(
                    MonthlyData(region=region, parameter=parameter, year=year_obj, month=month, value=value)
                )

            seasonal_values = [
                float(columns[i]) if len(columns) > i and columns[i] != "---" else None
                for i in range(13, 17)
            ]
            seasons = ["Winter", "Spring", "Summer", "Autumn"]
            for season, value in zip(seasons, seasonal_values):
                seasonal_data_objects.append(
                    SeasonalData(region=region, parameter=parameter, year=year_obj, season=season, value=value)
                )

            if len(columns) > 17 and columns[17] != "---":
                annual_data_objects.append(
                    AnnualData(region=region, parameter=parameter, year=year_obj, annual_value=float(columns[17]))
                )

        except ValueError as e:
            print(f"Error parsing line: {line} - {e}")

    with transaction.atomic():
        MonthlyData.objects.bulk_create(monthly_data_objects)
        SeasonalData.objects.bulk_create(seasonal_data_objects)
        AnnualData.objects.bulk_create(annual_data_objects)
