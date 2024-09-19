from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('key', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('value', models.TextField()),
            ],
        ),
    ]
