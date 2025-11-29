from django.db import models

# Create your models here.

from farm.models import Farm, Barn, Zone


class RfidTag(models.Model):
    STATUS_CHOICES = (
        ("free", "Free"),
        ("assigned", "Assigned"),
        ("lost", "Lost"),
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="rfid_tags",
        help_text="این تگ در کدام مزرعه ثبت شده است"
    )
    tag_code = models.CharField(
        max_length=100,
        unique=True,
        help_text="کد RFID (UID کارت/گوشی/تگ)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="free",
    )

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="توضیح اختیاری (مثلاً محل فیزیکی تگ زمانی که آزاد است)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rfid_tags"
        verbose_name = "RFID Tag"
        verbose_name_plural = "RFID Tags"
        ordering = ["tag_code"]

    def __str__(self) -> str:
        return f"{self.tag_code} ({self.farm.name})"


class Animal(models.Model):
    STATUS_CHOICES = (
        ("alive", "Alive"),
        ("sold", "Sold"),
        ("dead", "Dead"),
        ("missing", "Missing"),
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="animals",
    )
    barn = models.ForeignKey(
        Barn,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="animals",
    )
    current_zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="animals",
    )

    # رابطه‌ی یک‌به‌یک با تگ RFID (اختیاری)
    rfid_tag = models.OneToOneField(
        RfidTag,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="animal",
        help_text="تگ RFID متصل به این دام (در صورت وجود)"
    )

    species = models.CharField(
        max_length=50,
        help_text="گونه (مثلاً cow, sheep, poultry)"
    )
    breed = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="نژاد (در صورت نیاز)"
    )
    external_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="کد گوشواره، کد سیستم حسابداری یا هر شناسه‌ی خارجی"
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="alive",
    )

    notes = models.TextField(
        null=True,
        blank=True,
        help_text="توضیحات اضافی (وضعیت سلامتی، سوابق مهم، ...)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "animals"
        verbose_name = "Animal"
        verbose_name_plural = "Animals"
        indexes = [
            models.Index(fields=["farm", "barn", "current_zone"]),
            models.Index(fields=["species", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.species} #{self.id} ({self.farm.name})"
