import datetime
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
import random

from django.utils import timezone

from Edulearn.settings import EMAIL_HOST_USER
from Portal.forms import RegistrationForm, LoginForm, ForgotPasswordForm, PasswordRetrievalForm, ChangePasswordForm, \
    ProfileForm, SelectSessionPeriodForm, StudentRegistrationForm, StudentAssessmentForm, ResultForm, \
    SelectSessionPeriodAndStudentForm
from Portal.models import Student, Passcode, Teacher, Person, DailyReport, Result, Score, Performance

random = random.Random()


# Custom Functions
def check_registered_users(request, username, email):
    all_persons = Person.objects.all()

    for person in all_persons:
        if username == person.user.username:
            messages.error(request, "Username already in use")
            return HttpResponseRedirect(reverse('Portal:register'))
        elif email == person.email:
            messages.error(request, "Email already in use")
            return HttpResponseRedirect(reverse('Portal:register'))


def create_user(request, username, email, password, confirm_password, first_name, last_name):
    if password == confirm_password:
        return User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                        last_name=last_name)
    else:
        messages.error(request, "Password does not match")
        return HttpResponseRedirect(reverse('Portal:register'))


def create_personnel(user, email, first_name, last_name, middle_name, sex, dob, phone_number, address,
                     religion, country, state_of_origin, state_of_residence, role):
    person = Person.objects.create(last_name=last_name, first_name=first_name, middle_name=middle_name,
                                   sex=sex, dob=dob, phone_number=phone_number, email=email, address=address,
                                   religion=religion, country=country, state_of_origin=state_of_origin,
                                   state_of_residence=state_of_residence, role=role)
    person.user = user
    person.save()
    if role == 'Student':
        Student.objects.create(person=person)
    else:
        Teacher.objects.create(person=person)


def check_if_user_has_unused_password(user):
    all_passwords = Passcode.objects.filter(user=user)
    for password in all_passwords:
        if password.is_valid:
            password.is_valid = False
            password.save()


def delete_expired_password():
    all_passwords = Passcode.objects.filter(is_valid=True)
    for password in all_passwords:
        password.expiry()


def get_daily_report(date):
    if (timezone.now() - date) > datetime.timedelta(days=7):
        return ""
    else:
        try:
            report = get_object_or_404(DailyReport, date=date)
            if report is None:
                get_daily_report(date - datetime.timedelta(days=1))
            else:
                return report
        except Exception as e:
            get_daily_report(date - datetime.timedelta(days=1))


def change_profile_bio(person, user, last_name, first_name, middle_name, username, phone_number, email, address, image):
    if last_name != '':
        person.last_name = last_name

    if first_name != '':
        person.first_name = first_name

    if middle_name != '':
        person.middle_name = middle_name

    if username != '':
        user.username = username
        user.save()

    if phone_number != '':
        person.phone_number = phone_number

    if email != '':
        person.email = email

    if address != '':
        person.address = address

    if image != '':
        person.image = image

    person.save()


# View Functions
def register(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('Portal:dashboard'))
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                last_name = form.cleaned_data['last_name'].capitalize().strip()
                first_name = form.cleaned_data['first_name'].capitalize().strip()
                middle_name = form.cleaned_data['middle_name'].capitalize().strip()
                username = form.cleaned_data['username'].strip()
                sex = form.cleaned_data['sex'].capitalize().strip()
                dob = form.cleaned_data['dob']
                phone_number = form.cleaned_data['phone_number'].strip()
                email = form.cleaned_data['email'].strip()
                address = form.cleaned_data['address'].capitalize()
                religion = form.cleaned_data['religion'].capitalize()
                country = form.cleaned_data['country'].capitalize()
                state_of_origin = form.cleaned_data['state_of_origin'].capitalize()
                state_of_residence = form.cleaned_data['state_of_residence'].capitalize()
                password = form.cleaned_data['password'].strip()
                confirm_password = form.cleaned_data['confirm_password'].strip()
                role = form.cleaned_data['role'].capitalize().strip()

                check_registered_users(request, username, email)

                user = create_user(request, username, email, password, confirm_password, first_name, last_name)

                create_personnel(user, email, first_name, last_name, middle_name, sex, dob, phone_number, address,
                                 religion, country, state_of_origin, state_of_residence, role)

                subject = 'Password Update Successful'
                msg = "Registration successful. A mail of approval will be sent to your email when " \
                      "your registration has been approved, alongside your login details. Thank You."
                context = {'subject': subject, 'msg': msg}
                # html_message = render_to_string('Portal/msg.html', context=context)
                #
                # send_mail(subject, msg, EMAIL_HOST_USER, [email], html_message=html_message,
                #           fail_silently=False)

                messages.success(request,
                                 "Registration successful. A mail of approval will be sent to your email within "
                                 "the next 48hrs. Thank You.")
                return HttpResponseRedirect(reverse('Portal:login'))
            else:
                return HttpResponseRedirect(reverse('Portal:register'))
        else:
            form = RegistrationForm()
            context = {'form': form}
            return render(request, "Portal/register.html", context)


