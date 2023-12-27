from simplepro.admin import BaseAdmin, FieldOptions


class BaseAccountAdmin(BaseAdmin):
    list_display = ['id', 'group', 'username', 'pwd', 'remark', 'info']
    date_hierarchy = 'updatedAt'
    search_fields = ['group', 'username', 'pwd', 'remark', 'info']
    list_filter = ['group']
    list_select_related = ['group', 'wechat']
    autocomplete_fields = ['group']
    list_per_page = 8
    actions = []

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "username":
            if value:
                return BaseAdmin.username(obj.username)
        if field_name == 'pwd':
            if value:
                return BaseAdmin.password(obj.pwd)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'platform': {
            'width': '200px',
            'align': 'left'
        },
        'username': FieldOptions.USER_NAME,
        'pwd': FieldOptions.PASSWORD,
        'url': {
            'width': '130px',
            'align': 'center'
        },
        '_tels': {
            'width': '180px',
            'align': 'left'
        },
        '_emails': {
            'width': '200px',
            'align': 'left'
        },
        'wechat': {
            'width': '120px',
            'align': 'left'
        },

        'info': {
            'width': '180px',
            'align': 'left'
        },
        'name': {
            'width': '200px',
            'align': 'center'
        },
        'createdUserRecordName': {
            'width': '300px',
            'align': 'left'
        },
        'modifiedUserRecordName': {
            'width': '300px',
            'align': 'left'
        },
        'createdDeviceID': {
            'width': '400px',
            'align': 'left'
        },
        'modifiedDeviceID': {
            'width': '400px',
            'align': 'left'
        },
        'locationEnc': {
            'width': '1000px',
            'align': 'left'
        },
    }
