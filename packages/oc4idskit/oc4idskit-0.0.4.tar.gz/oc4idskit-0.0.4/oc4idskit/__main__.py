import logging

from ocdskit.__main__ import main as _main


def main():
    modules = (
        "oc4idskit.commands.convert_from_ocds",
        "oc4idskit.commands.split_project_packages",
        "oc4idskit.commands.combine_project_packages"
    )

    logger = logging.getLogger("oc4idskit")

    _main(
        description="Open Contracting for Infrastructure Data Standards CLI",
        modules=modules,
        logger=logger,
    )


if __name__ == "__main__":
    main()
