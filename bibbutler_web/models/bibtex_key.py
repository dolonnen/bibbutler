def get_namelist(entry):
    try:
        entry.author
    except AttributeError:
        entry.author = None
    try:
        entry.editor
    except AttributeError:
        entry.editor = None

    if entry.author:
        name = entry.author
    elif entry.editor:
        name = entry.editor
    else:
        name = 'noname'

    return name.split('and')


def get_year(entry):
    if entry.date:
        year = entry.date.year
    else:
        year = entry.year

    return str(year)[-2:]


def get_title(entry):
    title = entry.title.translate(str.maketrans('','',''' _@"',\#}{~%&^$'''))
    return title


def get_last_name_part(name):
    last_name = name.split(',')[0].strip()
    return last_name[:4].replace(' ','').title()


def author_year_key(entry):
    last_name_list = [get_last_name_part(name.strip()) for name in get_namelist(entry)]
    names = ''.join(last_name_list)
    return "{id}:{name}:{year}".format(id=entry.id, name=names[:12], year=get_year(entry))


def titel_year_key(entry):
    title = get_title(entry)

    if len(title) <= 18:
        titelstub = title
    else:
        titelstub = title[:8] + '...' + title[-8:]

    return "{id}:{titel}:{year}".format(id=entry.id, titel=titelstub, year=get_year(entry))


def get_bibtex_key(entry):
    return titel_year_key(entry)