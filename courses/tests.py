from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from courses.views import CoursesHome, TopicHome, PostComment, ReplyComment
from courses.models import Course, Topic
from core.models import Comment

class CoursesViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username='testuser', password='12345')

        self.course = Course.objects.create(name='Test Course', description='Test Description')

        self.topic = Topic.objects.create(name='Test Topic', course=self.course)

    def test_courses_home_view(self):
        request = self.factory.get(reverse('courses_home'))
        request.user = self.user

        response = CoursesHome(request)

        self.assertEqual(response.status_code, 200)
        print('Test Case 2 Ran Successfuly...')

    def test_topic_home_view(self):
        request = self.factory.get(reverse('topic_home', kwargs={'name': self.course.name}))
        request.user = self.user

        response = TopicHome(request, name=self.course.name)
        
        self.assertEqual(response.status_code, 200)
        print('Test Case 3 Ran Successfuly...')

    def test_post_comment_view(self):
        request = self.factory.post(reverse('post_comment', kwargs={'topic': self.topic.id}), {'content': 'Test Content'})
        request.user = self.user
        
        response = PostComment(request, topic=self.topic.id)
        
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after posting comment
        print('Test Case 4 Ran Successfuly...')

    def test_reply_comment_view(self):
        parent_comment = Comment.objects.create(content='Parent Comment', user=self.user, topic=self.topic)
        
        request = self.factory.post(reverse('reply_comment', kwargs={'topic': self.topic.id, 'comment': parent_comment.id}), {'my_custom_name': 'Reply Content'})
        request.user = self.user
        
        response = ReplyComment(request, topic=self.topic.id, comment=parent_comment.id)
        
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after replying
        print('Test Case 5 Ran Successfuly...')
