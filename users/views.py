import random
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Questions, Quizz, Lesson, Score, Announcement, Forum, Comments
from django.db.models import Count
from datetime import datetime
from django.utils.dateparse import parse_date
# Create your views here.




def mainLogin(request):
    return render(request, 'main/mainLogin.html')

def dashboard(request):
    student = User.objects.filter(last_name='Student').order_by('-id')
    instructor = User.objects.filter(last_name='Teacher').order_by('-id')
    context = {
        'student': student,
        'instructor':instructor
       
    }
    return render(request, 'main/mainDashboard.html', context)


def approve_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')

def disapprove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = False
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')


def approve_instructor(request, instructor_id):
    user = User.objects.get(pk=instructor_id)
    user.is_superuser = True
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')

def disapprove_instructor(request, instructor_id):
    user = User.objects.get(pk=instructor_id)
    user.is_superuser = False
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')


def deleteUser(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'User Removed')
    return redirect('/mainDashboard')




def about(request):
    return render(request, 'about.html')

def logoutUser(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('user_login')

def homepage(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password1']
        repeat_password = request.POST['password2']
       
        if password != repeat_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('register')

        else:
            # Create new user
            user = User.objects.create_user(first_name=fullname, username=email, email=email, password=password, last_name=role)
            user.save()
            messages.success(request, 'You have been registered successfully.')
            return redirect('user_login')

    return render(request, 'register.html')


def user_login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect('instructor_forum') 
            
            elif user.is_staff:
                return redirect('student_forum')
            
            else:
                messages.error(request, "Wait for Admin to Approve your account")
                return redirect('user_login')
            
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('user_login')

    return render(request, 'login.html')



@login_required(login_url='/login')
def student_quizzes(request):
    user = request.user
    quizzes = Quizz.objects.all().order_by('-id')
    taken_quizzes = Score.objects.filter(taker=user).values_list('quiz', flat=True)
    
    context = {
        'quizzes': quizzes,
        'taken_quizzes': taken_quizzes,
    }
    
    return render(request, 'student/quizzes.html', context)


@login_required(login_url='/login')
def student_startQuiz(request, q_id):
    quizz = get_object_or_404(Quizz, id=q_id)
    questions = Questions.objects.filter(name=q_id).order_by('-id')
    
    questions_number = Questions.objects.filter(name=q_id).count()
   
    
    if request.method == 'POST':
        score = request.POST['score']
        
        new_score = Score.objects.create(score=score, quiz=quizz, taker=request.user)

        new_score.save()
        
        messages.success(request, 'You have submitted your score.')
        return redirect('student_quizzes')
        
    context = {
        'quizz': quizz,
        'questions': questions,
        'questions_number':questions_number,
        
    }
    return render(request, 'student/start.html', context)


@login_required(login_url='/login')
def student_announcement(request):
   
    
    announcements = Announcement.objects.all().order_by('-upload_date')
    context = {
        
        'announcements':announcements 
    }
    return render(request, 'student/announcements.html',context)



@login_required(login_url='/login')
def student_lesson(request):

    topic_lists = Lesson.objects.all().order_by('-upload_date')

    context = { 
    
        'topic_lists': topic_lists,
      
    }
    return render(request, 'student/lesson.html', context)


@login_required(login_url='/login')
def student_forum(request):
   
    # Retrieve all forums with comment counts
    forums = Forum.objects.annotate(comment_count=Count('comments')).order_by('-id')
    
    if request.method == 'POST':
        comment = request.POST['comment']
        commentor = request.POST['commentor']
        post_id = request.POST['post']  # Retrieve the post ID
        
        # Get the corresponding Forum instance
        forum = get_object_or_404(Forum, pk=post_id)
        
        new_comment = Comments.objects.create(comment=comment, commentors=request.user, post=forum)
        new_comment.save()
        
    comments_lists = Comments.objects.all().order_by('comment_date')
    
    context = {
        'forums': forums,
        'comments_lists': comments_lists,
    }
    return render(request, 'student/forums.html', context)

def forum_page(request):
   
    # Retrieve all forums with comment counts
    forums = Forum.objects.annotate(comment_count=Count('comments')).order_by('-upload_date')
    
    if request.method == 'POST':
        comment = request.POST['comment']
       
        post_id = request.POST['post']  # Retrieve the post ID
        
        # Get the corresponding Forum instance
        forum = get_object_or_404(Forum, pk=post_id)
        
        new_comment = Comments.objects.create(comment=comment, commentors=request.user, post=forum)
        new_comment.save()
    
    # Get the forum_id from the query parameters
    forum_id = request.GET.get('forum_id')

    # Retrieve the forum object using the forum_id
    forum = Forum.objects.get(id=forum_id)

    # Retrieve all comments related to the forum
    comments = Comments.objects.filter(post=forum)
    
    context = {
        'forum': forum, 
        'comments': comments,
    }
    # Render the forum page template with the forum object and comments
    return render(request, 'student/forumPost.html', context)
























@login_required(login_url='/login')
def instructor_quizzes(request):
    quiz = Quizz.objects.filter(creator=request.user).prefetch_related('score_set')
    
    if request.method == 'POST':
        title = request.POST['title']
        # deadline_str = request.POST['deadline']
        # timelimit = request.POST['timelimit']
        
        
        # deadline_date = datetime.strptime(deadline_str, "%m/%d/%Y").strftime("%Y-%m-%d")
        
        new_quizz = Quizz.objects.create(title=title, creator=request.user)
        new_quizz.save()
        messages.success(request, 'New Quiz Uploaded')
        
    context = {
        'quiz': quiz,
    }
    
    return render(request, 'instructor/quizzes.html', context)


@login_required(login_url='/login')
def questions(request, q_id):
    quizz = get_object_or_404(Quizz, id=q_id)
    questions = Questions.objects.filter(name=q_id).order_by('-id')
    
    if request.method == 'POST':
        question = request.POST['question']

        answer = request.POST['answer']
        
        new_question = Questions.objects.create(name=quizz, question=question, answer=answer)
        new_question.save()
        messages.success(request, 'New Question Uploaded')
        
    context = {
        'quizz': quizz,
        'questions':questions,
    } 
    
    return render(request, 'instructor/questions.html', context)

def deletequestion(request, q_id):
    Questions.objects.filter(id=q_id).delete()
    messages.success(request, 'Question Removed')
    return redirect('/instructor_quizzes')

def deletequiz(request, q_id):
    Quizz.objects.filter(id=q_id).delete()
    messages.success(request, 'Quiz Removed')
    return redirect('/instructor_quizzes')



@login_required(login_url='/login')
def instructor_forum(request):
    authenticated_user = request.user
    students = User.objects.filter(last_name='Student')
    forums = Forum.objects.filter(uploader=authenticated_user).annotate(comment_count=Count('comments')).order_by('-id')
    comments_lists = Comments.objects.all().order_by('comment_date')

    if request.method == 'POST':
        if 'forum_form_submit' in request.POST:
            title = request.POST['title']
            description = request.POST['description']
            file = request.FILES.get('file')  # Use get() to avoid KeyError
            
            new_forum = Forum.objects.create(title=title, description=description, uploader=authenticated_user, file=file)
            new_forum.save()
            messages.success(request, 'Forum Added!')
             
        elif 'comment_form_submit' in request.POST:
            comment = request.POST['comment']
            commentor = request.POST['commentor']
            post_id = request.POST['post']  # Retrieve the post ID
        
            forum = get_object_or_404(Forum, pk=post_id)
        
            new_comment = Comments.objects.create(comment=comment, commentors=authenticated_user, post=forum)
            new_comment.save()
    
    context = {
        'students': students,
        'authenticated_user': authenticated_user,
        'forums': forums,
        'comments_lists': comments_lists,
    }
    return render(request, 'instructor/forum.html', context)


def deleteForum(request, forum_id):
    Forum.objects.filter(id=forum_id).delete()
    messages.success(request, 'Forum deleted')
    return redirect('/instructor_forum')


def forum_page1(request):
   
   
    # Retrieve all forums with comment counts
    forums = Forum.objects.annotate(comment_count=Count('comments')).order_by('-upload_date')
    
    if request.method == 'POST':
        comment = request.POST['comment']
        commentor = request.POST['commentor']
        post_id = request.POST['post']  # Retrieve the post ID
        
        # Get the corresponding Forum instance
        forum = get_object_or_404(Forum, pk=post_id)
        
        new_comment = Comments.objects.create(comment=comment, commentors=request.user, post=forum)
        new_comment.save()
    
    # Get the forum_id from the query parameters
    forum_id = request.GET.get('forum_id')

    # Retrieve the forum object using the forum_id
    forum = Forum.objects.get(id=forum_id)

    # Retrieve all comments related to the forum
    comments = Comments.objects.filter(post=forum)
    
    context = {
        'forum': forum, 
        'comments': comments,
    }
    # Render the forum page template with the forum object and comments
    return render(request, 'instructor/forumPost.html', context)




@login_required(login_url='/login')
def instructor_announcements(request):
   
   
    # Now you can use the teacher object as needed
    # For example, accessing its profile_pic, id_no, etc.
    students = User.objects.filter(last_name='Student')
    announcements = Announcement.objects.filter(uploader=request.user).order_by('-upload_date')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        
        # Check if a file was uploaded
        if 'file' in request.FILES:
            file = request.FILES['file']
            new_announcement = Announcement.objects.create(title=title, description=description, uploader=request.user, file=file, like=0)
            new_announcement.save()
            messages.success(request, 'Announcement Added!')
        else:
            # Handle case where no file was uploaded
            new_announcement = Announcement.objects.create(title=title, description=description, uploader=request.user, like=0)
            new_announcement.save()
            messages.success(request, 'Announcement Added!')
 
    context = {
        'students': students,
        'announcements': announcements,
    }
    return render(request, 'instructor/announcement.html', context)


def deleteAnnouncement(request,  announcement_id):
    Announcement.objects.filter(id = announcement_id).delete()
    messages.success(request, 'Announcement deleted')
    return redirect('/instructor_announcement')



@login_required(login_url='/login')
def instructor_lesson(request):
    
    authenticated_user = request.user
    
    # Now you can use the teacher object as needed
    # For example, accessing its profile_pic, id_no, etc.
    students = User.objects.filter(last_name='Student')
    lesson = Lesson.objects.filter(uploader=request.user).order_by('-upload_date')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['file']
        
        new_topic = Lesson.objects.create(title=title, description=description, uploader=request.user, file=file)
        new_topic.save()
        messages.success(request, 'Lesson Added!')
    context = {
        'students': students,
        'lesson':lesson,
    }
    return render(request, 'instructor/lesson.html', context)

def deleteLesson(request, lesson_id):
    Lesson.objects.filter(id=lesson_id).delete()
    messages.success(request, 'Lesson deleted')
    return redirect('/lesson')





def instructor_about(request):
    return render(request, 'instructor/about.html')

def student_about(request):
    return render(request, 'student/about.html')