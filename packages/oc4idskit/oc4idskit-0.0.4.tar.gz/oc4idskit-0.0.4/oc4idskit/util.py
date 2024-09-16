def _empty_package(uri, publisher, published_date, version):
    if publisher is None:
        publisher = {}

    return {
        'uri': uri,
        'publisher': publisher,
        'publishedDate': published_date,
        'license': None,
        'publicationPolicy': None,
        'version': version,
    }


def _empty_project_package(uri='', publisher=None, published_date='', version=None):
    package = _empty_package(uri, publisher, published_date, version)
    package['projects'] = []
    return package


def _update_package_metadata(output, package):
    for field in ('publisher', 'license', 'publicationPolicy'):
        if field in package:
            output[field] = package[field]


def _remove_empty_optional_metadata(output):
    for field in ('license', 'publicationPolicy', 'version'):
        if output[field] is None:
            del output[field]
