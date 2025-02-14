from django.contrib import admin

# Register your models here.
from .models import Archivo, Analisis, Vulnerabilidad,NuevaVulnerabilidad, Archivo_Usuario, Analisis_Usuario, Deteccion,DeteccionExp, Expresion, RequiereExpresion, Foro, Post, MensajesPost
from reversion.admin import VersionAdmin

@admin.register(Archivo)
class YourModelAdmin(VersionAdmin):
	list_display = ('titulo_archivo','archivo','extension', 'framework')
	def file_link(self, obj):
		if obj.file:
			return "<a href='%s' download>Download</a>" % (obj.file.url,)
		else:
			return "No attachment"
	file_link.allow_tags = True
	file_link.short_description = 'File Download'
	pass


class AdminAnalisis(admin.ModelAdmin):
    list_display = ('titulo_analisis','analisis','version', 'fecha')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminVulnerabilidad(admin.ModelAdmin):
    list_display = ('cve','cwe_id','source', 'cwe_name', 'base_score', 'type_attack')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminArchivo_Usuario(admin.ModelAdmin):
    list_display = ('id_archivo', 'titulo_archivo','usuario')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminAnalisis_Usuario(admin.ModelAdmin):
    list_display = ('titulo_analisis','titulo_archivo','usuario')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'


class AdminDeteccion(admin.ModelAdmin):
    list_display = ('id_deteccion', 'vulnerabilidad', 'titulo_analisis', 'fecha')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminDeteccionExp(admin.ModelAdmin):
    list_display = ('id_deteccion', 'expresion', 'titulo_analisis', 'fecha')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminExpresion(admin.ModelAdmin):
    list_display = ('id_expresion','nombre_expresion','vulnerabilidad', 'tipo')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminRequiereExpresion(admin.ModelAdmin):
    list_display = ('nombre_requisito','expresion_primaria','expresion_requerida', 'tipo_requisito')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'


class AdminNuevaVulnerabilidad(admin.ModelAdmin):
    list_display = ('usuario','cve','descripcion')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminForo(admin.ModelAdmin):
    list_display = ('usuario','post_id')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'


class AdminPost(admin.ModelAdmin):
    list_display = ('post','titulo','fecha')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'

class AdminMensajesPost(admin.ModelAdmin):
    list_display = ('post','usuario','fecha')
    def file_link(self, obj):
        if obj.file:
            return "<a href='%s' download>Download</a>" % (obj.file.url,)
        else:
            return "No attachment"
    file_link.allow_tags = True
    file_link.short_description = 'File Download'


admin.site.register(Vulnerabilidad, AdminVulnerabilidad )
admin.site.register(Archivo_Usuario, AdminArchivo_Usuario)
admin.site.register(Analisis_Usuario, AdminAnalisis_Usuario)
admin.site.register(Deteccion, AdminDeteccion)
admin.site.register(DeteccionExp, AdminDeteccionExp)

admin.site.register(Expresion, AdminExpresion)
admin.site.register(RequiereExpresion, AdminRequiereExpresion)
admin.site.register(NuevaVulnerabilidad, AdminNuevaVulnerabilidad)
admin.site.register(Foro, AdminForo)
admin.site.register(Post, AdminPost)
admin.site.register(MensajesPost, AdminMensajesPost)
admin.site.register(Analisis , AdminAnalisis)



