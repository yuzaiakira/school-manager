from django import template
register = template.Library()


# @register.filter
# def show_display_group_name(value):
#     if group_name_status[value] in group_name_status:
#         return group_name_status[value][1]
#     else:
#         return 'گروه نامعتبر'


@register.filter
def show_boolean_value(value):
    if value:
        return 'بله'
    else:
        return 'خیر'
