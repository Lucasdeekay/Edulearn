from django.urls import path, include
from rest_framework import routers

from Portal import views
from Portal.api_views import StudentAPIView, PerformanceAPIView, TeacherAPIView, PasscodeAPIView, PersonAPIView, \
    SubjectAPIView, ResultAPIView, DailyReportAPIView, ScoreAPIView, ReplyAPIView, MessageAPIView

router = routers.DefaultRouter()
router.register('student', StudentAPIView)
router.register('teacher', TeacherAPIView)
router.register('person', PersonAPIView)
router.register('performance', PerformanceAPIView)
router.register('daily-report', DailyReportAPIView)
router.register('password', PasscodeAPIView)
router.register('subject', SubjectAPIView)
router.register('score', ScoreAPIView)
router.register('result', ResultAPIView)
router.register('reply', ReplyAPIView)
router.register('message', MessageAPIView)

app_name = "Portal"

urlpatterns = [
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("login/forgot-password", views.forgot_password, name="forgot_password"),
    path("login/forgot-password/<str:username>/retrieve-password", views.password_retrieval, name="password_retrieval"),
    path("login/forgot-password/<str:username>/resend-password", views.resend_password, name="resend_password"),
    path("login/forgot-password/<str:username>/change-password", views.change_password, name="change_password"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("result", views.result, name="result"),
    path("review-results", views.review_results, name="review_results"),
    path("daily-report", views.daily_report, name="daily_report"),
    path("review-reports", views.review_reports, name="review_reports"),
    path("register-student", views.register_student, name="register_student"),
    path("review-students", views.review_students, name="review_students"),
    path("record-daily-report", views.record_daily_report, name="record_daily_report"),
    path("record-score", views.record_score, name="record_score"),
    path("message", views.message, name="message"),
    path("chat", views.chat, name="chat"),
    path("chat/delete_message<int:id>", views.delete_message, name="delete_message"),
    path("chat/reply_message<int:id>", views.reply_message, name="reply_message"),
    path("settings/profile", views.profile_settings, name="profile_settings"),
    path("settings/reset-password", views.reset_password, name="reset_password"),
    path("api/", include(router.urls)),
]
