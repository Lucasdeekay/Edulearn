from django.contrib import admin

from Portal.models import Student, Teacher, Performance, Passcode, Person, Subject, Result, DailyReport, Score


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'middle_name', 'sex', 'dob', 'phone_number', 'email', 'address',
                    'religion', 'country', 'state_of_origin', 'state_of_residence', 'image', 'role')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('person', 'assigned_class')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'assigned_class')


class PasscodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recovery_password', 'time', 'is_valid')


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'attentiveness')


class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'performance', 'report', 'date')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject',)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('session', 'term', 'student', 'subject', 'score')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('student',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Passcode, PasscodeAdmin)
admin.site.register(DailyReport, DailyReportAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Result, ResultAdmin)
