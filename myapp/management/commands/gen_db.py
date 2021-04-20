from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from random import choice, sample, randint
from faker import Faker

f = Faker()


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--users", nargs="+", type=int)
        parser.add_argument("--questions", nargs="+", type=int)
        parser.add_argument("--answers", nargs="+", type=int)
        parser.add_argument("--tags", nargs="+", type=int)
        parser.add_argument("--likes", nargs="+", type=int)
        parser.add_argument("--ulikes", nargs="+", type=int)

        parser.add_argument("--db_size", nargs="+", type=str)

        parser.add_argument("--dusers", nargs="+", type=int)
        parser.add_argument("--dlikes", nargs="+", type=int)
        parser.add_argument("--dtags", nargs="+", type=int)
        parser.add_argument("--danswers", nargs="+", type=int)
        parser.add_argument("--dquestions", nargs="+", type=int)
        parser.add_argument("--dall", nargs="+", type=int)

    def handle(self, *args, **options):
        if options["users"]:
            self.fill_profile(options["users"][0])

        if options["tags"]:
            self.fill_tag(options["tags"][0])

        if options["questions"]:
            self.fill_questions(options["questions"][0])

        if options["answers"]:
            self.fill_answers(options["answers"][0])

        if options["likes"]:
            self.fill_likes_questions(1000000)
            self.fill_likes_answers(2000000)

        if options["dusers"]:
            self.delete_users()

        if options["dlikes"]:
            self.delete_likes()

        if options["dtags"]:
            self.delete_tags()

        if options["danswers"]:
            self.delete_answers()

        if options["dquestions"]:
            self.delete_questions()

        if options["ulikes"]:
            self.update_likes()

        if options["dall"]:
            self.delete_all()

        self.stdout.write(self.style.SUCCESS("Successfully closed poll "))

    @staticmethod
    def fill_profile(cnt):
        for i in range(cnt):
            name = f.user_name()
            while User.objects.filter(username=name).exists():
                name = f.user_name()
            Profile.objects.create(
                user=User.objects.create(username=name, email=f.email(), password=f.password(length=8, digits=True)),
                avatar="img/star.jpeg",
            )

    @staticmethod
    def fill_tag(cnt):
        for i in range(cnt):
            tag = f.word()
            while Tag.objects.filter(name=tag).exists():
                tag = f.word() + f.word()
            Tag.objects.create(
                name=tag,
            )

    @staticmethod
    def fill_questions(cnt):
        tag_ids = list(Tag.objects.values_list("id", flat=True))
        for profile in Profile.objects.all():
            for i in range(10):
                q = Question.objects.create(
                    author=profile,
                    title=f.sentence(),
                    text=f.text(),
                )
                q.tags.set(Tag.objects.filter(id__in=sample(tag_ids, k=randint(1, 3)))),

    @staticmethod
    def fill_answers(cnt):
        profile_ids = list(Profile.objects.values_list("id", flat=True))
        question_ids = list(Question.objects.values_list("id", flat=True))
        tag_ids = list(Tag.objects.values_list("id", flat=True))
        for i in range(cnt):
            a = Answer.objects.create(
                author=Profile.objects.get(pk=choice(profile_ids)),
                question=Question.objects.get(pk=choice(question_ids)),
                text=f.text(),
            )
            a.tags.set(Tag.objects.filter(id__in=sample(tag_ids, k=randint(1, 3)))),

    @staticmethod
    def fill_likes_questions(cnt):
        profile_ids = list(Profile.objects.values_list("id", flat=True))
        count = 0
        for cur_question in Question.objects.all():
            for profile in Profile.objects.filter(id__in=sample(profile_ids, k=randint(0, 20))):
                LikeQuestion.objects.create(
                    question=cur_question,
                    user=profile,
                )
                count += 1
                if count == cnt:
                    break
            if count == cnt:
                break

    @staticmethod
    def fill_likes_answers(cnt):
        profile_ids = list(Profile.objects.values_list("id", flat=True))
        count = 0
        for cur_answer in Answer.objects.all():
            for profile in Profile.objects.filter(id__in=sample(profile_ids, k=randint(0, 20))):
                LikeAnswer.objects.create(
                    answer=cur_answer,
                    user=profile,
                )
                count += 1
                if count == cnt:
                    break
            if count == cnt:
                break

    @staticmethod
    def delete_users():
        Profile.objects.all().delete()
        User.objects.all().delete()

    @staticmethod
    def delete_tags():
        Tag.objects.all().delete()

    @staticmethod
    def delete_likes():
        LikeQuestion.objects.all().delete()
        LikeAnswer.objects.all().delete()

    @staticmethod
    def delete_answers():
        Answer.objects.all().delete()

    @staticmethod
    def delete_questions():
        Question.objects.all().delete()

    @staticmethod
    def delete_all():
        Profile.objects.all().delete()
        User.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Tag.objects.all().delete()
        LikeQuestion.objects.all().delete()
        LikeAnswer.objects.all().delete()

    @staticmethod
    def update_likes():
        questions = list(Question.objects.values_list("id", flat=True))
        for q in questions:
            answers_of_question = list(Answer.objects.filter(question_id=q).order_by("-rating"))
            question = Question.objects.get(pk=q)
            question.answers_number = len(answers_of_question)
