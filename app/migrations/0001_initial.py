# Generated by Django 4.2.16 on 2024-11-03 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("likes_count", models.IntegerField(default=0)),
            ],
            options={
                "ordering": ["likes_count"],
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars/"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("likes_count", models.IntegerField(default=0)),
                ("answers_number", models.IntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="questions",
                        to="app.profile",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(related_name="questions", to="app.tag"),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AnswerLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_likes",
                        to="app.answer",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.profile"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="answer",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="answers",
                to="app.profile",
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="app.question",
            ),
        ),
        migrations.CreateModel(
            name="QuestionLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="question_likes",
                        to="app.question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.profile"
                    ),
                ),
            ],
            options={
                "unique_together": {("question", "user")},
            },
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(
                fields=["created_at"], name="app_questio_created_eedfc6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(
                fields=["likes_count"], name="app_questio_likes_c_1d2fa4_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="answerlike",
            unique_together={("answer", "user")},
        ),
        migrations.AddIndex(
            model_name="answer",
            index=models.Index(
                fields=["created_at"], name="app_answer_created_9a6840_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="answer",
            index=models.Index(
                fields=["likes_count"], name="app_answer_likes_c_469dd5_idx"
            ),
        ),
    ]