def log_in(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('Portal:dashboard'))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username'].strip()
                password = form.cleaned_data['password'].strip()
                user = authenticate(request, username=username, password=password)
                if user is not None and not user.is_superuser:
                    person = get_object_or_404(Person, user=user)
                    if form.cleaned_data['role']:
                        if person.role == 'Teacher':
                            login(request, user)
                            return HttpResponseRedirect(reverse("Portal:dashboard"))
                        else:
                            messages.error(request, "User is not a staff")
                            return HttpResponseRedirect(reverse("Portal:login"))
                    else:
                        if person.role == 'Student':
                            login(request, user)
                            return HttpResponseRedirect(reverse("Portal:dashboard"))
                        else:
                            messages.error(request, "User is not a student")
                            return HttpResponseRedirect(reverse("Portal:login"))
                else:
                    messages.error(request, "Invalid login credentials")
                    return HttpResponseRedirect(reverse("Portal:login"))
        else:
            form = LoginForm()
            context = {'form': form}
            return render(request, "Portal/login.html", context)


def forgot_password(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('Portal:dashboard'))
    else:
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email'].strip()
                all_users = User.objects.all()
                for user in all_users:
                    if user.email == email:
                        recovery_password = ''.join(
                            [random.choice(string.ascii_letters + string.digits) for i in range(12)])
                        subject = 'Password Recovery'

                        check_if_user_has_unused_password(user)

                        Passcode.objects.create(user=user, recovery_password=recovery_password,
                                                time=timezone.now())

                        msg = f"Recovery password will expire after an hour. Your password is displayed below"
                        context = {'subject': subject, 'msg': msg, 'recovery_password': recovery_password,
                                   'username': user.username}
                        # html_message = render_to_string('Portal/msg.html', context=context)
                        # send_mail(subject, msg, EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)

                        messages.success(request, "Recovery password has been successfully sent")
                        return HttpResponseRedirect(reverse("Portal:password_retrieval", args=(user.username,)))
                else:
                    messages.error(request, "User profile not found")
                    return HttpResponseRedirect(reverse('Portal:forgot_password'))
        else:
            form = ForgotPasswordForm()
            context = {'form': form}
            return render(request, "Portal/forgot_password.html", context)


def resend_password(request, username):
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('Portal:dashboard'))
    else:
        user = get_object_or_404(User, username=username)

        recovery_password = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(12)])
        subject = 'Password Recovery'

        check_if_user_has_unused_password(user)

        Passcode.objects.create(user=user, recovery_password=recovery_password,
                                time=timezone.now())

        msg = f"Recovery password will expire after an hour. Your password is displayed below"
        context = {'subject': subject, 'msg': msg, 'recovery_password': recovery_password,
                   'username': user.username}
        # html_message = render_to_string('Portal/msg.html', context=context)
        # send_mail(subject, msg, EMAIL_HOST_USER, [user.email], html_message=html_message, fail_silently=False)

        messages.success(request, "Recovery password has been successfully sent")
        return HttpResponseRedirect(reverse("Portal:password_retrieval", args=(user.username,)))


