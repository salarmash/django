from django.contrib import admin
from django.contrib.auth.models import User
from .models import Score, MatchDay, Match, Rule, UserForcastHistory, UserForcast
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Score)


class MatchAdmin(admin.StackedInline):
    model = Match


@admin.register(MatchDay)
class MatchDayAdmin(admin.ModelAdmin):
    inlines = [MatchAdmin]


class RulAdmin(SummernoteModelAdmin):
    summernote_fields = ("body",)


admin.site.register(Rule, RulAdmin)
admin.site.register(UserForcastHistory)
admin.site.register(UserForcast)
