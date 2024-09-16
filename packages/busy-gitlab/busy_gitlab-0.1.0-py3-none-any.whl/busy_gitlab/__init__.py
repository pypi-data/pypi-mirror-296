from busy.error import BusyError

QUEUE = 'tasks'


def sync(app):
    dones = app.storage.get_collection(QUEUE, 'done')
    todos = app.storage.get_collection(QUEUE, 'todo')
    plans = app.storage.get_collection(QUEUE, 'plan')
    tag = first_item_configured_tag(app)
    alltodos = [t.base for t in todos[1:] if tag in t.tags]
    utodos = []
    [utodos.append(x) for x in alltodos if x not in utodos]
    allplans = [t.base for t in plans if tag in t.tags]
    uplans = []
    [uplans.append(x) for x in allplans if x not in (utodos + uplans)]
    alldones = [d.base for d in dones if tag in d.tags]
    udones = []
    [udones.append(x) for x in alldones if x not in (utodos + uplans + udones)]
    fmtdones = [f"- [x] {d}\n" for d in udones]
    fmttodos = [f"- [ ] {t}\n" for t in utodos]
    fmtplans = [f"- [ ] {p}\n" for p in uplans]
    return "".join(fmtdones + fmttodos + fmtplans)


def first_item(app):
    """The current task underway. Please give this function a new name."""
    todos = app.storage.get_collection(QUEUE, 'todo')
    return todos[0]


def first_item_configured_tag(app):
    """The tag that matters - one from the config that's in the current task"""
    my_tags = first_item(app).tags
    config = app.config.get('busy-integrations-gitlab-tags')
    configured = config.split(' ') if config else []
    tag = next((t for t in configured if t in my_tags), None)
    return tag
