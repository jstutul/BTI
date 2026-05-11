from django.conf import settings

def global_context(request):
    context = {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'My Website'),
        'REG_NO': getattr(settings, 'REG_NO', ''),
        'ADDRESS': getattr(settings, 'ADDRESS', ''),
        'EMAIL': getattr(settings, 'EMAIL', ''),
        'PHONE': getattr(settings, 'PHONE', ''),
        'ADMISSION_FEE': getattr(settings, 'ADMISSION_FEE', ''),
        'FAVICON': getattr(settings, 'FAVICON', ''),
        'LOGO': getattr(settings, 'LOGO', ''),
    }

    if request.user.is_authenticated:
        context.update({
            'role': getattr(request.user.profile, 'role', None),
            'current_user': request.user,
        })
    return context