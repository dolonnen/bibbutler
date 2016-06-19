def get_namelist(entry):
    try:
        entry.author
    except AttributeError:
        entry.author = None
    try:
        entry.editor
    except AttributeError:
        entry.editor = None
    try:
        entry.puplisher
    except AttributeError:
        entry.puplisher = None
        pass
    try:
        entry.organization
    except AttributeError:
        entry.organization = None

    if entry.author:
        name = entry.author
    elif entry.editor:
        name = entry.editor
    elif entry.puplisher:
        name = entry.puplisher
    elif entry.organization:
        name = entry.organization
    else:
        name = 'noname'

    return name.split(',')


def get_year(entry):
    if entry.year:
        year = entry.year
    else:
        year = entry.date.year

    return year


def author_year_key(entry):
    last_name_list = [name.split()[-1] for name in get_namelist(entry)]
    names = ','.join(last_name_list)
    return "{id}:{name}:{year}".format(id=entry.id, name=names, year=get_year(entry))


def get_bibtex_key(entry):
    return author_year_key(entry)


