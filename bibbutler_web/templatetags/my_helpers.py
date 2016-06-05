from django import template

register = template.Library()


@register.simple_tag
def get_verbose_name(object):
    return object._meta.verbose_name


@register.simple_tag
def get_fields(object):
    return object._meta.get_fields()


@register.simple_tag
def get_fields_without_id_and_relations(object):
    blacklist = ('id', 'polymorphic_ctype_id', 'bibliography_id', 'entry_ptr_id')
    fields = get_fields(object)
    return [field for field in fields if field.attname not in blacklist]