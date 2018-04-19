import logging
from ckan import model
from ckan.plugins import toolkit
log = logging.getLogger(__name__)


def render_tree(top_nodes=None):
    '''Returns HTML for a hierarchy of all data containers'''
    context = {'model': model, 'session': model.Session}
    if not top_nodes:
        top_nodes = toolkit.get_action('group_tree')(
            context,
            data_dict={'type': 'data-container'})
    return _render_tree(top_nodes)


def _render_tree(top_nodes):
    html = '<ul class="hierarchy-tree-top">'
    for node in top_nodes:
        html += _render_tree_node(node)
    return html + '</ul>'


def _render_tree_node(node):
    html = '<a href="/data-container/{}">{}</a>'.format(
        node['name'], node['title'])
    if node['children']:
        html += '<ul class="hierarchy-tree">'
        for child in node['children']:
            html += _render_tree_node(child)
        html += '</ul>'

    if node['highlighted']:
        html = '<li id="node_{}" class="highlighted">{}</li>'.format(
            node['name'], html)
    else:
        html = '<li id="node_{}">{}</li>'.format(node['name'], html)
    return html


def page_authorized():

    if (toolkit.c.controller == 'error' and
            toolkit.c.action == 'document' and
            toolkit.c.code and toolkit.c.code[0] != '403'):
        return True

    # TODO: remove request_reset and perform_reset when LDAP is integrated
    return (
        toolkit.c.userobj or
        (toolkit.c.controller == 'user' and
            toolkit.c.action in [
                'login', 'logged_in', 'request_reset', 'perform_reset',
                'logged_out', 'logged_out_page', 'logged_out_redirect'
                ]))


def get_linked_datasets_options(exclude_id=None):
    context = {'model': model}

    # Get options
    options = []
    get_containers = toolkit.get_action('organization_list_for_user')
    get_container = toolkit.get_action('organization_show')
    containers = get_containers(context, {'id': toolkit.c.userobj.id})
    for container in containers:
        container = get_container(context, {'id': container['id'], 'include_datasets': True})
        for package in container['packages']:
            if package['id'] == exclude_id:
                continue
            options.append({'text': package['name'], 'value': package['id']})

    return options


def get_linked_datasets_names(ids):
    context = {'model': model}

    # Get names
    names = []
    ids = ids if isinstance(ids, list) else ids.strip('{}').split(',')
    for id in ids:
        dataset = toolkit.get_action('package_show')(context, {'id': id})
        names.append(dataset['name'])

    return names
