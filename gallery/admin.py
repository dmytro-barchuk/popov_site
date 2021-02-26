from django.contrib import admin
from .models import Post, Tag
from datetime import datetime


class PostAdmin(admin.ModelAdmin):
	# list_filter = ('created', )
	# search_fields = ('title', 'body')
	date_hierarchy = 'created'
	ordering = ('created', )

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)