def password_retrieval(request, username):
    delete_expired_password()

    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('Portal:dashboard'))
    else:
        if request.method == 'POST':
            form = PasswordRetrievalForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password'].strip()
                all_password = Passcode.objects.all()
                user = get_object_or_404(User, username=username)

                for passcode in all_password:
                    if passcode.user == user and passcode.recovery_password == password and passcode.is_valid:
                        passcode.valid = False
                        subject = 'Password Recovery Successful'
                        msg = "Account has been successfully recovered. Kindly proceed to update your password"
                        context = {'subject': subject, 'msg': msg}
                        # html_message = render_to_string('Portal/msg.html', context=context)

                        # send_mail(subject, msg, EMAIL_HOST_USER, [user.email], html_message=html_message,
                        #           fail_silently=False)

                        messages.success(request,
                                         'Account has been successfully recovered. Kindly update your password')
                        return HttpResponseRedirect(reverse('Portal:change_password', args=(username,)))
                else:
                    messages.error(request,
                                   "Incorrect recovery password. Click on resend to get the retrieval password again")
                    return HttpResponseRedirect(reverse('Portal:password_retrieval', args=(username,)))
        else:
            form = PasswordRetrievalForm()
            user = get_object_or_404(User, username=username)
            context = {'user': user, 'username': username, 'form': form}
            return render(request, 'Portal/password_retrieval.html', context)


def change_password(request, username):
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('Portal:dashboard'))
    else:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password'].strip()
                confirm_password = form.cleaned_data['confirm_password'].strip()

                if password == confirm_password:
                    user = get_object_or_404(User, username=username)
                    user.set_password(password)
                    user.save()

                    subject = 'Password Changed Successful'
                    msg = "Account password has  been successfully changed"
                    context = {'subject': subject, 'msg': msg}
                    # html_message = render_to_string('Portal/msg.html', context=context)

                    # send_mail(subject, msg, EMAIL_HOST_USER, [user.email], html_message=html_message,
                    #           fail_silently=False)

                    messages.success(request, 'Password successfully changed')
                    return HttpResponseRedirect(reverse('Portal:login'))
                else:
                    messages.error(request, "Password does not match")
                    return HttpResponseRedirect(reverse("Portal:change_password"))
        else:
            form = ChangePasswordForm()
            context = {'form': form}
            return render(request, "Portal/change_password.html", context)


