from django.shortcuts import render,redirect,get_object_or_404
from accounts.decorators import role_required
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Course, Session,Institution,Profile,Student,Result,Certificate,PaymentDeposit,BalanceTransaction,Chairman
from dashboard.forms import CourseForm,SessionForm,InstitutionForm,StudentForm,StudentEditForm,ResultForm,CertificateForm,CertificateEditForm,ChairmanForm
from django.contrib import messages
from django.core.paginator import Paginator
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from dashboard.utils.email_utils import send_html_email
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.templatetags.static import static
from .bkash_service import create_payment, execute_payment
from decimal import Decimal
from django.db import transaction,DatabaseError
from django.db.models import Sum
from django.urls import reverse
import qrcode
import os
from io import BytesIO
from django.core.files.base import ContentFile

User = get_user_model()


@role_required(['admin'])
def admin_dashboard(request):
    total_institutions = Institution.objects.filter(is_active=True).count()
    total_students = Student.objects.count()
    total_certificates = Certificate.objects.count()
    total_results_published = Result.objects.count()
    total_results_pending = Result.objects.filter(
        is_published=False
    ).count()
    # fee calculations
    fee_per_student = settings.STUDENT_FEE
    total_fee_collected = total_results_published * fee_per_student
    total_fee_pending = total_results_pending * fee_per_student
    # latest institutions
    latest_institutions = Institution.objects.filter(
        is_active=True
    ).order_by('-id')[:5]
    # latest payments
    latest_payments =BalanceTransaction.objects.select_related('user')[:5]
    context = {
        'total_institutions': total_institutions,
        'total_students': total_students,
        'total_certificates': total_certificates,

        'total_fee_collected': total_fee_collected,
        'total_fee_pending': total_fee_pending,

        'latest_institutions': latest_institutions,
        'latest_payments': latest_payments,
    }
    
    return render(request, 'dashboard/admin.html',context)

@role_required(['admin'])
def course_list(request):
    courses = Course.objects.all()
    sessions = Session.objects.all()
    tab = request.GET.get('tab', 'courses') 
    return render(request, 'dashboard/course/list.html', {'courses': courses,'sessions':sessions, 'tab': tab})


@role_required(['admin'])
def course_add(request):
    form = CourseForm()
    courses = Course.objects.all()

    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, "Course added successfully!")
            return redirect('dashboard:course_list')

    return render(request, 'dashboard/course/add.html', {
        'course_form': form,'courses': courses
    })

@role_required(['admin'])
def course_edit(request, pk):
    course = Course.objects.get(pk=pk)

    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, "Course updated successfully!")
            return redirect('dashboard:course_list')

    return render(request, 'dashboard/course/edit.html', {
        'course_form': form,
        'course': course
    })


@role_required(['admin'])
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course added successfully!")
    return redirect('dashboard:course_list')


@role_required(['admin'])
def session_add(request):
    form = SessionForm()

    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Session added successfully!")
            return redirect('/dashboard/admin/courses/?tab=sessions')

    return render(request, 'dashboard/session/add.html', {
        'form': form
    })


@role_required(['admin'])
def session_edit(request, pk):
    session = get_object_or_404(Session, pk=pk)

    form = SessionForm(instance=session)

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)

        if form.is_valid():
            form.save()
            messages.success(request, "Session updated successfully!")
            return redirect('/dashboard/admin/courses/?tab=sessions')

    return render(request, 'dashboard/session/edit.html', {
        'form': form
    })

@role_required(['admin'])
def session_delete(request, pk):
    session = get_object_or_404(Session, pk=pk)
    session.delete()
    messages.success(request, "Session deleted successfully!")
    return redirect('/dashboard/admin/courses/?tab=sessions')


@role_required(['admin'])
def institution_list(request):
    institutions = Institution.objects.all()
    total = institutions.count()
    active = institutions.filter(profile__is_active=True).count()
    inactive = institutions.filter(profile__is_active=False).count()
    paginator = Paginator(institutions, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/institution/list.html', {
        'institutions': page_obj,
        'total': total,
        'active': active,
        'inactive': inactive,
    })

