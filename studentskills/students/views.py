from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Sum, Count
from django.utils import timezone
from datetime import date
from .models import *

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_student(request):
    if request.method == 'POST':
        StudentRegistration.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            mobile_number=request.POST.get('mobile_number'),
            email=request.POST.get('email'),
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            qualification=request.POST.get('qualification'),
            parent_name=request.POST.get('parent_name',''),
            parent_mobile=request.POST.get('parent_mobile',''),
            address=request.POST.get('address',''),
        )
        messages.success(request, 'Registration submitted! We will contact you soon.')
        return redirect('register_student')
    return render(request, 'students/register.html')

def parent_portal(request):
    student = None
    search = request.GET.get('search', '')
    if search:
        student = Student.objects.filter(first_name__icontains=search).first() or \
                  Student.objects.filter(last_name__icontains=search).first() or \
                  Student.objects.filter(roll_number__iexact=search).first()
    return render(request, 'students/parent_portal.html', {'student': student, 'search': search})

def feedback_view(request):
    if request.method == 'POST':
        Feedback.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            role=request.POST.get('role'),
            feedback_type=request.POST.get('feedback_type'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Thank you! Your feedback has been submitted.')
        return redirect('feedback')
    return render(request, 'students/feedback.html')

def is_admin(user): return user.is_superuser or user.groups.filter(name='Admin').exists()
def is_teacher(user): return user.groups.filter(name='Teacher').exists() or is_admin(user)

@login_required(login_url='login')
def home(request):
    query_name = request.GET.get('name', '')
    query_mobile = request.GET.get('mobile', '')
    students = Student.objects.all().order_by('-created_at')
    if query_name:
        from django.db.models import Q
        students = students.filter(Q(first_name__icontains=query_name) | Q(last_name__icontains=query_name))
    if query_mobile:
        students = students.filter(mobile_number__icontains=query_mobile)
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(students, per_page)
    page_obj = paginator.get_page(request.GET.get('page'))
    events = Event.objects.filter(event_date__gte=date.today()).order_by('event_date')[:5]
    notifications = Notification.objects.order_by('-created_at')[:5]
    holidays = Holiday.objects.filter(date__gte=date.today()).order_by('date')[:5]
    best_students = BestStudent.objects.order_by('-year')[:3]
    return render(request, 'students/home.html', {
        'page_obj': page_obj, 'query_name': query_name, 'query_mobile': query_mobile,
        'per_page': per_page, 'total': students.count(),
        'events': events, 'notifications': notifications,
        'holidays': holidays, 'best_students': best_students,
        'is_admin': is_admin(request.user), 'is_teacher': is_teacher(request.user),
    })

@login_required(login_url='login')
def create_student(request):
    if not (is_admin(request.user) or is_teacher(request.user)):
        messages.error(request, 'Access denied.'); return redirect('home')
    subjects = Subject.objects.all()
    if request.method == 'POST':
        student = Student(
            first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'),
            mobile_number=request.POST.get('mobile_number'), email=request.POST.get('email'),
            gender=request.POST.get('gender'), dob=request.POST.get('dob'),
            qualification=request.POST.get('qualification'),
            skill_java='skill_java' in request.POST, skill_dotnet='skill_dotnet' in request.POST,
            skill_python='skill_python' in request.POST, skill_database='skill_database' in request.POST,
            description=request.POST.get('description',''),
            parent_name=request.POST.get('parent_name',''), parent_mobile=request.POST.get('parent_mobile',''),
            parent_email=request.POST.get('parent_email',''), address=request.POST.get('address',''),
        )
        if request.FILES.get('profile_image'): student.profile_image = request.FILES['profile_image']
        student.save()
        selected_subjects = request.POST.getlist('subjects')
        student.subjects.set(selected_subjects)
        messages.success(request, f'Student {student.first_name} created! Roll No: {student.roll_number}')
        return redirect('home')
    return render(request, 'students/create_student.html', {'subjects': subjects})

@login_required(login_url='login')
def edit_student(request, pk):
    if not (is_admin(request.user) or is_teacher(request.user)):
        messages.error(request, 'Access denied.'); return redirect('home')
    student = get_object_or_404(Student, pk=pk)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.mobile_number = request.POST.get('mobile_number')
        student.email = request.POST.get('email')
        student.gender = request.POST.get('gender')
        student.dob = request.POST.get('dob')
        student.qualification = request.POST.get('qualification')
        student.skill_java = 'skill_java' in request.POST
        student.skill_dotnet = 'skill_dotnet' in request.POST
        student.skill_python = 'skill_python' in request.POST
        student.skill_database = 'skill_database' in request.POST
        student.description = request.POST.get('description','')
        student.parent_name = request.POST.get('parent_name','')
        student.parent_mobile = request.POST.get('parent_mobile','')
        student.parent_email = request.POST.get('parent_email','')
        student.address = request.POST.get('address','')
        if request.FILES.get('profile_image'): student.profile_image = request.FILES['profile_image']
        student.save()
        student.subjects.set(request.POST.getlist('subjects'))
        messages.success(request, f'Student {student.first_name} updated!')
        return redirect('home')
    return render(request, 'students/edit_student.html', {'student': student, 'subjects': subjects})

@login_required(login_url='login')
def delete_student(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = f"{student.first_name} {student.last_name}"
        student.delete()
        messages.success(request, f'Student {name} deleted!')
        return redirect('home')
    return render(request, 'students/delete_confirm.html', {'student': student})

@login_required(login_url='login')
def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    marks = student.marks.all().order_by('-date')
    achievements = student.achievements.all().order_by('-date')
    attendance = student.attendance.all().order_by('-date')
    total_days = attendance.count()
    present_days = attendance.filter(status='Present').count()
    attendance_pct = round((present_days / total_days * 100), 1) if total_days > 0 else 0
    return render(request, 'students/report.html', {
        'student': student, 'marks': marks, 'achievements': achievements,
        'attendance': attendance, 'total_days': total_days,
        'present_days': present_days, 'attendance_pct': attendance_pct,
        'is_admin': is_admin(request.user), 'is_teacher': is_teacher(request.user),
    })

@login_required(login_url='login')
def add_marks(request, pk):
    if not is_teacher(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    student = get_object_or_404(Student, pk=pk)
    subjects = student.subjects.all()
    if request.method == 'POST':
        Mark.objects.create(
            student=student,
            subject_id=request.POST.get('subject'),
            marks_obtained=request.POST.get('marks_obtained'),
            max_marks=request.POST.get('max_marks', 100),
            exam_type=request.POST.get('exam_type','Mid Term'),
            added_by=request.user,
        )
        messages.success(request, 'Marks added successfully!')
        return redirect('student_report', pk=pk)
    return render(request, 'students/add_marks.html', {'student': student, 'subjects': subjects})

@login_required(login_url='login')
def add_achievement(request, pk):
    if not is_teacher(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        Achievement.objects.create(
            student=student,
            title=request.POST.get('title'),
            description=request.POST.get('description',''),
            date=request.POST.get('date'),
            added_by=request.user,
        )
        messages.success(request, 'Achievement added!')
        return redirect('student_report', pk=pk)
    return render(request, 'students/add_achievement.html', {'student': student})

@login_required(login_url='login')
def mark_attendance(request):
    if not is_teacher(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    students = Student.objects.filter(status='Active')
    today = date.today()
    existing = Attendance.objects.filter(date=today).values_list('student_id', flat=True)
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'attendance_{student.pk}', 'Absent')
            Attendance.objects.update_or_create(
                student=student, date=today,
                defaults={'status': status, 'marked_by': request.user}
            )
        messages.success(request, f'Attendance marked for {today}!')
        return redirect('home')
    return render(request, 'students/attendance.html', {'students': students, 'today': today, 'existing': existing})

@login_required(login_url='login')
def manage_events(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    events = Event.objects.all().order_by('-event_date')
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'),
            event_type=request.POST.get('event_type'),
            description=request.POST.get('description',''),
            event_date=request.POST.get('event_date'),
            created_by=request.user,
        )
        messages.success(request, 'Event added!')
        return redirect('manage_events')
    return render(request, 'students/events.html', {'events': events})

@login_required(login_url='login')
def manage_notifications(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    notifications = Notification.objects.all().order_by('-created_at')
    if request.method == 'POST':
        Notification.objects.create(
            title=request.POST.get('title'),
            message=request.POST.get('message'),
            target=request.POST.get('target','All'),
            created_by=request.user,
        )
        messages.success(request, 'Notification sent!')
        return redirect('manage_notifications')
    return render(request, 'students/notifications.html', {'notifications': notifications})

@login_required(login_url='login')
def manage_holidays(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    holidays = Holiday.objects.all().order_by('date')
    if request.method == 'POST':
        Holiday.objects.create(
            name=request.POST.get('name'),
            date=request.POST.get('date'),
            description=request.POST.get('description',''),
        )
        messages.success(request, 'Holiday added!')
        return redirect('manage_holidays')
    return render(request, 'students/holidays.html', {'holidays': holidays})

@login_required(login_url='login')
def best_student(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    awards = BestStudent.objects.all().order_by('-year')
    students = Student.objects.filter(status='Active')
    if request.method == 'POST':
        BestStudent.objects.update_or_create(
            year=request.POST.get('year'),
            defaults={
                'student_id': request.POST.get('student'),
                'reason': request.POST.get('reason'),
                'awarded_by': request.user,
            }
        )
        messages.success(request, 'Best Student award given!')
        return redirect('best_student')
    return render(request, 'students/best_student.html', {'awards': awards, 'students': students})

@login_required(login_url='login')
def manage_feedbacks(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'students/manage_feedbacks.html', {'feedbacks': feedbacks})

@login_required(login_url='login')
def manage_registrations(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    registrations = StudentRegistration.objects.all().order_by('-submitted_at')
    if request.method == 'POST':
        reg_id = request.POST.get('reg_id')
        action = request.POST.get('action')
        reg = get_object_or_404(StudentRegistration, pk=reg_id)
        reg.status = action
        reg.save()
        if action == 'Approved':
            Student.objects.create(
                first_name=reg.first_name, last_name=reg.last_name,
                mobile_number=reg.mobile_number, email=reg.email,
                gender=reg.gender, dob=reg.dob, qualification=reg.qualification,
                parent_name=reg.parent_name, parent_mobile=reg.parent_mobile,
                address=reg.address,
            )
            messages.success(request, f'{reg.first_name} approved and added as student!')
        else:
            messages.info(request, f'{reg.first_name} registration rejected.')
        return redirect('manage_registrations')
    return render(request, 'students/registrations.html', {'registrations': registrations})

@login_required(login_url='login')
def manage_subjects(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.'); return redirect('home')
    subjects = Subject.objects.all()
    if request.method == 'POST':
        Subject.objects.create(name=request.POST.get('name'), code=request.POST.get('code'))
        messages.success(request, 'Subject added!')
        return redirect('manage_subjects')
    return render(request, 'students/subjects.html', {'subjects': subjects})
