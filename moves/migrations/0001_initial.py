# Generated by Django 5.0.4 on 2024-04-27 09:36

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "number_of_sides",
                    models.PositiveIntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(3),
                        ],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Move",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "player",
                    models.CharField(
                        choices=[("X", "Player X"), ("O", "Player O")], max_length=1
                    ),
                ),
                (
                    "row",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
                (
                    "column",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="moves.game"
                    ),
                ),
            ],
            options={
                "db_table": "moves",
            },
        ),
        migrations.AddConstraint(
            model_name="move",
            constraint=models.UniqueConstraint(
                fields=("game", "row", "column"), name="unique_position_for_game"
            ),
        ),
    ]
