from oc4idskit.__main__ import main
from tests import assert_streaming


def test_command(capsys, monkeypatch):
    assert_streaming(
        capsys,
        monkeypatch,
        main,
        ["convert-from-ocds", "--project-id", "1"],
        ["release_1.1.json"],
        ["oc4ids-project_minimal.json"],
    )


def test_command_package(capsys, monkeypatch):
    assert_streaming(
        capsys,
        monkeypatch,
        main,
        ["convert-from-ocds", "--project-id", "1", "--package"],
        ["release_1.1.json"],
        ["oc4ids-project-package_minimal.json"],
    )
