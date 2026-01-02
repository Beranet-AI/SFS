# livestock/infrastructure/db.py
from .db import atomic
from contextlib import contextmanager
from django.db import transaction

@contextmanager
def atomic():
    """
    Unit of Work boundary for Livestock aggregate
    """
    with transaction.atomic():
        yield
