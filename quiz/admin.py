from django.contrib import admin
from .models import Question, Option, Attempt, Round, Phase ,BzrAttempt

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'round', 'category', 'options']
    search_fields = ['title']
    list_filter = ['category', 'round', 'type']

    def options(self, obj):
        return "\n| ".join([option.title for option in obj.option_set.all()])
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Attempt)
admin.site.register(Round)
admin.site.register(Phase)
admin.site.register(BzrAttempt)
