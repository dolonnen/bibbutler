from django import template
from bibbutler_web.models.entry import entry_types

register = template.Library()


@register.simple_tag
def get_class_verbose_name(object):
    return object._meta.verbose_name


@register.simple_tag
def get_fields(object):
    return object._meta.get_fields()


@register.simple_tag
def get_fields_without_id_and_relations(object):
    blacklist = ('id', 'polymorphic_ctype_id', 'bibliography_id', 'entry_ptr_id')
    fields = get_fields(object)
    return [field for field in fields if field.attname not in blacklist]


@register.inclusion_tag('bibbutler_web/modal_entry_type.html')
def load_modal_entry_type(bib_id):
    return {'entry_types': entry_types,
            'bib_id': bib_id}


@register.inclusion_tag('bibbutler_web/modal_delete_entry.html')
def load_modal_delete_entry(entry_id):
    return {'entry_id': entry_id}