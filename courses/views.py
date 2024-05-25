from django.shortcuts import render
from django.contrib import messages
from courses.models import Course, Topic
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from courses.forms import CommentForm, Comment, ReplyCommentForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

def CoursesHome(request : HttpRequest) -> HttpResponse:
    context ={
        'sign_log': True,
    }
    
    courses_list = Course.objects.all()
    per_page = 3
    paginator = Paginator(courses_list, per_page)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
        
    context['courses'] = courses
    
    if request.user.is_authenticated:
        context['sign_log'] = False
        context['loged_in'] = True
        
        return render(request, 'courses/courseHome.html', context)
    
    return render(request, 'courses/courseHome.html', context)


def TopicHome(request : HttpRequest, name : str, topic=None, comment=None) -> HttpResponse:
    context = {
        'sign_log': True,
    }

    course = Course.objects.get(name=name)
        
    topics = Topic.objects.filter(course=course)

    introduction_topic = topics.get(name='Introduction')
        
    if topic == None:
        top = topics.first()
        context['topic'] = top
    else:
        for top in topics:
            if top.id == topic:
                try:
                    top = topics.get(id=topic)
                    context['topic'] = top
                except Exception as e:
                    pass

    # Check if the Query is Wrong!

    # replies = None
    # if comment != None:
    #     replies = Comment.objects.filter(comment=comment)
    #     context['rcomments'] = replies
                
    if comment is not None:
        parent_comment = Comment.objects.filter(id=comment).first()
        if parent_comment:
            replies = Comment.objects.filter(parent_id=parent_comment.id)
            context['rcomments'] = replies

    comments = None
    if context['topic']:
        comments = Comment.objects.filter(topic=context['topic']).order_by('-timestamp')

    context['course'] = name
    context['topics'] = topics
    context['comments'] = comments
    context['introduction_topic'] = introduction_topic

    if request.user.is_authenticated:
        context['sign_log'] = False
        context['loged_in'] = True

        forms = CommentForm()

        rforms = ReplyCommentForm()

        context['forms'] = forms
        context['rforms'] = rforms

        return render(request, 'courses/topicHome.html', context)
    
    return render(request, 'courses/topicHome.html', context)

@login_required
def PostComment(request : HttpRequest, topic : int ) -> HttpResponse:
    if request.method == "POST":
        comment = CommentForm(request.POST)
        user = request.user
        top = Topic.objects.filter(id=topic).first()

        if comment.is_valid():
            content = comment.cleaned_data['content']

            cmt = Comment.objects.create(
                content = content,
                user = user,
                topic = top,
            )

            cmt.save()

            messages.success(request, "Comment Added!")
            return TopicHome(request, name=top.course.name, topic=top.id)

        messages.error(request, "Not Valid!")
        return TopicHome(request, name=top.course.name, topic=top.id)

def ReplyComment(request : HttpRequest, topic : int, comment : int) -> HttpResponse:
    if request.method == "POST":
        '''
            Will create an Comment object with Parent as the comment id, thus the new comment will be the an reply comment
        '''
        top = Topic.objects.filter(id = topic).first()

        course = Course.objects.filter(id = top.course.id).first()

        parent_comment = Comment.objects.filter(id = comment).first()

        content = request.POST['my_custom_name']
        
        comment = Comment.objects.create(
            content = content,
            user = request.user,
            topic = top,
            parent = parent_comment
        )

        comment.save()

        messages.success(request, "Reply Added Successfuly!")
        return HttpResponseRedirect(f'/courses/{course.name}/{topic}')
    