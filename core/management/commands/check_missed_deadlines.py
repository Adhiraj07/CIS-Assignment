from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, Task
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Checks for users with 5+ missed tasks in past week and deactivates them'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)
        active_users = User.objects.filter(is_active=True)
        
        for user in active_users:
            missed_count = Task.objects.filter(
                assigned_to=user,
                status='MISSED',
                deadline__gte=week_ago
            ).count()
            
            if missed_count >= 5:
                user.is_active = False
                user.save()
                logger.warning(
                    f"Deactivated user {user.username} "
                    f"for {missed_count} missed tasks"
                )
                
                # Log task details for managers
                tasks = Task.objects.filter(
                    assigned_to=user,
                    status='MISSED',
                    deadline__gte=week_ago
                )[:5]  # Show first 5 as sample
                
                for task in tasks:
                    logger.warning(
                        f"Missed Task: {task.title} "
                        f"(Deadline: {task.deadline})"
                    )
