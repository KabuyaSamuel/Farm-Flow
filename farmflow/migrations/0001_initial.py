# Generated by Django 4.2 on 2023-05-20 14:18

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CropProductionStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planted_date', models.DateField()),
                ('harvested_date', models.DateField()),
                ('ploughing', models.DateField()),
                ('weeding', models.DateField()),
                ('harvesting', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=55)),
                ('length', models.PositiveIntegerField(default=0)),
                ('width', models.PositiveIntegerField(default=0)),
                ('is_leased', models.BooleanField(default=False)),
                ('approval_status', models.CharField(choices=[('Pending', 'Pending Approval'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FarmingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Outdoor', 'Outdoor'), ('Greenhouse', 'Greenhouse')], max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FarmInputUsed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_used', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('date_used', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='InputUsed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Fertilizer', 'Fertilizer'), ('Pesticides', 'Pesticides')], max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.CharField(choices=[('kg', 'kg'), ('litres', 'litres')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Produce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('grade', models.CharField(choices=[('Grade A', 'Grade A'), ('Grade B', 'Grade B'), ('Grade C', 'Grade C')], max_length=255)),
                ('production_date', models.DateField()),
                ('status', models.CharField(choices=[('Harvested', 'Harvested'), ('In Transit', 'In Transit'), ('At the Market', 'At the Market'), ('Sold', 'Sold')], max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProducerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('avatar', cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/fevercode/image/upload/v1654534329/default_n0r7rf.png', max_length=255, verbose_name='image')),
                ('bio', models.TextField(default='This is my bio', max_length=500)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=255)),
                ('id_number', models.PositiveBigIntegerField(blank=True, null=True, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('plot_size', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SoilTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Complete', 'Complete'), ('Partial', 'Partial')], max_length=255)),
                ('done', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], max_length=255)),
                ('reason', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ValueChainChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Poultry', 'Poultry'), ('Vegetable', 'Vegetable'), ('Herbs', 'Herbs'), ('Dairy', 'Dairy')], max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Borehole', 'Borehole'), ('River', 'River'), ('Dam', 'Dam'), ('Rain', 'Rain'), ('Swamp', 'Swamp'), ('Other', 'other')], max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.CharField(editable=False, max_length=36, unique=True)),
                ('status', models.CharField(default='Harvested', max_length=50)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.profile')),
                ('produce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.produce')),
            ],
        ),
        migrations.AddConstraint(
            model_name='soiltestresult',
            constraint=models.UniqueConstraint(fields=('type', 'done'), name='unique_test_result'),
        ),
        migrations.AddConstraint(
            model_name='soiltestresult',
            constraint=models.CheckConstraint(check=models.Q(('done', 'Y'), models.Q(('done', 'N'), _negated=True), models.Q(('reason', ''), _negated=True), _connector='OR'), name='reason_required_for_no'),
        ),
        migrations.AddField(
            model_name='profile',
            name='farm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='farmflow.farm'),
        ),
        migrations.AddField(
            model_name='profile',
            name='producer_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='farmflow.producergroup'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='producergroup',
            name='cluster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.cluster'),
        ),
        migrations.AddField(
            model_name='producergroup',
            name='members',
            field=models.ManyToManyField(related_name='producer_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='produce',
            name='farmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.profile'),
        ),
        migrations.AddField(
            model_name='produce',
            name='value_chain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.valuechainchoice'),
        ),
        migrations.AddField(
            model_name='inputused',
            name='farms',
            field=models.ManyToManyField(through='farmflow.FarmInputUsed', to='farmflow.farm'),
        ),
        migrations.AddField(
            model_name='inputused',
            name='value_chain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.valuechainchoice'),
        ),
        migrations.AddField(
            model_name='farminputused',
            name='crop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.crop'),
        ),
        migrations.AddField(
            model_name='farminputused',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.farm'),
        ),
        migrations.AddField(
            model_name='farminputused',
            name='input_used',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.inputused'),
        ),
        migrations.AddField(
            model_name='farm',
            name='crops',
            field=models.ManyToManyField(blank=True, related_name='crops', to='farmflow.crop'),
        ),
        migrations.AddField(
            model_name='farm',
            name='farming_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.farmingtype'),
        ),
        migrations.AddField(
            model_name='farm',
            name='input_used',
            field=models.ManyToManyField(through='farmflow.FarmInputUsed', to='farmflow.inputused'),
        ),
        migrations.AddField(
            model_name='farm',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farmer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='farm',
            name='soil_test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.soiltestresult'),
        ),
        migrations.AddField(
            model_name='farm',
            name='value_chains',
            field=models.ManyToManyField(blank=True, to='farmflow.valuechainchoice'),
        ),
        migrations.AddField(
            model_name='farm',
            name='water_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.watersource'),
        ),
        migrations.AddField(
            model_name='cropproductionstage',
            name='crop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.crop'),
        ),
        migrations.AddField(
            model_name='cropproductionstage',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.farm'),
        ),
        migrations.AddField(
            model_name='cropproductionstage',
            name='inputs',
            field=models.ManyToManyField(blank=True, to='farmflow.inputused'),
        ),
        migrations.AddField(
            model_name='crop',
            name='value_chain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmflow.valuechainchoice'),
        ),
    ]
