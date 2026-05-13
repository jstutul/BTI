from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
import random
import string
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.db.models import Sum

class User(AbstractUser):
    @property
    def balance(self):
        credits = self.transactions.filter(transaction_type='credit').aggregate(total=Sum('amount'))['total'] or 0
        # Get total debits
        debits = self.transactions.filter(transaction_type='debit').aggregate(total=Sum('amount'))['total'] or 0
        return credits - debits
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    ADMIN = 'admin'
    INSTITUTION = 'institution'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (INSTITUTION, 'Institution'),
        (STUDENT, 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.png',
        blank=True,
        null=True
    )
    sign_image = models.ImageField(
        upload_to='sign_images/',
        default='sign_images/default.png',
        blank=True,
        null=True
    )
    is_active =models.BooleanField(default=True)
    create_at =models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    
class Session(models.Model):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    UPCOMING = 'upcoming'

    STATUS_CHOICES = [
        (UPCOMING, 'Upcoming'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    ]

    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    exam_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=UPCOMING
    )

    def __str__(self):
        return self.name

class Course(models.Model):
    DURATION_CHOICES = [
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
    ]
    CERTIFICATE_TYPE = [
        ('course', 'Course Certificate'),
        ('it_program', 'IT Program Certificate'),
        ('both', 'Both (Course + IT Program)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name  = models.CharField(max_length=500,blank=False)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    cert_type = models.CharField(max_length=20, choices=CERTIFICATE_TYPE)
    exam_fee =models.DecimalField(decimal_places=2,default=100.00,max_digits=10)
    description = models.CharField(max_length=5000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}'

    def get_custom_duration(self):
        choices_dict = dict(self.DURATION_CHOICES)
        return choices_dict.get(self.duration, "Unknown Duration")

    @property
    def expiry_date(self):
        if not self.created_at:
            return None

        if self.duration == '6_months':
            return self.created_at + relativedelta(months=6)

        elif self.duration == '1_year':
            return self.created_at + relativedelta(years=1)

        elif self.duration == '2_years':
            return self.created_at + relativedelta(years=2)

        elif self.duration == '3_years':
            return self.created_at + relativedelta(years=3)

        return self.created_at

class Institution(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='institution')
    name = models.CharField(blank=False,null=False,max_length=500)
    branch_code = models.CharField(max_length=50, unique=True)
    director = models.CharField(blank=False,null=False,max_length=200)
    mobile = models.CharField(blank=True,max_length=15)
    email=models.CharField(blank=True,max_length=100)
    district = models.TextField(blank=True)
    upazila = models.TextField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
        
    def student_count(self):
        return self.students.count()
    
    
class Student(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    NATIONALITY_CHOICES = [
        ('Bangladeshi', 'Bangladeshi'),
        ('Indian', 'Indian'),
        ('Pakistani', 'Pakistani'),
        ('Nepali', 'Nepali'),
        ('Sri Lankan', 'Sri Lankan'),
        ('Other', 'Other'),
    ]
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='student')
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='students'
    )
    courses = models.ForeignKey(Course, related_name='students', blank=True,on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=30, unique=True)
    roll_no =  models.CharField(max_length=30)
    reg_book_no =  models.CharField(max_length=30)
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='students'
    )
    full_name = models.CharField(max_length=150)
    father_name =models.CharField(max_length=150)
    mother_name =models.CharField(max_length=150)
    dob =models.DateField(blank=False)
    email =models.CharField(blank=False,max_length=200)
    gender = models.CharField(max_length=20,blank=True,choices=GENDER_CHOICES)
    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
        blank=True,
        null=True
    )
    mobile = models.CharField(blank=True,null=True,max_length=30)
    nid_no = models.CharField(blank=True,null=True,max_length=30)
    religion = models.CharField(blank=True,null=True,max_length=30)
    nationality = models.CharField(
        max_length=50,
        choices=NATIONALITY_CHOICES,
        blank=True,
        null=True
    )
    district = models.CharField(blank=True,null=True,max_length=300)
    thana = models.CharField(blank=True,null=True,max_length=300)
    present_address = models.CharField(blank=True,null=True,max_length=300)
    permanent_address = models.CharField(blank=True,null=True,max_length=300)
    education = models.CharField(blank=True,null=True,max_length=300)
    admissionDate = models.DateField(blank=True,null=True)
    create_at = models.DateField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    def get_full_name_camel_case(self):
        if self.full_name:
            return "".join(word.capitalize() for word in self.full_name.split())
        return ""
    
    
    
class BalanceTransaction(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'
    TRANSACTION_TYPES = [
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.transaction_type} - {self.amount}'
    
    


class Result(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='results')

    written_mark = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    practical_mark = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    viva_mark = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    total_mark = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False)
    grade = models.CharField(max_length=5, blank=True, editable=False)

    exam_date = models.DateField()
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course', 'session'],
                name='unique_student_course_session_result'
            )
        ]

    def calculate_grade(self, total):

        if total >= 80:
            return "A+"
        elif total >= 75:
            return "A"
        elif total >= 70:
            return "A-"
        elif total >= 65:
            return "B+"
        elif total >= 60:
            return "B"
        elif total >= 55:
            return "B-"
        elif total >= 50:
            return "C+"
        elif total >= 45:
            return "C"
        elif total >= 40:
            return "D"
        else:
            return "F"
    
    def get_grade_point(self):
        total = self.total_mark
        
        if total >= 80:
            return 4.00
        elif total >= 75:
            return 3.75
        elif total >= 70:
            return 3.50
        elif total >= 65:
            return 3.25
        elif total >= 60:            
            return 3.00
        elif total >= 55:
            return 2.75
        elif total >= 50:
            return 2.50
        elif total >= 45:
            return 2.25
        elif total >= 40:
            return 2.00
        else:
            return 0.00

    def is_passed(self):
        return self.grade != 'F'


    def save(self, *args, **kwargs):

        total = (
            (self.written_mark or 0) +
            (self.practical_mark or 0) +
            (self.viva_mark or 0)
        )
        if total > 100:
            raise ValueError("Total mark cannot exceed 100")

        self.total_mark = total
        self.grade = self.calculate_grade(total)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}"


class Certificate(models.Model):
    result = models.OneToOneField(
        'Result',
        on_delete=models.CASCADE,
        related_name='certificate'
    )

    cert_id = models.CharField(max_length=30, unique=True, editable=False)
    serial_no = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(
        upload_to='qr_images/',
        default='qr_images/default.png',
        blank=True,
        null=True
    )

  

    def save(self, *args, **kwargs):
        if self.result.grade == 'F':
            raise ValueError("Cannot generate certificate for failed student")

        if not self.cert_id:
            self.cert_id = f"BTI-CERT-{uuid.uuid4().hex[:10].upper()}"
            
        if not self.serial_no:
            self.serial_no = str(random.randint(100000, 999999))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cert_id} - {self.result.student.full_name}"



class PaymentDeposit(models.Model):
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_deposits")

    payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    trx_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    base_amount = models.DecimalField(max_digits=12, decimal_places=2)
    extra_charge = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    gateway = models.CharField(max_length=30, default="bkash")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    raw_create_response = models.JSONField(blank=True, null=True)
    raw_execute_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.gateway} - {self.status} - {self.base_amount}"