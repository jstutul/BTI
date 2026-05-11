from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_html_email(subject, to_email, html_content, text_content=""):
    if not to_email:
        return False
    from_email = f"{settings.ORG_NAME} <{settings.EMAIL_HOST_USER}>"
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content or "Please view this email in HTML format.",
        from_email=from_email,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    return True