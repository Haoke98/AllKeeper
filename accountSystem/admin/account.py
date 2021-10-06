from django.contrib import admin
from django.utils.safestring import mark_safe

from accountSystem.models import Account
from izBasar.admin import LIST_DISPLAY


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['_name', '_username', '_password', '_url', '_info', 'type']
    list_display_links = ['id', '_name']
    date_hierarchy = 'updatedAt'
    search_fields = ['name', 'username', 'url', 'info']
    list_filter = ['group', 'type', 'tels', 'emails']
    list_select_related = ['group', 'type', 'password']
    autocomplete_fields = ['tels', 'emails', 'password', 'group', 'type']
    list_per_page = 10
    actions = ['actionTelAndEmailMigration']

    def _url(self, obj):
        tag = mark_safe('''
                    <a class="ui circular icon red button" href="%s" target="blank">
                        <i class="linkify icon"></i>
                    </a>
            ''' % obj.url)
        return tag

    _url.allow_tags = True

    def _info(self, obj):
        if obj.info:
            tag = mark_safe(
                '''<i class="circular info icon link" data-id="%s" data-title="%s"
                ></i>''' % (
                    obj.id, obj.name))
        else:
            tag = "-"
        return tag

    _url.allow_tags = True

    def _password(self, obj):
        tag = mark_safe(
            '''<div class="ui left labeled button" tabindex="0">
                    <div class="ui button">
                        <i class="eye icon"></i>
                    </div>
                    <a class="ui basic left pointing label">
                    ******
                    </a>
                    <div class="ui vertical animated button blue" onclick="copyStr('%s')" >
                        <div class="hidden content" style="color:white;" >复制</div>
                        <div class="visible content">
                                <i class="copy icon"></i>
                        </div>
                    </div>
                </div>''' % obj.password.password)
        return tag

    _password.allow_tags = True

    def _username(self, obj):
        tag = mark_safe(
            '''<div class="ui left labeled button" tabindex="0">
                    <a class="ui basic right pointing label" style="width:20em;">
                    %s
                    </a>
                    <div class="ui vertical animated button blue" onclick="copyStr('%s')" >
                        <div class="hidden content" style="color:white;" >1</div>
                        <div class="visible content">
                                <i class="copy icon"></i>
                        </div>
                    </div>
                </div>''' % (obj.username, obj.username))
        return tag

    _username.allow_tags = True

    def _name(self, obj):
        tag = mark_safe(
            '''<a class="ui teal tag label" style="width:20em;" onclick="goToDetail(this)">%s</a>''' % obj.name)
        return tag

    _name.allow_tags = True

    def actionTelAndEmailMigration(self, request, queryset):
        for obj in queryset:
            obj.tels.add(obj.tel)
            obj.emails.add(obj.email)
            obj.save()

    class Media:

        def __init__(self):
            pass

        css = {
            'all': ('Semantic-UI-CSS-master/semantic.css',)
        }
        js = [
            'kindeditor4.1.11/kindeditor-all.js',
            'kindeditor4.1.11/lang/zh-CN.js',
            'js/jquery-3.6.0.min.js',
            'js/config-account-admin.js',
            'Semantic-UI-CSS-master/semantic.js',
            'js/clipboardUtil.js',
            'bootstrap-3.4.1-dist/js/bootstrap.js'
        ]
