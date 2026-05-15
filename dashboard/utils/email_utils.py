# from django.core.mail import EmailMultiAlternatives
# from django.conf import settings
import resend
from django.conf import settings
resend.api_key = "re_MH1cvMwS_1bdP4Cb3rqaePhFgAyuPjJ7Q"
def send_html_email(subject, to_email, html_content, text_content=""):
    if not to_email:
        return False
    
    try:
        params: resend.Emails.SendParams = {
            "from": f"{settings.ORG_NAME} <support@bti.edu.bd>",
            "to": [to_email],
            "subject": subject,
            "html": html_content,
            "text": text_content or "Please view this email in HTML format.",
        }

        response = resend.Emails.send(params)
        return True

    except Exception as e:
        import logging
        logger = logging.getLogger('dashboard')
        logger.error(f"Resend email failed: {e}")
        return False
# def send_html_email(subject, to_email, html_content, text_content=""):
#     if not to_email:
#         return False
#     from_email = f"{settings.ORG_NAME} <{settings.EMAIL_HOST_USER}>"
#     email = EmailMultiAlternatives(
#         subject=subject,
#         body=text_content or "Please view this email in HTML format.",
#         from_email=from_email,
#         to=[to_email],
#     )

#     email.attach_alternative(html_content, "text/html")
#     email.send()

#     return True