def dashboard(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        context = {'person': person}
        return render(request, 'Portal/dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def result(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = SelectSessionPeriodForm(request.POST)
            if form.is_valid():
                session_period = form.cleaned_data['session_period'].strip()
                session_term = form.cleaned_data['session_term'].strip()

                score = Score.objects.filter(session= session_period,term=session_term, student=person)

                context = {'form': form, 'person': person, 'score':score}
                return render(request, 'Portal/result.html', context)
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse("Portal:result"))
        else:
            form = SelectSessionPeriodForm()
            context = {'form': form, 'person': person, 'score': ''}
            return render(request, 'Portal/result.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def daily_report(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        date = datetime.date.today()
        if request.method == 'POST':
            date = request.POST.get('date')
        report = get_daily_report(timezone.now())
        if report is None:
            context = {'person': person, 'report': '', 'date': date}
        else:
            context = {'person': person, 'report': report, 'date': date}
        return render(request, 'Portal/daily_report.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def profile_settings(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                last_name = form.cleaned_data['last_name'].strip()
                first_name = form.cleaned_data['first_name'].strip()
                middle_name = form.cleaned_data['middle_name'].strip()
                username = form.cleaned_data['username'].strip()
                phone_number = form.cleaned_data['phone_number'].strip()
                email = form.cleaned_data['email'].strip()
                address = form.cleaned_data['address'].strip()
                image = form.cleaned_data['image']

                change_profile_bio(person, request.user, last_name, first_name, middle_name, username, phone_number, email, address, image)

                messages.success(request, "Profile successfully edited")
                return HttpResponseRedirect(reverse("Portal:profile_settings"))
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse("Portal:profile_settings"))
        else:
            form = ProfileForm()
            context = {'form': form, 'person': person}
            return render(request, 'Portal/profile_settings.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def reset_password(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password'].strip()
                confirm_password = form.cleaned_data['confirm_password'].strip()

                if password == confirm_password:
                    request.user.set_password(password)
                    request.user.save()
                    messages.success(request, "Password successfully set")
                    return HttpResponseRedirect(reverse("Portal:reset_password"))
                else:
                    messages.error(request, "Password does not match")
                    return HttpResponseRedirect(reverse("Portal:reset_password"))
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse("Portal:reset_password"))
        else:
            form = ChangePasswordForm()
            context = {'form': form, 'person': person}
            return render(request, 'Portal/reset_password.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def register_student(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                last_name = form.cleaned_data['last_name'].capitalize().strip()
                first_name = form.cleaned_data['first_name'].capitalize().strip()
                middle_name = form.cleaned_data['middle_name'].capitalize().strip()
                username = form.cleaned_data['username'].strip()
                sex = form.cleaned_data['sex'].capitalize().strip()
                dob = form.cleaned_data['dob']
                phone_number = form.cleaned_data['phone_number'].strip()
                email = form.cleaned_data['email'].strip()
                address = form.cleaned_data['address'].capitalize()
                religion = form.cleaned_data['religion'].capitalize()
                country = form.cleaned_data['country'].capitalize()
                state_of_origin = form.cleaned_data['state_of_origin'].capitalize()
                state_of_residence = form.cleaned_data['state_of_residence'].capitalize()
                password = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
                role = 'Student'

                check_registered_users(request, username, email)

                user = create_user(request, username, email, password, password, first_name, last_name)

                create_personnel(user, email, first_name, last_name, middle_name, sex, dob, phone_number, address,
                                 religion, country, state_of_origin, state_of_residence, role)

                subject = 'Password Update Successful'
                msg = "Registration successful. A mail of approval will be sent to your email when " \
                      "your registration has been approved, alongside your login details. Thank You."
                context = {'subject': subject, 'msg': msg}
                # html_message = render_to_string('Portal/msg.html', context=context)
                #
                # send_mail(subject, msg, EMAIL_HOST_USER, [email], html_message=html_message,
                #           fail_silently=False)

                messages.success(request, "Registration successful")
                return HttpResponseRedirect(reverse('Portal:register_student'))
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse('Portal:register_student'))
        else:
            form = StudentRegistrationForm()
            context = {'form': form, 'person': person}
            return render(request, "Portal/register_student.html", context)
    else:
        return HttpResponseRedirect(reverse('Portal:login'))


def record_daily_report(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = StudentAssessmentForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                report = form.cleaned_data['report']
                attentiveness = form.cleaned_data['attentiveness']
                date = request.POST.get('date')

                performance = Performance.objects.create(student=student, date=date, attentiveness=attentiveness)

                DailyReport.objects.create(student=student, performance=performance, report=report, date=date)

                messages.success(request, "Report added")
                return HttpResponseRedirect(reverse('Portal:record_daily_report'))
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse('Portal:record_daily_report'))
        else:
            form = StudentAssessmentForm()
            context = {'form': form, 'person': person}
            return render(request, "Portal/record_daily_report.html", context)
    else:
        return HttpResponseRedirect(reverse('Portal:login'))


def record_score(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = ResultForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                subject = form.cleaned_data['subject']
                score = form.cleaned_data['score']

                Result.objects.create(student=student, subject=subject, score=score)

                messages.success(request, "Student score added")
                return HttpResponseRedirect(reverse('Portal:record_score'))
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse('Portal:record_score'))
        else:
            form = ResultForm()
            context = {'form': form, 'person': person}
            return render(request, "Portal/record_score.html", context)
    else:
        return HttpResponseRedirect(reverse('Portal:login'))


def review_students(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        teacher = get_object_or_404(Teacher, person=person)
        all_students = Student.objects.filter(assigned_class=teacher.assigned_class)
        context = {'all_students': all_students, 'person': person}
        return render(request, 'Portal/review_students.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def review_reports(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        date = datetime.date.today()
        if request.method == 'POST':
            date = request.POST.get('date')
        all_reports = DailyReport.objects.filter(date=date)
        context = {'all_reports': all_reports, 'person': person}
        return render(request, 'Portal/review_reports.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def review_results(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        person = get_object_or_404(Person, user=request.user)
        if request.method == 'POST':
            form = SelectSessionPeriodAndStudentForm(request.POST)
            if form.is_valid():
                session_period = form.cleaned_data['session_period'].strip()
                session_term = form.cleaned_data['session_term'].strip()
                student = form.cleaned_data['student'].strip()

                score = Score.objects.filter(session=session_period, term=session_term, student=person)

                context = {'form':form, 'person':person, 'score':score, 'session':session_period, 'term':session_term}
                return render(request, 'Portal/result.html', context)
            else:
                messages.error(request, "Invalid form submission.")
                return HttpResponseRedirect(reverse("Portal:review_results"))
        else:
            form = SelectSessionPeriodAndStudentForm()
            context = {'form': form, 'person': person, 'score': ''}
            return render(request, 'Portal/review_results.html', context)
    else:
        return HttpResponseRedirect(reverse("Portal:login"))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("Portal:login"))
