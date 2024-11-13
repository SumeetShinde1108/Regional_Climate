from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "01 Region"
        

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)


class MonthlyData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    month = models.CharField(max_length=3)  
    value = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('region', 'parameter', 'year', 'month', )

    def __str__(self):
        return f"{self.region.name} - {self.parameter.name} - {self.year.year} - {self.month}"


class SeasonalData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    season = models.CharField(max_length=6)  
    value = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('region', 'parameter', 'year', 'season', )

    def __str__(self):
        return f"{self.region.name} - {self.parameter.name} - {self.year.year} - {self.season}"


class AnnualData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    annual_value = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('region', 'parameter', 'year')

    def __str__(self):
        return f"{self.region.name} - {self.parameter.name} - {self.year.year} - Annual"


