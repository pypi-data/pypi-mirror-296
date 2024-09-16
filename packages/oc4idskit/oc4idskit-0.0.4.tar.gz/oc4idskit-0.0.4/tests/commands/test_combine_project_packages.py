import pytest

from oc4idskit.__main__ import main
from oc4idskit.combine import combine_project_packages
from oc4idskit.exceptions import MissingProjectsWarning
from tests import assert_streaming


def test_command(capsys, monkeypatch):
    assert_streaming(
        capsys,
        monkeypatch,
        main,
        ["combine-project-packages"],
        ["project_package_split.json"],
        ["project_package_combined.json"],
    )


def test_command_warning(capsys, monkeypatch):
    with pytest.warns(MissingProjectsWarning) as records:
        def data():
            yield {}

        output = combine_project_packages(data())

    assert output == {"uri": "", "publisher": {}, "publishedDate": "", "version": "0.9", "projects": []}
    assert len(records) == 1
    assert str(records[0].message) == 'item 0 has no "projects" field (check that it is a project package)'
