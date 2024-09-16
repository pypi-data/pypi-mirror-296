from oc4idskit.__main__ import main
from tests import assert_streaming


def test_command(capsys, monkeypatch):
    assert_streaming(
        capsys,
        monkeypatch,
        main,
        ["split-project-packages", "1"],
        ["project_package.json"],
        ["project_package_split.json"],
    )
