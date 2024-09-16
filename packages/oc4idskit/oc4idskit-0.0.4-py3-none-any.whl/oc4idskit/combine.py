import warnings

from oc4idskit.exceptions import MissingProjectsWarning
from oc4idskit.util import _empty_project_package, _remove_empty_optional_metadata, _update_package_metadata

DEFAULT_VERSION = '0.9'  # fields might be deprecated


def combine_project_packages(packages, uri='', publisher=None, published_date='', version=DEFAULT_VERSION):
    """
    Collects the projects from the project packages into one project package.

    Warns ``~oc4idskit.exceptions.MissingProjectsWarning`` if the "projects" field is missing from a project package.

    :param packages: an iterable of project packages
    :param str uri: the project package's ``uri``
    :param dict publisher: the project package's ``publisher``
    :param str published_date: the project package's ``publishedDate``
    :param str version: the project package's ``version``
    """
    # See options for not buffering all inputs into memory: https://github.com/open-contracting/ocdskit/issues/119
    output = _empty_project_package(uri, publisher, published_date, version)

    for i, package in enumerate(packages):
        _update_package_metadata(output, package)
        if 'projects' in package:
            output['projects'].extend(package['projects'])
        else:
            warnings.warn(
                f'item {i} has no "projects" field (check that it is a project package)',
                category=MissingProjectsWarning,
                stacklevel=2,
            )

    if publisher:
        output['publisher'] = publisher

    _remove_empty_optional_metadata(output)

    return output
