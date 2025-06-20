from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from core.models import User, Task
from django.db.models import Q
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Deactivate users with 5+ missed tasks in last week'
    
    def handle(self, *args, **options):
        today = timezone.now()
        last_week = today - timedelta(days=7)
        grace_period = today - timedelta(hours=24)
        
        # Only check users who are either active or were deactivated before grace period
        users = User.objects.filter(
            Q(is_active=True) | 
            Q(is_active=False, last_deactivation__lt=grace_period)
        )
        
        deactivated_count = 0
        
        for user in users:
            missed_count = Task.objects.filter(
                assigned_to=user,
                status='MISSED',
                deadline__range=(last_week, today)
            ).count()
            
            if missed_count >= 5:
                user.is_active = False
                user.last_deactivation = timezone.now()
                user.save()
                logger.warning(f"Deactivated {user.username} for {missed_count} missed tasks")
                deactivated_count += 1
        
        if deactivated_count:
            logger.info(f"Deactivated {deactivated_count} users")
        else:
            logger.info("No users met deactivation criteria")
