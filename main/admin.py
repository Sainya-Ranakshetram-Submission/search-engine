from django.contrib import admin, messages
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import ngettext


@admin.register(CrawledWebPages)
class CrawledWebPagesAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "http_status",
        "uses",
        "ip_address",
        "sitemap_filepath",
        "robot_txt_filepath",
        "last_crawled"
    )
    
    list_filter = ('last_crawled',)
    readonly_fields = (
        'uses',
        'keywords_meta_tags',
        'keywords_in_site',
        'stripped_request_body',
        'keywords_ranking',
        'last_crawled'
    )
    
    search_fields = list_display+list_filter
    list_per_page = 34
    fieldsets = (
        (_("Url"), {"fields": ("url",)}),
        (_('Rank'), {"fields": ("uses",)}),
        (_('Status'), {'fields': ("http_status",)}),
        (_('Crawl File Path'), {'fields': ("sitemap_filepath", "robot_txt_filepath", "scan_internal_links")}),
        (_('Request Body'), {'fields': ('keywords_meta_tags', 'keywords_in_site', 'stripped_request_body', 'keywords_ranking')}),
        (_('Last Crawled'), {'fields': ('last_crawled',)})
    )

@admin.register(ToBeCrawledWebPages)
class ToBeCrawledWebPagesAdmin(admin.ModelAdmin):
    list_per_page = 34
    list_display = ('url', 'http_status', 'last_crawled')
    list_filter=list_display[-1:]
    readonly_fields = list_display[1:]
    fieldsets = (
        (_("Url"), {"fields": ("url",)}),
        (_('Status'), {'fields': ("http_status",)}),
        (_('Last Crawled'), {'fields': ('last_crawled',)})
    )
    

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def delete_admin_logs(self, request, queryset):
        querysetmsg = queryset.delete()

        self.message_user(
            request,
            ngettext(
                "%d log was successfully deleted.",
                "%d logs were successfully deleted.",
                len(queryset),
            )
            % int(len(queryset)),
            messages.SUCCESS,
        )

    delete_admin_logs.short_description = (
        "Delete the selected ADMIN Logs without sticking"
    )

    actions = [delete_admin_logs]


admin.site.unregister(Group)
admin.site.site_header = admin.site.site_title = "Konohagakure Search"

