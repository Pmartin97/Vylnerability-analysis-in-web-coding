# Generated by Django 2.2.12 on 2020-06-16 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vulnerabilidad',
            name='scope',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='archivo',
            name='framework',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('html', 'HTML'), ('nodejs', 'Nodejs'), ('react', 'React')], default='unknown', help_text='Select the framework', max_length=20),
        ),
        migrations.AlterField(
            model_name='expresion',
            name='tipo',
            field=models.CharField(choices=[('busqueda', 'Busqueda'), ('uso_de_variable', 'Uso de variable'), ('variable', 'Variable')], default='busqueda', help_text='Seleccione el tipo de expresion', max_length=20),
        ),
        migrations.AlterField(
            model_name='requiereexpresion',
            name='tipo_requisito',
            field=models.CharField(choices=[('busqueda', 'Busqueda'), ('uso_de_variable', 'Uso de variable'), ('variable', 'Variable')], default='busqueda', help_text='Seleccione el tipo de expresion', max_length=20),
        ),
        migrations.AlterField(
            model_name='vulnerabilidad',
            name='clase_vulnerabilidad',
            field=models.CharField(choices=[('terceros', 'Terceros'), ('acciones', 'Acciones')], default='terceros', help_text='Seleccione la clase de vulnerabilidad', max_length=10),
        ),
        migrations.AlterField(
            model_name='vulnerabilidad',
            name='framework',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('html', 'HTML'), ('nodejs', 'Nodejs'), ('react', 'React')], default='html', help_text='Select the framework', max_length=20),
        ),
    ]
