import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Уникальный код королевства')),
            ],
            options={
                'verbose_name': 'Королевство',
                'verbose_name_plural': 'Королевства',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Вопрос')),
                ('answer_options', models.JSONField(verbose_name='Варианты ответа')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='King',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('kingdom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.kingdom', verbose_name='Королевство')),
            ],
            options={
                'verbose_name': 'Король',
                'verbose_name_plural': 'Короли',
            },
        ),
        migrations.CreateModel(
            name='CandidateTestTrial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_test', models.CharField(max_length=255, verbose_name='Имя теста')),
                ('kingdom_code', models.CharField(max_length=255, unique=True, verbose_name='Уникальный код королевства')),
                ('kingdom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.kingdom', verbose_name='Королевство')),
                ('questions', models.ManyToManyField(to='app.question', verbose_name='Список вопросов')),
            ],
            options={
                'verbose_name': 'Тестовое испытание кандидата',
                'verbose_name_plural': 'Тестовые испытания кандидатов',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('email', models.CharField(max_length=255, unique=True, verbose_name='Голубь (email)')),
                ('status', models.CharField(choices=[('Enrolled', 'Зачислен'), ('Not enrolled', 'Не зачислен')], default='Not enrolled', null=True, verbose_name='Статус зачисления')),
                ('king', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='app.king', verbose_name='Король')),
                ('kingdom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.kingdom', verbose_name='Королевство')),
            ],
            options={
                'verbose_name': 'Подданный',
                'verbose_name_plural': 'Подданные',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_name='app_user_groups', to='auth.group', verbose_name='')),
                ('subject_permissions', models.ManyToManyField(related_name='app_user_permissions', to='auth.permission')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('king', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.king', verbose_name='Король')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subject', verbose_name='Подданный')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.JSONField(null=True, verbose_name='Выбранные ответы')),
                ('status', models.CharField(choices=[('Solved', 'Решенный'), ('Not solved', 'Не решенный')], default='Not solved', null=True, verbose_name='Статус теста')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatetesttrial', verbose_name='Тестовое задание')),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='test_case',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.testcase', verbose_name='Тест кандидата'),
        )
    ]
