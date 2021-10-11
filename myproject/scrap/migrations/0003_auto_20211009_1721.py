# Generated by Django 3.2.8 on 2021-10-09 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0002_electivesgroup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='college',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='electivesgroup',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='college',
            name='courdiv',
            field=models.ManyToManyField(related_name='colleges', to='scrap.Courdiv'),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='scrap.college')),
                ('courdiv', models.ManyToManyField(related_name='departments', to='scrap.Courdiv')),
            ],
        ),
    ]