from django.db import models

# Create your models here.


class Farm(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(
        max_length=50, unique=True, null=True, blank=True, help_text="کد داخلی/سازمانی مزرعه (اختیاری)"
    )
    location = models.CharField(max_length=500, null=True, blank=True, help_text="آدرس یا توضیح موقعیت مزرعه")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "farms"
        verbose_name = "Farm"
        verbose_name_plural = "Farms"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name or f"Farm #{self.id}"


class Barn(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="barns")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, null=True, blank=True, help_text="مثلاً Barn-A1 یا Shed-3")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "barns"
        verbose_name = "Barn"
        verbose_name_plural = "Barns"
        ordering = ["farm", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.farm.name})"


class Zone(models.Model):
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "zones"
        verbose_name = "Zone"
        verbose_name_plural = "Zones"
        ordering = ["barn", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.barn.name})"