def generate_unique_branch_code():
    while True:
        number = random.randint(1000000000, 9999999999)  # 10 digits
        code = f"BR-{number}"

        if not Institution.objects.filter(branch_code=code).exists():
            return code


@role_required(['admin'])
def institution_add(request):
    form = InstitutionForm()

    if request.method == 'POST':
        form = InstitutionForm(request.POST)

        if form.is_valid():
            branch_code = generate_unique_branch_code()
            user = User.objects.create_user(
                username=branch_code,
                password=branch_code,
                is_staff=True
            )
            profile = user.profile

            # # 4. create institution safely
            institution = form.save(commit=False)
            institution.profile = profile
            institution.branch_code = branch_code
            institution.save()

            name = form.cleaned_data.get("name")
            director = form.cleaned_data.get("director")
            email = form.cleaned_data.get("email")

            html_content = render_to_string("emails/institution_created.html", {
                "director":director,
                "username": branch_code,
                "password": branch_code,
                "name": name,
            })

            send_html_email(
                subject="Institution Account Created",
                to_email=email,
                html_content=html_content,
            )

            messages.success(
                request,
                f"Institution created! Username: {branch_code}, Password: {branch_code}"
            )
            return redirect('dashboard:institution_list')

        else:
            print(form.errors)
            messages.error(request, "Form validation failed!")

    return render(request, 'dashboard/institution/add.html', {
        'form': form
    })

@role_required(['admin'])
def institution_edit(request, pk):
    institution = get_object_or_404(Institution, pk=pk)
    form = InstitutionForm(instance=institution)

    if request.method == 'POST':
        form = InstitutionForm(request.POST, instance=institution)

        if form.is_valid():
            institution = form.save(commit=False)

            # 🔥 OPTIONAL: sync with user/profile
            user = institution.profile.user

            # Example updates (adjust as needed)
            user.email = form.cleaned_data.get("email")
            user.save()

            institution.save()

            messages.success(request, "Institution updated successfully!")
            return redirect('dashboard:institution_list')

    return render(request, 'dashboard/institution/edit.html', {
        'form': form,
        'institution': institution
    })

@role_required(['admin'])
def institution_delete(request, pk):
    institution = get_object_or_404(Institution, pk=pk)
    user = institution.profile.user  # 🔥 get user

    user.delete()  # ✅ this deletes profile + institution (cascade)

    messages.success(request, "Institution deleted successfully!")
    return redirect('dashboard:institution_list')

