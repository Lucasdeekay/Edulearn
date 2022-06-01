from rest_framework import viewsets

from Portal.models import Student, Teacher, Performance, Passcode, Person, Subject, Result, DailyReport, Score, Reply, \
    Message
from Portal.serializers import StudentSerializer, TeacherSerializer, PerformanceSerializer, PasscodeSerializer, \
    PersonSerializer, SubjectSerializer, ResultSerializer, DailyReportSerializer, ScoreSerializer, ReplySerializer, \
    MessageSerializer


class PersonAPIView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class TeacherAPIView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class StudentAPIView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class PasscodeAPIView(viewsets.ModelViewSet):
    serializer_class = PasscodeSerializer
    queryset = Passcode.objects.all()


class PerformanceAPIView(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()


class DailyReportAPIView(viewsets.ModelViewSet):
    serializer_class = DailyReportSerializer
    queryset = DailyReport.objects.all()


class SubjectAPIView(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class ScoreAPIView(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    queryset = Score.objects.all()


class ResultAPIView(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()


class ReplyAPIView(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()


class MessageAPIView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
