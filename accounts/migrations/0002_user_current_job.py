from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="current_job",
            field=models.CharField(
                blank=True,
                help_text="Current job or profession",
                max_length=150,
            ),
        ),
    ]