@role_required(['admin', 'institution'])
def student_list(request):
    students = Student.objects.select_related(
        'institution', 'session', 'courses', 'profile'
    )

    if request.user.profile.role == 'institution':
        students = students.filter(
            institution=request.user.profile.institution
        )

    q = request.GET.get('q')
    if q:
        students = students.filter(
            Q(full_name__icontains=q) |
            Q(reg_no__icontains=q) |
            Q(father_name__icontains=q) |
            Q(mobile__icontains=q)
        )
    inst = request.GET.get('inst')
    print(inst)
    if inst:
        students = students.filter(institution__id=int(inst))

    sess = request.GET.get('sess')
    if sess:
        students = students.filter(session_id=sess)


    stat = request.GET.get('stat')
    if stat == 'active':
        students = students.filter(is_active=True)
    elif stat == 'inactive':
        students = students.filter(is_active=False)

    # counts (before pagination)
    total = students.count()
    active = students.filter(is_active=True).count()
    inactive = students.filter(is_active=False).count()

    # 🔥 PAGINATION
    paginator = Paginator(students, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.profile.role == 'admin':
        institution = Institution.objects.filter(is_active=True)
    else:
        institution = Institution.objects.filter(
            id=request.user.profile.institution.id
        )
    session = Session.objects.filter(status='active')

    return render(request, 'dashboard/student/list.html', {
        'page_obj': page_obj,
        'students': page_obj.object_list,  # optional shortcut
        'total': total,
        'active': active,
        'inactive': inactive,
        'institutions': institution,
        'sessions': session,
        'q': q,
        'inst': inst,
        'sess': sess,
        'stat': stat,
    })

def get_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.user.profile.role == 'institution':
        if student.institution != request.user.profile.institution:
            return None  # or raise PermissionDenied

    return student


@role_required(['admin', 'institution'])
def student_toggle(request, pk):

    student = get_object_or_404(Student, pk=pk)

    # institution restriction
    if request.user.profile.role == 'institution':
        if student.institution != request.user.profile.institution:
            return HttpResponse("Unauthorized")

    student.is_active = not student.is_active
    student.save()

    return redirect('dashboard:student_list')


@role_required(['admin', 'institution'])
def assign_course(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    # 🔥 SECURITY RULE
    if request.user.profile.role == 'institution':
        if student.institution != request.user.profile.institution:
            return HttpResponse("Unauthorized")

    if request.method == 'POST':
        course_ids = request.POST.getlist('courses')

        # 🔥 OPTIONAL EXTRA SECURITY (institution courses only)
        if request.user.profile.role == 'institution':
            course_ids = Course.objects.filter(
                id__in=course_ids,
                user=request.user
            ).values_list('id', flat=True)

        student.courses.set(course_ids)

        messages.success(request, "Courses assigned successfully!")
        return redirect('dashboard:student_list')

    courses = Course.objects.all()

    return render(request, 'dashboard/student/assign.html', {
        'student': student,
        'courses': courses
    })

def generate_reg_no():
    # 1. Get last student reg_no
    student_last = Student.objects.exclude(reg_no__isnull=True)\
        .exclude(reg_no='')\
        .order_by('-id').first()

    # 2. Get last user username (if used as reg system)
    user_last = User.objects.exclude(username__isnull=True)\
        .exclude(username='')\
        .order_by('-id').first()

    numbers = []

    # extract from student
    if student_last and student_last.reg_no.startswith("REG-"):
        try:
            numbers.append(int(student_last.reg_no.split('-')[1]))
        except:
            pass

    # extract from user (ONLY if format matches REG-XXXXXX)
    if user_last and user_last.username.startswith("REG-"):
        try:
            numbers.append(int(user_last.username.split('-')[1]))
        except:
            pass

    # if nothing exists
    if not numbers:
        return "REG-000001"

    return f"REG-{max(numbers) + 1:06d}"

def generate_roll_no():
    last_student = Student.objects.order_by('-id').first()

    if not last_student or not last_student.roll_no:
        return "RL-000001"

    try:
        last_number = int(last_student.roll_no.split('-')[1])
    except:
        last_number = 0

    new_number = last_number + 1
    return f"RL-{new_number:06d}"

@role_required(['admin', 'institution'])
def student_add(request):
    user = request.user
    form = StudentForm()
    # Institution restriction
    if user.profile.role == 'institution':
        form.fields['institution'].queryset = Institution.objects.filter(
            id=user.profile.institution.id
        )
        form.fields['institution'].initial = user.profile.institution
        form.fields['institution'].disabled = True

    if request.method == 'POST':
        form = StudentForm(request.POST or None, request.FILES or None,user=request.user)

        reg_no = generate_reg_no()
        roll_no = generate_roll_no()

        if form.is_valid():
            student = form.save(commit=False)

            # create login user
            user_obj = User.objects.create_user(
                username=reg_no,
                password=roll_no
            )

            profile = user_obj.profile
            image = form.cleaned_data.get('profile_image')
            if image:
                profile.profile_image = image
                profile.save()
                

            student.profile = profile
            student.reg_no = reg_no
            student.roll_no = roll_no

            # SAFE institution handling
            if request.user.profile.role == 'institution':
                student.institution = request.user.profile.institution
            else:
                student.institution = form.cleaned_data.get("institution")

            student.save()

            # IMPORTANT for ManyToMany
            form.save()

            # SAFE course handling
            courses = form.cleaned_data.get("courses")

            full_name = form.cleaned_data.get("full_name")

            institution = student.institution
            institution_name = institution.name if institution else "N/A"

            email = form.cleaned_data.get("email")

            html_content = render_to_string("emails/student_created.html", {
                "password": roll_no,
                "username": reg_no,
                "reg_no": reg_no,
                "roll_no": roll_no,
                "full_name": full_name,
                "institution": institution_name,
                "courses": courses,
            })

            send_html_email(
                subject="Student Account Created",
                to_email=email,
                html_content=html_content,
            )

            messages.success(
                request,
                f"Student created! Username: {reg_no}, Password: {roll_no}"
            )
            return redirect('dashboard:student_list')

    return render(request, 'dashboard/student/add.html', {
        'form': form
    })



@role_required(['admin', 'institution'])
def student_edit(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.user.profile.role == 'institution':
        
        if student.institution != request.user.profile.institution:
            messages.error(request, "You cannot edit this student.")
            return redirect('dashboard:student_list')
        else:
            student.institution = request.user.profile.institution

    form = StudentEditForm(
        request.POST or None,
        request.FILES or None,
        instance=student,
        user=request.user
    )

    if form.is_valid():
        student = form.save(commit=False)

        # ensure institution stays locked for institution users
        if request.user.profile.role == 'institution':
            student.institution = request.user.profile.institution

        student.save()
        form.save_m2m() 


        profile_image = form.cleaned_data.get('profile_image')
        if profile_image:
            student.profile.profile_image = profile_image
            student.profile.save()


        messages.success(request, "Student updated successfully!")
        return redirect('dashboard:student_list')
    else:
        print(11)
    return render(request, 'dashboard/student/edit.html', {
        'form': form,
        'student': student
    })

@role_required(['admin', 'institution'])
def result_list(request):
    user = request.user
    q = request.GET.get('q', '')
    inst = request.GET.get('inst', '')
    sess = request.GET.get('sess', '')
    cors = request.GET.get('course', '')

    results = Result.objects.select_related(
        'student', 'student__institution', 'course', 'session'
    )

    if user.profile.role == 'institution':
        results = results.filter(student__institution=user.profile.institution)

    if q:
        results = results.filter(
            student__full_name__icontains=q
        ) | results.filter(
            student__reg_no__icontains=q
        )

    if user.profile.role == 'admin' and inst:
        results = results.filter(student__institution_id=inst)

    if sess:
        results = results.filter(session_id=sess)

    if cors:
        results = results.filter(course_id=cors)

    paginator = Paginator(results, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    institutions = Institution.objects.filter(is_active=True)
    sessions = Session.objects.filter(status='active')
    courses = Course.objects.filter(is_active=True)

    return render(request, 'dashboard/result/list.html', {
        'page_obj': page_obj,
        'institutions': institutions,
        'sessions': sessions,
        'q': q,
        'inst': inst,
        'sess': sess,
        'courses':courses
    })

@role_required(['admin', 'institution'])
def result_add(request):
    user = request.user
    form = ResultForm(request.POST or None, user=user)

    if user.profile.role == 'institution':
        form.fields['student'].queryset = Student.objects.filter(
            institution=user.profile.institution
        )

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                # 1. Create result object but don't save to DB yet
                result = form.save(commit=False)

                # 2. Safety Check: Does this student belong to this institution?
                if user.profile.role == 'institution':
                    if result.student.institution != user.profile.institution:
                        messages.error(request, "Invalid student selection!")
                        return redirect('dashboard:result_add')

                # 3. Balance Check (Using the calculated balance)
                # Note: 'user.balance' works if you added the @property to your User model
                charge = Decimal(settings.STUDENT_FEE)
                if user.balance < charge:
                    messages.warning(request, 'Insufficient balance.')
                    return redirect('dashboard:result_add')

                # 4. Perform the operations
                result.save() # Save the result to DB
                
                BalanceTransaction.objects.create(
                    user=user,
                    transaction_type='debit',
                    amount=charge,
                    note=f"Result published for student: {result.student.full_name}"
                )

                messages.success(request, "Result added successfully!")
                return redirect('dashboard:result_list')

        except Exception as e:
            # This will now help you see the REAL error in your console/terminal
            print(f"Error: {e}") 
            messages.error(request, "An unexpected error occurred. Please try again.")
                
    return render(request, 'dashboard/result/add.html', {'form': form})
    

@role_required(['admin', 'institution'])
def result_edit(request, pk):

    result = get_object_or_404(Result, pk=pk)

    if request.user.profile.role == 'institution':
        if result.student.institution != request.user.profile.institution:
            messages.error(request, "Not allowed")
            return redirect('dashboard:result_list')

    form = ResultForm(request.POST or None, instance=result,user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Result updated successfully!")
        return redirect('dashboard:result_list')

    return render(request, 'dashboard/result/edit.html', {
        'form': form,
        'result': result
    })



def generate_qr_code(cert_id, url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Black QR, transparent background
    img = qr.make_image(fill_color="black", back_color="transparent")

    # Save to in-memory buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f"qr_{cert_id}.png"
    return ContentFile(buffer.read(), name=filename)


@role_required(['admin', 'institution'])
def certificate_generate(request):

    if request.method == "POST":
        form = CertificateForm(request.POST, user=request.user)

        if form.is_valid():
            cert = form.save(commit=False)

            result = cert.result

            # 🔥 BLOCK: must pass check (VERY IMPORTANT)
            if result.grade not in ['A+', 'A', 'A-', 'B+', 'B-', 'C+', 'C', 'D']:
                form.add_error('result', "Student has not passed. Certificate cannot be generated.")
                return render(request, 'dashboard/certificate/generate.html', {'form': form})

            # institution restriction
            if request.user.profile.role == 'institution':
                if result.student.institution != request.user.profile.institution:
                    form.add_error('result', "Not allowed for this student.")
                    return render(request, 'dashboard/certificate/generate.html', {'form': form})

            # duplicate check
            if Certificate.objects.filter(result=result).exists():
                form.add_error('result', "Certificate already exists for this student.")
                return render(request, 'dashboard/certificate/generate.html', {'form': form})

            cert.cert_id = "BTI-CERT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            qr_url = f"https://bti.edu.bd/verify/?cert_id={cert.cert_id}"
            cert.qr_code = generate_qr_code(cert.cert_id, qr_url)
            cert.save()

            messages.success(request, "Certificate generated successfully!")
            return redirect('dashboard:certificate_list')

    else:
        form = CertificateForm(user=request.user)

    return render(request, 'dashboard/certificate/generate.html', {
        'form': form
    })

@role_required(['admin', 'institution'])
def certificate_edit(request, pk):

    cert = get_object_or_404(Certificate, pk=pk)

    # institution restriction
    if request.user.profile.role == 'institution':
        if cert.result.student.institution != request.user.profile.institution:
            messages.error(request, "Not allowed")
            return redirect('dashboard:certificate_list')

    if request.method == "POST":
        form = CertificateEditForm(request.POST, instance=cert)

        if form.is_valid():
            form.save()
            messages.success(request, "Certificate updated successfully!")
            return redirect('dashboard:certificate_list')

    else:
        form = CertificateEditForm(instance=cert)

    return render(request, 'dashboard/certificate/edit.html', {
        'form': form,
        'cert': cert
    })
@role_required(['admin', 'institution'])
def certificate_delete(request, pk):

    cert = get_object_or_404(Certificate, pk=pk)

    if request.user.profile.role == 'institution':
        if cert.result.student.institution != request.user.profile.institution:
            messages.error(request, "Not allowed")
            return redirect('dashboard:certificate_list')

    cert.delete()
    messages.success(request, "Deleted successfully!")
    return redirect('dashboard:certificate_list')

@role_required(['admin', 'institution'])
def certificate_list(request):

    user = request.user
    role = user.profile.role

    # filters
    q = request.GET.get('q', '').strip()
    inst = request.GET.get('inst', '').strip()
    sess = request.GET.get('sess', '').strip()
    course = request.GET.get('course', '').strip()

    # MAIN QUERYSET (IMPORTANT)
    certs = Certificate.objects.select_related(
        'result__student__institution',
        'result__student__profile',
        'result__course',
        'result__session'
    )

    # 🔒 Institution restriction
    if role == 'institution':
        certs = certs.filter(
            result__student__institution=user.profile.institution
        )

    # 🔍 Search
    if q:
        certs = certs.filter(
            Q(result__student__full_name__icontains=q) |
            Q(result__student__reg_no__icontains=q)
        )

    # 🏫 Admin institution filter
    if role == 'admin' and inst:
        certs = certs.filter(
            result__student__institution_id=inst
        )

    # 📅 Session filter
    if sess:
        certs = certs.filter(
            result__session_id=sess
        )

    # 📚 Course filter
    if course:
        certs = certs.filter(
            result__course_id=course
        )

    # 📊 stats
    total_certificates = certs.count()

    total_passed = Result.objects.filter(
        grade__in=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']
    ).count()

    eligible = Result.objects.filter(
        grade__in=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']
    ).exclude(certificate__isnull=False)

    # 📄 pagination (IMPORTANT FIX)
    paginator = Paginator(certs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # dropdown data
    institutions = Institution.objects.filter(is_active=True)
    sessions = Session.objects.filter(status='active')
    courses = Course.objects.filter(is_active=True)

    return render(request, 'dashboard/certificate/list.html', {
        'page_obj': page_obj,

        'total_certificates': total_certificates,
        'total_passed': total_passed,
        'eligible': eligible,

        'institutions': institutions,
        'sessions': sessions,
        'courses': courses,

        'q': q,
        'inst': inst,
        'sess': sess,
        'course': course,
        'role': role,
    })


def certificate_html_api(request, pk):

    cert = get_object_or_404(
        Certificate.objects.select_related(
            'result__student__institution',
            'result__student__profile',
            'result__course',
            'result__session'
        ),
        id=pk
    )
    chairman =get_object_or_404(Chairman,id=1)
 
    if not cert.qr_code or cert.qr_code.name == 'qr_images/default.png':
        qr_url = f"https://bti.edu.bd/verify/?cert_id={cert.cert_id}"
        cert.qr_code = generate_qr_code(cert.cert_id, qr_url)
        cert.save(update_fields=['qr_code']) 

    # institution restriction
    if request.user.profile.role == "institution":
        if cert.result.student.institution != request.user.profile.institution:
            return JsonResponse({
                "error": "Not allowed"
            }, status=403)

    html = render_to_string(
        "dashboard/certificate/template.html",
        {
            "cert": cert,
            "result": cert.result,
            "student": cert.result.student,
            "course": cert.result.course,
            "session": cert.result.session,
            "institution": cert.result.student.institution,
            "profile": cert.result.student.institution.profile,
            "chairman":chairman
        }
    )

    return JsonResponse({
        "html": html
    })

@role_required(['institution'])
def institution_dashboard(request):
    user = request.user
    role = user.profile.role

    institution = request.user.profile.institution

    # 🎓 students (only this institution)
    total_students = Student.objects.filter(
        institution=institution
    ).count()

    # 📄 certificates
    total_certificates = Certificate.objects.filter(
        result__student__institution=institution
    ).count()

    # 📊 results
    total_results_published = Result.objects.filter(
        student__institution=institution,
        is_published=True
    ).count()

    total_results_pending = Result.objects.filter(
        student__institution=institution,
        is_published=False
    ).count()

    # 💰 fee logic
    fee_per_student = 300  # or settings.STUDENT_FEE

    total_fee_collected = total_results_published * fee_per_student
    total_fee_pending = total_results_pending * fee_per_student

    # 🏦 latest payments (institution only)
    latest_payments = BalanceTransaction.objects.filter(
        user__profile__institution=institution
    ).select_related('user')[:5]

    context = {
        'institution': institution,
        'total_students': total_students,
        'total_certificates': total_certificates,
        'total_results_published': total_results_published,
        'total_results_pending': total_results_pending,
        'total_fee_collected': total_fee_collected,
        'total_fee_pending': total_fee_pending,
        'latest_payments': latest_payments,
    }
    return render(request, 'dashboard/institution.html',context)


@role_required(['student'])
def student_dashboard(request):
    return render(request, 'dashboard/student.html')






# API 
def get_result_info(request, pk):

    result = get_object_or_404(
        Result.objects.select_related(
            'student', 'course', 'session', 'student__institution'
        ),
        id=pk
    )

    user = request.user
    role = user.profile.role

    if role == 'institution':
        if result.student.institution != user.profile.institution:
            return JsonResponse({
                'error': 'Not allowed for this institution'
            }, status=403)

    if result.grade not in ['A+', 'A', 'A-', 'B+', 'B','B-', 'C+', 'C', 'D']:
        return JsonResponse({
            'error': 'Student has not passed'
        }, status=400)

    # if hasattr(result, 'certificate'):
    #     return JsonResponse({
    #         'error': 'Certificate already generated'
    #     }, status=400)

    photo_url = ""
    if result.student.profile.profile_image:
        photo_url = result.student.profile.profile_image.url

    data = {
        'student': result.student.full_name,
        'institution': result.student.institution.name,
        'course': result.course.name,
        'session': result.session.name,

        'written': float(result.written_mark),
        'practical': float(result.practical_mark),
        'viva': float(result.viva_mark),
        'total': float(result.total_mark),
        'grade': result.grade,
        'exam_date': result.exam_date.strftime('%Y-%m-%d'),

        'photo': photo_url
    }

    return JsonResponse(data)
@role_required(['admin', 'institution'])
def deposit_page(request):
    user = request.user
    role = user.profile.role

    # Initialize base QuerySets
    pays = BalanceTransaction.objects.all()
    pending = Student.objects.filter(results__isnull=True)

    if role == 'institution':
        # Restrict data to only this institution
        institution = user.profile.institution
        pays = pays.filter(user=user)
        pending = pending.filter(institution=institution)
    
    # Finalize QuerySets
    pays = pays.order_by('-created_at')
    pending = pending.distinct()

    # Calculations
    total_paid = pays.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
    total_deposit = pays.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
    
    pending_count = pending.count()
    # Ensure STUDENT_FEE is a Decimal or float in settings
    charge = getattr(settings, 'STUDENT_FEE', 300)
    pending_amount = pending_count * Decimal(charge)

    context = {
        'pays': pays,
        'pending': pending,
        'total_paid': total_paid,
        'total_deposit': total_deposit,
        'pending_count': pending_count,
        'pending_amount': pending_amount,
    }
    return render(request, "dashboard/payments/deposit.html", context)

@role_required(['admin', 'institution'])
def bkash_pay(request):
    if request.method != "POST":
        return redirect("dashboard:deposit_page")

    amount = Decimal(request.POST.get("amount", "0"))

    if amount < settings.BKASH_MIN_DEPOSIT:
        messages.error(request, f"Minimum deposit amount is ৳{settings.BKASH_MIN_DEPOSIT}")
        return redirect("dashboard:deposit_page")

    extra_charge = (amount * settings.BKASH_EXTRA_CHARGE_PERCENT / Decimal("100")).quantize(Decimal("0.01"))
    payable_amount = amount + extra_charge

    deposit = PaymentDeposit.objects.create(
        user=request.user,
        base_amount=amount,
        extra_charge=extra_charge,
        paid_amount=payable_amount,
        status=PaymentDeposit.STATUS_PENDING,
    )

    data = create_payment(request, payable_amount)
  

    deposit.raw_create_response = data
    deposit.payment_id = data.get("paymentID")
    deposit.save(update_fields=["raw_create_response", "payment_id"])

    bkash_url = data.get("bkashURL")

    if not bkash_url:
        deposit.status = PaymentDeposit.STATUS_FAILED
        deposit.save(update_fields=["status"])
        messages.error(request, data.get("statusMessage", "bKash payment create failed"))
        return redirect("dashboard:deposit_page")

    request.session["payment_deposit_id"] = deposit.id
    return redirect(bkash_url)


@role_required(['admin', 'institution'])
def bkash_callback(request):
    status = request.GET.get("status")
    payment_id = request.GET.get("paymentID")
    deposit_id = request.session.get("payment_deposit_id")

    deposit = PaymentDeposit.objects.filter(
        id=deposit_id,
        user=request.user
    ).first()

    if not deposit:
        messages.error(request, "Payment record not found.")
        return redirect("dashboard:deposit_page")

    if status == "cancel":
        deposit.status = PaymentDeposit.STATUS_CANCELLED
        deposit.save(update_fields=["status"])
        messages.warning(request, "Payment cancelled.")
        return redirect("dashboard:deposit_page")

    if status == "failure":
        deposit.status = PaymentDeposit.STATUS_FAILED
        deposit.save(update_fields=["status"])
        messages.error(request, "Payment failed.")
        return redirect("dashboard:deposit_page")

    token = request.session.get("bkash_token")

    result = execute_payment(payment_id, token)

    deposit.raw_execute_response = result
    deposit.trx_id = result.get("trxID")
    deposit.save(update_fields=["raw_execute_response", "trx_id"])

    if result.get("statusCode") != "0000":
        deposit.status = PaymentDeposit.STATUS_FAILED
        deposit.save(update_fields=["status"])
        messages.error(request, result.get("statusMessage", "Payment failed."))
        return redirect("dashboard:deposit_page")

    if deposit.status == PaymentDeposit.STATUS_COMPLETED:
        messages.warning(request, "This payment already processed.")
        return redirect("dashboard:transactions")

    with transaction.atomic():
        user = request.user
        user.balance += deposit.base_amount
        user.save(update_fields=["balance"])

        BalanceTransaction.objects.create(
            user=user,
            transaction_type=BalanceTransaction.CREDIT,
            amount=deposit.base_amount,
            note=f"bKash deposit. PaymentID: {payment_id}. TrxID: {deposit.trx_id}. Paid: {deposit.paid_amount}. Charge: {deposit.extra_charge}",
        )

        deposit.status = PaymentDeposit.STATUS_COMPLETED
        deposit.save(update_fields=["status"])

    request.session.pop("payment_deposit_id", None)
    request.session.pop("bkash_token", None)

    messages.success(request, f"Deposit successful. ৳{deposit.base_amount} added.")
    return redirect("dashboard:transactions")
    

@role_required(['admin', 'institution'])
def transaction_list(request):
    transactions = BalanceTransaction.objects.filter(user=request.user)

    return render(request, "dashboard/payments/transactions.html", {
        "transactions": transactions
    })


@role_required(['admin'])
def chairman_settings(request):
    chairman, created = Chairman.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = ChairmanForm(request.POST, request.FILES, instance=chairman)
        if form.is_valid():
            form.save()
            messages.success(request, f"Chairman Signature update successful.")
            return redirect('dashboard:chairman_settings')
    else:
        form = ChairmanForm(instance=chairman)

    return render(request, 'dashboard/chairman_form.html', {
        'form': form,
        'chairman': chairman
    })