from django.contrib import admin



from .models import Team, Category
admin.site.register(Category)
# admin.site.register(Team)

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'get_participants']
    list_filter = ['name', 'category']
    search_fields = ['name', 'category']

    def get_participants(self, obj):
        return "\n| ".join([p.username for p in obj.participants.all()])

admin.site.register(Team, TeamAdmin)