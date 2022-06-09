# Generated by Django 3.0.4 on 2022-05-29 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220522_2309'),
        ('chat', '0002_chat_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='slug',
            field=models.SlugField(blank=True, max_length=12, null=True),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.Chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
    ]
