from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'age',
        'gender',
        'predicted_disease',
        'confidence',
        'created_at'
    )


    search_fields = ('name', 'predicted_disease')


    list_filter = ('gender', 'predicted_disease', 'created_at')

    ordering = ('-created_at',)

    readonly_fields = (
        'predicted_disease',
        'confidence',
        'created_at'
    )