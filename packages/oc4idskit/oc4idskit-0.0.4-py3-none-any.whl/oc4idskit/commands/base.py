from ocdskit.commands.base import OCDSCommand


class OC4IDSCommand(OCDSCommand):
    def add_package_arguments(self, infix, prefix='', version='0.9'):
        super().add_package_arguments(infix, prefix, version)
