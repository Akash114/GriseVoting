from django.contrib import admin
# Register your models here.
from .models import Question, Choice,UserInfo
from django.contrib.auth.models import Group,User


admin.site.site_header = "Grise Admin"
admin.site.site_title = "Grise Poll Admin Area"
admin.site.index_title = "Welcome to the Grise Poller Admin Area"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {
        'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('question','selected_choice','address')


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
