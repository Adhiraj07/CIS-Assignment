from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task
import logging

logger = logging.getLogger(__name__)

# Signals removed - functionality moved to management command
