from django.contrib import admin
from .models import Notice, CommitteeMember, GalleryImage

# Registering the Notice model with a custom admin class
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'pdf_file')
    search_fields = ('title',)

# Registering the GalleryImage model
admin.site.register(GalleryImage)

# Custom admin configuration for CommitteeMember
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ['serial_no', 'name', 'position', 'email', 'mobile']
    list_editable = ['serial_no']
    ordering = ['serial_no']
    list_display_links = ['name']  # Set a clickable field, for example, 'name'

# Registering the CommitteeMember model with the custom admin class
admin.site.register(CommitteeMember, CommitteeMemberAdmin)
