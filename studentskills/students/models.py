from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    def __str__(self): return f"{self.code} - {self.name}"

class Student(models.Model):
    QUALIFICATION_CHOICES = [('B.Tech','B. Tech'),('MCA','MCA'),('Graduation','Graduation'),('Post-Graduation','Post-Graduation'),('MBA','MBA'),('Others','Others')]
    GENDER_CHOICES = [('Male','Male'),('Female','Female')]
    STATUS_CHOICES = [('Active','Active'),('Inactive','Inactive')]

    roll_number = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    skill_java = models.BooleanField(default=False)
    skill_dotnet = models.BooleanField(default=False)
    skill_python = models.BooleanField(default=False)
    skill_database = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    parent_name = models.CharField(max_length=100, blank=True)
    parent_mobile = models.CharField(max_length=15, blank=True)
    parent_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.first_name} {self.last_name}"
    def get_skills(self):
        skills = []
        if self.skill_java: skills.append('JAVA')
        if self.skill_dotnet: skills.append('.Net')
        if self.skill_python: skills.append('Python')
        if self.skill_database: skills.append('Database')
        return ', '.join(skills) if skills else 'None'
    def save(self, *args, **kwargs):
        if not self.roll_number:
            super().save(*args, **kwargs)
            self.roll_number = f"JALA{self.pk:04d}"
            Student.objects.filter(pk=self.pk).update(roll_number=self.roll_number)
        else:
            super().save(*args, **kwargs)

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    exam_type = models.CharField(max_length=50, default='Mid Term')
    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def percentage(self): return round((self.marks_obtained / self.max_marks) * 100, 2)

class Achievement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Attendance(models.Model):
    STATUS_CHOICES = [('Present','Present'),('Absent','Absent'),('Late','Late')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta: unique_together = ('student', 'date')

class Event(models.Model):
    EVENT_TYPES = [('Fee','Fee Due'),('Exam','Exam'),('Result','Result'),('Cultural','Cultural'),('Sports','Sports'),('Holiday','Holiday'),('Other','Other')]
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    ROLE_CHOICES = [('Student','Student'),('Parent','Parent')]
    TYPE_CHOICES = [('Feedback','Feedback'),('Complaint','Complaint')]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    feedback_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    target = models.CharField(max_length=20, default='All')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BestStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    reason = models.TextField()
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta: unique_together = ('student', 'year')

class Holiday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)

class StudentRegistration(models.Model):
    STATUS_CHOICES = [('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    qualification = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=100, blank=True)
    parent_mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
