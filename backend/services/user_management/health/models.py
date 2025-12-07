from __future__ import annotations

from django.db import models
from django.utils import timezone


class Cow(models.Model):
    """Domain model for dairy cows extending the generic Animal registry."""

    animal = models.OneToOneField(
        "livestock.Animal",
        on_delete=models.CASCADE,
        related_name="cow_profile",
        help_text="Animal record for this cow",
    )
    lactation_stage = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Early, mid, late, or dry",
    )
    parity = models.PositiveIntegerField(
        default=0,
        help_text="Number of calvings",
    )
    days_in_milk = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Days since last calving",
    )
    last_calving_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cows"
        verbose_name = "Cow"
        verbose_name_plural = "Cows"
        indexes = [models.Index(fields=["parity", "lactation_stage"])]

    def __str__(self) -> str:
        return f"Cow {self.animal.id} ({self.lactation_stage or 'unknown stage'})"


class Disease(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    symptoms = models.JSONField(
        null=True,
        blank=True,
        help_text="List of dominant symptoms or markers",
    )
    detection_methods = models.JSONField(
        null=True,
        blank=True,
        help_text="Algorithms, heuristics, or lab methods used",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "diseases"
        verbose_name = "Disease"
        verbose_name_plural = "Diseases"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class MLModel(models.Model):
    """Metadata for trained ML models used for diagnosis."""

    name = models.CharField(max_length=200)
    version = models.CharField(max_length=50, default="1.0.0")
    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        related_name="models",
    )
    framework = models.CharField(
        max_length=50,
        help_text="sklearn, pytorch, tensorflow, onnx, etc.",
    )
    artifact_path = models.CharField(
        max_length=500,
        help_text="URI to the serialized model artifact",
    )
    input_schema = models.JSONField(
        help_text="List of expected features and shapes",
    )
    metrics = models.JSONField(
        null=True,
        blank=True,
        help_text="Evaluation metrics for the specific version",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Flag to indicate preferred version for inference",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ml_models"
        verbose_name = "ML Model"
        verbose_name_plural = "ML Models"
        ordering = ["name", "version"]
        unique_together = ("name", "version")

    def __str__(self) -> str:
        return f"{self.name} v{self.version} ({self.framework})"


class SensorData(models.Model):
    QUALITY_CHOICES = (
        ("good", "Good"),
        ("suspect", "Suspect"),
        ("bad", "Bad"),
    )

    sensor = models.ForeignKey(
        "devices.Sensor",
        on_delete=models.PROTECT,
        related_name="health_data",
    )
    sensor_type = models.ForeignKey(
        "devices.SensorType",
        on_delete=models.PROTECT,
        related_name="health_sensor_data",
    )
    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="sensor_data",
        null=True,
        blank=True,
    )
    ts = models.DateTimeField(db_index=True)
    value = models.FloatField()
    unit = models.CharField(max_length=20, null=True, blank=True)
    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES,
        default="good",
    )
    raw_payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sensor_data"
        verbose_name = "Sensor Data"
        verbose_name_plural = "Sensor Data"
        indexes = [
            models.Index(fields=["sensor", "ts"]),
            models.Index(fields=["cow", "ts"]),
        ]
        ordering = ["-ts"]

    def __str__(self) -> str:
        return f"{self.sensor} @ {self.ts} = {self.value}"


class Prediction(models.Model):
    STATUS_CHOICES = (
        ("healthy", "Healthy"),
        ("suspected", "Suspected"),
        ("at_risk", "At Risk"),
    )

    model = models.ForeignKey(
        MLModel,
        on_delete=models.PROTECT,
        related_name="predictions",
    )
    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        related_name="predictions",
    )
    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="predictions",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="healthy",
    )
    probability = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Probability or confidence score",
    )
    predicted_at = models.DateTimeField(default=timezone.now, db_index=True)
    features = models.JSONField(
        help_text="Feature vector used for prediction",
    )
    feature_window_start = models.DateTimeField(null=True, blank=True)
    feature_window_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "predictions"
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
        indexes = [
            models.Index(fields=["cow", "predicted_at"]),
            models.Index(fields=["disease", "predicted_at"]),
        ]
        ordering = ["-predicted_at"]

    def __str__(self) -> str:
        return f"{self.disease} prediction for {self.cow}"


class DiseaseRecord(models.Model):
    STATUS_CHOICES = (
        ("suspected", "Suspected"),
        ("confirmed", "Confirmed"),
        ("recovered", "Recovered"),
    )

    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="disease_records",
    )
    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        related_name="records",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="suspected",
    )
    source_prediction = models.ForeignKey(
        Prediction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="disease_records",
    )
    diagnosed_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "disease_records"
        verbose_name = "Disease Record"
        verbose_name_plural = "Disease Records"
        indexes = [
            models.Index(fields=["cow", "disease", "diagnosed_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.disease} for {self.cow} ({self.status})"
