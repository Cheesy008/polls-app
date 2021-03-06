# Generated by Django 2.2.10 on 2021-09-16 10:17

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
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1, verbose_name='Номер')),
                ('text', models.TextField(verbose_name='Ответ')),
                ('votes_qty', models.PositiveIntegerField(default=0, verbose_name='Количество голосов')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('start_date', models.DateTimeField(verbose_name='Время начала опроса')),
                ('end_date', models.DateTimeField(verbose_name='Время окончания опроса')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polls', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1, verbose_name='Номер')),
                ('question_text', models.TextField(verbose_name='Текст вопроса')),
                ('question_type', models.CharField(choices=[('TE', 'Text'), ('SI', 'Single'), ('MU', 'Multiple')], default='SI', max_length=2)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.Poll', verbose_name='Опрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='UserPollResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='polls.Poll', verbose_name='Опрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_poll_responses', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Данные об опросе, на который отвечает пользователь',
                'verbose_name_plural': 'Данные об опросах, на которые отвечает пользователь',
            },
        ),
        migrations.CreateModel(
            name='UserQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True, verbose_name='Ответ в виде текста')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='polls.Question', verbose_name='Вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_question_responses', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('user_poll_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.UserPollResponse', verbose_name='Опрос пользователя')),
            ],
            options={
                'verbose_name': 'Данные о вопросе, на который отвечает пользователь',
                'verbose_name_plural': 'Данные о вопросах, на которые отвечает пользователь',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='polls.Answer', verbose_name='Ответ из предоставленных вариантов')),
                ('user_question_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.UserQuestionResponse', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователя',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.Question', verbose_name='Вопрос'),
        ),
    ]
