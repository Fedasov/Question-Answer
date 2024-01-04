from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def top_tag_questions(self, tag):
        question = Question.objects.filter(tags=tag.id)
        return question.annotate(answer_count=Count('answer')).order_by('-date_writen')
    def new_question(self):
        return self.annotate(answer_count=Count('answer')).order_by('-date_writen')
    def hot_question(self):
        hot = self.annotate(answer_count=Count('answer')).order_by('-rating')
        return hot

class AnswerManager(models.Manager):
    def answer_question(self, question_id):
        answers = self.filter(question__id=question_id).annotate(like_count=Count('like')).order_by('-like_count')
        return answers

class LikeQuestionManager(models.Manager):
    def toggle_like(self, user, question):
        if self.filter(user=user, question=question).exists():
            like = self.get(user=user, question=question)
            if like.positive:       # like
                question.rating -= 1
                self.filter(user=user, question=question).delete()
            else:                           # dislike
                like.positive = True
                print(like)
                like.save()
                question.rating += 2
        else:
            question.rating += 1
            self.create(user=user, question=question, positive=True)
        question.save()
    def toggle_dislike(self, user, question):
        if self.filter(user=user, question=question).exists():
            like = self.get(user=user, question=question)
            if like.positive:       # like
                like.positive = False
                like.save()
                question.rating -= 2
            else:                           # dislike
                question.rating += 1
                self.filter(user=user, question=question).delete()
        else:
            question.rating -= 1
            self.create(user=user, question=question, positive=False)
        question.save()

class LikeAnswerManager(models.Manager):
    def toggle_like(self, user, answer):
        if self.filter(user=user, answer=answer).exists():
            like = self.get(user=user, answer=answer)
            if like.positive:  # like
                answer.rating -= 1
                self.filter(user=user, answer=answer).delete()
            else:  # dislike
                like.positive = True
                like.save()
                answer.rating += 2
        else:
            answer.rating += 1
            self.create(user=user, answer=answer, positive=True)
        answer.save()

    def toggle_dislike(self, user, answer):
        if self.filter(user=user, answer=answer).exists():
            like = self.get(user=user, answer=answer)
            if like.positive:  # like
                like.positive = False
                like.save()
                answer.rating -= 2
            else:  # dislike
                answer.rating += 1
                self.filter(user=user, answer=answer).delete()
        else:
            answer.rating -= 1
            self.create(user=user, answer=answer, positive=False)
        answer.save()


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    date_writen = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey('Profile', max_length=256, on_delete=models.PROTECT)
    like = models.ManyToManyField('Profile', through="LikeQuestion", related_name="question_likes", related_query_name="question_like")

    objects = QuestionManager()
    def __str__(self):
        return f"{self.title} {self.date_writen}"

class LikeQuestion(models.Model):
    positive = models.BooleanField()
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='like_question')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='like_model')
    objects = LikeQuestionManager()

    class Meta:
        unique_together = ('user', 'question',)

class Answer(models.Model):
    content = models.TextField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.PROTECT, null=True, related_query_name="answer")  # точно
    user = models.ForeignKey('Profile', on_delete=models.PROTECT)
    like = models.ManyToManyField('Profile', through="LikeAnswer", related_name="answer_likes",
                                  related_query_name="answer_like")

    objects = AnswerManager()
    def __str__(self):
        return f"{self.content}"

class LikeAnswer(models.Model):
    positive = models.BooleanField()
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='like_answer')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='like_model')

    objects = LikeAnswerManager()

    class Meta:
        unique_together = ('user', 'answer',)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="Default.png", upload_to="images/")
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()
    def __str__(self):
        return f"{self.user}"

class Tag(models.Model):
    tag = models.CharField(max_length=256)

    objects = models.Manager()
    def __str__(self):
        return f"{self.tag}"