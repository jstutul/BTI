from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from accounts.models import *
from django.db.models import Q
from django.http import JsonResponse
from accounts.forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib import messages

def courses_view(request):
    courses = Course.objects.filter(is_active=True)
    return render(request,'courses.html',{"courses":courses})

def trainning_center(request):
    training_centers = Institution.objects.filter(is_active=True)

    centers_data = []
    for tc in training_centers:
        courses = Course.objects.filter(
            students__institution=tc
        ).distinct()
        course_names = [c.name for c in courses]

        centers_data.append({
            'name': tc.name,
            'district': tc.district,
            'upazila': tc.upazila,
            'mobile': tc.mobile,
            'reg_no': tc.branch_code,
            'approved_date': getattr(tc, 'approved_date', None),
            'courses': course_names
        })

    return render(request,'center.html',{'training_centers': centers_data})

def trems_condition(request):
    return render(request,'trems.html')

def privacy_view(request):
    return render(request,'privacy.html')

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your message has been saved successfully. We’ll get back to you soon.")
            return redirect('contact_us')
    else:
        form = ContactForm()

    return render(request, "contact_us.html", {"form": form})

def home(request):

    total_students = Student.objects.count()
    total_centers = Institution.objects.count()
    total_institutes = Institution.objects.filter(is_active=True).count()
    total_courses = Course.objects.count()
    training_centers = Institution.objects.filter(is_active=True)

    centers_data = []
    for tc in training_centers:
        courses = Course.objects.filter(
            students__institution=tc
        ).distinct()
        course_names = [c.name for c in courses]

        centers_data.append({
            'name': tc.name,
            'district': tc.district,
            'upazila': tc.upazila,
            'mobile': tc.mobile,
            'reg_no': tc.branch_code,
            'approved_date': getattr(tc, 'approved_date', None),
            'courses': course_names
        })

    context = {
        "total_students": total_students,
        "total_centers": total_centers,
        "total_institutes": total_institutes,
        "total_courses": total_courses,
        "courses":Course.objects.filter(is_active=True),
        "institution":training_centers,
        'training_centers': centers_data
    }

    return render(request, 'index.html', context)


def verify_certificate(request):

    cert_id = request.GET.get("cert_id", "").strip()
    result = None
    error = None

    if cert_id:
        cert = Certificate.objects.select_related(
            "result__student",
            "result__student__profile",
            "result__student__institution",
            "result__course",
            "result__session"
        ).filter(
            Q(cert_id__iexact=cert_id) |
            Q(result__student__reg_no__iexact=cert_id) |
            Q(result__student__roll_no__iexact=cert_id)
        ).first()

        if not cert:
            error = "Certificate not found"
        else:
            result = cert

    return render(request, "verify.html", {
        "cert": result,
        "error": error,
        "cert_id": cert_id
    })


def id_card(request, pk):

    cert = Certificate.objects.select_related(
        'result__student__institution',
        'result__student__profile',
        'result__course',
        'result__session'
    ).filter(id=pk).first()

    # ❌ CASE 1: Certificate not found
    if not cert:
        return JsonResponse({
            "status": "error",
            "message": "Certificate not found / not generated"
        }, status=404)

    # 🔒 Institution restriction
    if request.user.profile.role == "institution":
        if cert.result.student.institution != request.user.profile.institution:
            return JsonResponse({
                "status": "error",
                "message": "Not allowed"
            }, status=403)

    # ✅ Generate HTML
    html = render_to_string("verify/idcard.html", {
        "cert": cert,
        "result": cert.result,
        "student": cert.result.student,
        "course": cert.result.course,
        "session": cert.result.session,
        "institution": cert.result.student.institution,
    })

    return JsonResponse({
        "status": "success",
        "html": html
    })



def register_card(request, pk):

    cert = Certificate.objects.select_related(
        'result__student__institution',
        'result__student__profile',
        'result__course',
        'result__session'
    ).filter(id=pk).first()

    # ❌ CASE 1: Certificate not found
    if not cert:
        return JsonResponse({
            "status": "error",
            "message": "Certificate not found / not generated"
        }, status=404)
    chairman =get_object_or_404(Chairman,id=1)
    html = render_to_string("verify/register.html", {
        "cert": cert,
        "result": cert.result,
        "student": cert.result.student,
        "course": cert.result.course,
        "session": cert.result.session,
        "institution": cert.result.student.institution,
        "chairman":chairman
    })
    return JsonResponse({
        "status": "success",
        "html": html
    })



def id_card(request, pk):

    cert = Certificate.objects.select_related(
        'result__student__institution',
        'result__student__profile',
        'result__course',
        'result__session'
    ).filter(id=pk).first()

    # ❌ CASE 1: Certificate not found
    if not cert:
        return JsonResponse({
            "status": "error",
            "message": "Certificate not found / not generated"
        }, status=404)

    chairman =get_object_or_404(Chairman,id=1)
    html = render_to_string("verify/idcard.html", {
        "cert": cert,
        "result": cert.result,
        "student": cert.result.student,
        "course": cert.result.course,
        "session": cert.result.session,
        "institution": cert.result.student.institution,
        "chairman":chairman
    })

    return JsonResponse({
        "status": "success",
        "html": html
    })



def admit_card(request, pk):

    cert = Certificate.objects.select_related(
        'result__student__institution',
        'result__student__profile',
        'result__course',
        'result__session'
    ).filter(id=pk).first()

    # ❌ CASE 1: Certificate not found
    if not cert:
        return JsonResponse({
            "status": "error",
            "message": "Certificate not found / not generated"
        }, status=404)

    chairman =get_object_or_404(Chairman,id=1)

    html = render_to_string("verify/admit.html", {
        "cert": cert,
        "result": cert.result,
        "student": cert.result.student,
        "course": cert.result.course,
        "session": cert.result.session,
        "institution": cert.result.student.institution,
        "chairman":chairman
    })

    return JsonResponse({
        "status": "success",
        "html": html
    })