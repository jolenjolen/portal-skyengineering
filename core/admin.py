# author: Jolen Mascarenhas (w2078969)
from django.contrib import admin
from .models import TblUser, TblTeam, TblDepartment, TblProject, TblDependencies, TblAudit

admin.site.register(TblUser)
admin.site.register(TblTeam)
admin.site.register(TblDepartment)
admin.site.register(TblProject)
admin.site.register(TblDependencies)
admin.site.register(TblAudit)