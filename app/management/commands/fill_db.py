from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import time
import random

fake = Faker()
class Command(BaseCommand):
    help = "Create random user"

    def add_arguments(self, parser):
        parser.add_argument('param', type=int)

    def create_users(self, ratio):
        faker = Faker()
        start_time = time.time()
        auth_users = User.objects.bulk_create(
            [User(username=faker.user_name(), email=f'user{i}@mail.ru', password=f'password{i}') for i in range(ratio)])

        users = Profile.objects.bulk_create([Profile(user=auth_users[i]) for i in range(ratio)])
        tags = Tag.objects.bulk_create([Tag(tag=f"tag{i}") for i in range(ratio)])

        for i in range(ratio * 10):
            title = f'title {i}'
            content = f'Content {i}'
            user = users[random.randrange(1, ratio)]
            question = Question(title=title, content=content, user=user)
            question.save()
            tag_id = random.randrange(0, ratio - 2)
            question.tags.add(tags[tag_id])
            question.tags.add(tags[tag_id+1])
            question.tags.add(tags[tag_id+2])

        counter = 0
        for q in Question.objects.all():
            Answer.objects.bulk_create([Answer(content=f"{counter + i} answer",
                                               question=q, user=users[random.randint(0, ratio - 1)]) for i in range(10)])
            counter += 10

        questions = Question.objects.all()
        step = ratio//10
        for i in range(ratio):
            u = users[i]
            LikeQuestion.objects.bulk_create([LikeQuestion(positive=random.randint(0, 1), user=u, question=questions[
                random.randint(step * j, step * (j + 1) - 1)]) for j in range(100)])
        for q in questions:
            like = q.like_model
            for j in like.all():
                if j.positive == 1:
                    q.rating += 1
                else:
                    q.rating -= 1
            q.save()
        answers = Answer.objects.all()
        for i in range(ratio):
            u = users[i]
            LikeAnswer.objects.bulk_create([LikeAnswer(positive=random.randint(0, 1), user=users[i],
                                             answer=answers[random.randint(ratio * j, ratio * (j + 1) - 1)]) for j in
                                  range(100)])
        for a in answers:
            like = a.like_model
            for j in like.all():
                if j.positive == 1:
                    a.rating += 1
                else:
                    a.rating -= 1
            a.save()
        print('OK')
        print("--- %s seconds ---" % (time.time() - start_time))



    def handle(self, *args, **kwargs):
        ratio = kwargs.get('param')
        self.create_users(ratio)
        print('OK')



# 17  и 152
# 9.5 и 95.5
