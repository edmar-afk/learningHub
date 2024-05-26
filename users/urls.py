from django.urls import path
from . import views



urlpatterns = [
    path('mainLogin', views.mainLogin, name='mainLogin'),
    path('mainDashboard', views.dashboard, name='mainDashboard'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('disapprove-user/<int:user_id>/', views.disapprove_user, name='disapprove_user'),
    
    path('approve-instructor/<int:instructor_id>/', views.approve_instructor, name='approve_instructor'),
    path('disapprove-instructor/<int:instructor_id>/', views.disapprove_instructor, name='disapprove_instructor'),
    path('<int:user_id>/deleteuser/', views.deleteUser, name='deleteuser'),
    
    path('homepage', views.homepage, name='homepage'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('logout', views.logoutUser, name='logout'),
    
    
    
    path('forum_page', views.forum_page, name='forum_page'),
    path('student_about', views.student_about, name='student_about'),
    path('student_forum', views.student_forum, name='student_forum'),
    path('student_lesson', views.student_lesson, name='student_lesson'),
    path('student_quizzes', views.student_quizzes, name='student_quizzes'),
    path('student_announcement', views.student_announcement, name='student_announcement'),
    path('student_lesson', views.student_lesson, name='student_lesson'),
    path('startquiz/<int:q_id>/', views.student_startQuiz, name='start_quiz'),
     
    path('instructor_lesson', views.instructor_lesson, name='instructor_lesson'),
    path('instructor_quizzes', views.instructor_quizzes, name='instructor_quizzes'),
    path('questions/<int:q_id>/', views.questions, name='questions'),
    path('instructor_forum', views.instructor_forum, name='instructor_forum'),
    path('forum_page1', views.forum_page1, name='forum_page1'),
    path('instructor_lesson', views.instructor_lesson, name='instructor_lesson'),
    path('instructor_announcement', views.instructor_announcements, name='instructor_announcement'),
    path('instructor_about', views.instructor_about, name='instructor_about'),
    
    
    path('<int:announcement_id>/deleteannouncement/', views.deleteAnnouncement, name='deleteannouncement'),
    path('<int:q_id>/deletequestion/', views.deletequestion, name='deletequestion'),
    path('<int:q_id>/deletequiz/', views.deletequiz, name='deletequiz'),
    path('<int:forum_id>/deleteforum/', views.deleteForum, name='deleteforum'),
    path('<int:lesson_id>/deletelesson/', views.deleteLesson, name='deletelesson'),
]