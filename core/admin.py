from django.contrib import admin
from .models import Directory, Document, CommonDocument, DirectoryAccess

admin.site.register(Directory)
admin.site.register(Document)
admin.site.register(CommonDocument)
admin.site.register(DirectoryAccess)