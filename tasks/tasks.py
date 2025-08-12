# tasks/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date

User = get_user_model()

@shared_task
def send_assignment_email_task(task_id, reason="assigned"):
    try:
        t = Task.objects.select_related("assigned_to","project").get(pk=task_id)
    except Task.DoesNotExist:
        return f"Task {task_id} not found"

    if not t.assigned_to or not t.assigned_to.email:
        return "No recipient"

    subject = ""
    message = ""
    if reason == "assigned":
        subject = f"New task assigned: {t.title}"
        message = f"You were assigned to task '{t.title}' in project '{t.project.name}'.\n\nDescription: {t.description}\nDue: {t.due_date}\n\nOpen the app to view more details."
    elif reason == "status_changed":
        subject = f"Task status updated: {t.title}"
        message = f"The status of task '{t.title}' changed to {t.status}.\n\nProject: {t.project.name}"
    
    recipient_email = "sample@gmail.com"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )
    return f"Email sent to {recipient_email}"

@shared_task
def send_overdue_summary_task():
    today = date.today()
    # find tasks overdue and not done, grouped by assigned user
    overdue = Task.objects.filter(due_date__lt=today).exclude(status="done").select_related("assigned_to")
    users = {}
    for t in overdue:
        if t.assigned_to and t.assigned_to.email:
            users.setdefault(t.assigned_to.email, []).append(t)
    for email, tasks in users.items():
        subject = "Daily overdue tasks summary"
        body = "You have the following overdue tasks:\n\n"
        for t in tasks:
            body += f"- {t.title} (project: {t.project.name}, due: {t.due_date})\n"
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    return "Overdue summary sent"
