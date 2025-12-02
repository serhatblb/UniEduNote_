from django.conf import settings
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email_via_sendgrid(subject: str, to_email: str, template_name: str, context: dict) -> None:
    """
    Genel amaçlı SendGrid mail gönderme fonksiyonu.

    - template_name: Django template yolu (örn: 'users/activation_email.html')
    - context: template için context dict
    """
    html_content = render_to_string(template_name, context)

    api_key = getattr(settings, "SENDGRID_API_KEY", None)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "no-reply@example.com"

    if not api_key:
        # PROD'da mutlaka ayarlı olmalı
        raise RuntimeError("SENDGRID_API_KEY ayarlı değil. Render ortamında env'e eklemelisin.")

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
    except Exception as exc:
        # Şimdilik basit log; istersen logging'e çeviririz
        print(f"SendGrid hata: {exc}")
        raise


def send_activation_email(user, activation_link: str) -> None:
    """Kullanıcıya aktivasyon maili gönderir."""
    subject = "UniEduNote Hesap Aktivasyonu"
    context = {
        "user": user,
        "activation_link": activation_link,
    }
    send_email_via_sendgrid(subject, user.email, "users/activation_email.html", context)
