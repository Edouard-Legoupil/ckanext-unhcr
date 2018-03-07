import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

from ckanext.unhcr import helpers, jobs


class UnhcrPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'unhcr')

    # IFacets

    def _facets(self, facets_dict):
        if 'groups' in facets_dict:
            del facets_dict['groups']
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return self._facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        return self._facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        return self._facets(facets_dict)

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'render_tree': helpers.render_tree,
            'page_authorized': helpers.page_authorized,
        }

    # IPackageController

    def before_index(self, pkg_dict):
        pkg_dict.pop('admin_notes', None)
        pkg_dict.pop('extras_admin_notes', None)
        return pkg_dict

    def after_create(self, context, data_dict):
        if not context.get('job'):
            toolkit.enqueue_job(jobs.process_dataset_fields, [data_dict['id']])

    def after_update(self, context, data_dict):
        if not context.get('job'):
            toolkit.enqueue_job(jobs.process_dataset_fields, [data_dict['id']])
