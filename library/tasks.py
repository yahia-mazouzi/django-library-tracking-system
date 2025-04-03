from datetime import date, time
from celery import Celery, shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from library_system.celery import app
from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        check_overdue_loans.s(), name="add every 10", sig=crontab(hour=24)
    )


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        _ = send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    try:
        overdue_loans = Loan.objects.filter(
            is_returned=False, due_date__gt=date.today()
        )
        mails_list = list(map(lambda item: item.member.user.email, overdue_loans))
        _ = send_mail(
            subject="Book Loan Overdue",
            message=f"Hello",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=mails_list,
            fail_silently=False,
        )
    except Exception as e:
        pass
        # TODO handle retry
