# Generated by Django 3.2 on 2021-05-08 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulos', '0003_populando_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulo',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='modulo',
            name='publico',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='modulo',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]