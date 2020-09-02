# Generated by Django 3.0.8 on 2020-08-30 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20200830_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='date_released',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='ImageLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_img_name', models.CharField(max_length=200)),
                ('content_img', models.URLField(verbose_name='Content Image URL')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='content.Project')),
            ],
        ),
    ]