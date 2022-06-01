from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Portal.extra import ContentTypeRestrictedFileField

states = ['Abia', 'Adamawa', 'Akwa Ibom', 'Anambra']
countries = ['Nigeria', 'Ghana', 'Togo']
subjects = ['Mathematics', 'English Language', 'Basic Science']


class Person(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=False)
    first_name = models.CharField(max_length=256, null=False)
    middle_name = models.CharField(max_length=256, null=False)
    sex = models.CharField(max_length=6, null=False, choices=[('Male', 'Male'), ('Female', 'Female')])
    dob = models.DateField()
    phone_number = models.CharField(max_length=16, null=False)
    email = models.EmailField(null=False)
    address = models.TextField(max_length=256, null=False)
    religion = models.CharField(max_length=20, null=False, choices=[('Christianity', 'Christianity'), ('Islam', 'Islam')])
    country = models.CharField(max_length=30, null=False, choices=[(x, x) for x in countries])
    state_of_origin = models.CharField(max_length=20, null=False, choices=[(x, x) for x in states])
    state_of_residence = models.CharField(max_length=20, null=False, choices=[(x, x) for x in states])
    image = ContentTypeRestrictedFileField(upload_to='Portal/profile_image',
                                           max_upload_size=5242880,
                                           content_types=['image/jpeg', 'image/jpg', 'image/png'],
                                           null=True,
                                           blank=True,
                                           max_length=250)
    role = models.CharField(max_length=10, null=False, choices=[('Student', 'Student'), ('Teacher', 'Teacher')])

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}"


class Teacher(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    assigned_class = models.CharField(max_length=50, null=True, blank=True,  choices=[
        ('JS1', 'JS1'), ('JS2', 'JS2'), ('JS3', 'JS3'),
        ('SS1', 'SS1'), ('SS2', 'S2'), ('SS3', 'SS3'),
    ])

    def __str__(self):
        return {self.person}


class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    assigned_class = models.CharField(max_length=50, null=True, blank=True, choices=[
        ('JS1', 'JS1'), ('JS2', 'JS2'), ('JS3', 'JS3'),
        ('SS1', 'SS1'), ('SS2', 'S2'), ('SS3', 'SS3'),
    ])

    def __str__(self):
        return {self.person}


class Passcode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    recovery_password = models.CharField(max_length=12, null=False)
    time = models.DateTimeField(null=False)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} -> {self.recovery_password}"

    def expiry(self):
        if (timezone.now() - self.time) >= timezone.timedelta(hours=1):
            self.delete()
        else:
            pass


class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=False)
    attentiveness = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Performance report for {self.student} on {self.date}"


class DailyReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    report = models.TextField(max_length=500)
    date = models.CharField(max_length=16, null=False)

    def __str__(self):
        return f'{self.student} -> {self.report}'


class Subject(models.Model):
    subject = models.CharField(max_length=30, null=False, choices=[(x, x) for x in subjects])

    def __str__(self):
        return self.subject


class Score(models.Model):
    session = models.CharField(max_length=25, null=False, choices=[
        (f'{x}/{x+1}', f'{x}/{x+1}') for x in range(2022, 2050)
    ])
    term = models.CharField(max_length=25, null=False, choices=[
        ('1st', '1st'), ('1st Mid-Term', '1st Mid-Term'), ('2nd', '2nd'), ('2nd Mid-Term', '2nd Mid-Term')
    ])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.student} -> {self.subject} -> {self.session} -> {self.term}'


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    result = models.ManyToManyField(Score, blank=True, null=True)

    def __str__(self):
        return {self.student}


class Reply(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    reply = models.CharField(max_length=1000)
    date = models.DateTimeField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.reply}'


class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="receiver")
    message = models.CharField(max_length=1000)
    date = models.DateTimeField()
    reply = models.ManyToManyField(Reply)


    def __str__(self):
        return f'{self.message}'

    def draft(self):
        return self.message[:250]