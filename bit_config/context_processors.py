from accounts.models import Course

def top_students_footer(request):
    # Use = instead of == inside filter()
    courses = Course.objects.filter(is_active=True)[:5] 
    return {
        'courses': courses
    }