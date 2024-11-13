from django.contrib import admin
from .models import Region, Parameter, Year, MonthlyData, SeasonalData, AnnualData


class MonthlyDataInline(admin.StackedInline):
    model = MonthlyData
    fields = ('parameter', 'month', 'value')  
    ordering = ('month',)  


class SeasonalDataInline(admin.StackedInline):
    model = SeasonalData
    fields = ('parameter', 'season', 'value')
    ordering = ('season',)


class AnnualDataInline(admin.StackedInline):
    model = AnnualData
    fields = ('parameter', 'annual_value')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [MonthlyDataInline, SeasonalDataInline, AnnualDataInline] 


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)
    inlines = [MonthlyDataInline, SeasonalDataInline, AnnualDataInline]  


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MonthlyData)
class MonthlyDataAdmin(admin.ModelAdmin):
    list_display = ('region', 'parameter', 'year', 'month', 'value')
    list_filter = ('region', 'parameter', 'year', 'month')
    search_fields = ('region__name', 'parameter__name', 'year__year', 'month')
    ordering = ('year', 'month', 'region', 'parameter')


@admin.register(SeasonalData)
class SeasonalDataAdmin(admin.ModelAdmin):
    list_display = ('region', 'parameter', 'year', 'season', 'value')
    list_filter = ('region', 'parameter', 'year', 'season')
    search_fields = ('region__name', 'parameter__name', 'year__year', 'season')
    ordering = ('year', 'season', 'region', 'parameter')


@admin.register(AnnualData)
class AnnualDataAdmin(admin.ModelAdmin):
    list_display = ('region', 'parameter', 'year', 'annual_value')
    list_filter = ('region', 'parameter', 'year')
    search_fields = ('region__name', 'parameter__name', 'year__year')
    ordering = ('year', 'region', 'parameter')

