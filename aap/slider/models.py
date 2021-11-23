"""Slider app models."""
from django.db import models

from base.models import Base


class Slide(Base):
    """Slide model implementation."""

    title = models.CharField(max_length=1024, null=False, unique=True)
    content = models.TextField(null=False)
    image = models.URLField()
    is_draft = models.BooleanField(default=False)
    # How many visitors clicked on slide link
    # visited = models.PositiveIntegerField(default=0)
    order = models.PositiveSmallIntegerField(null=False, unique=True)
    link = models.URLField()
    is_approved = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    expire_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        if self.is_deleted:
            return f"{self.title} [deleted]"
        if self.is_draft:
            return f"{self.title} [draft]"
        return self.title
