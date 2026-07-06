"""
MarketVerse Guardian
registry_sync.py

Purpose:
Synchronize Project Registry with Guardian scan results.
"""

from .registry import ProjectRegistry, ModuleInfo


class RegistrySync:

    def __init__(self):
        self.registry = ProjectRegistry()

    def sync(self, files, validation_results):
        """
        Synchronize registry from scanned project files.
        """

        for file, result in zip(files, validation_results):

            module = ModuleInfo(
                name=file.stem,
                path=str(file),
                status="OK" if result.valid else "ERROR"
            )

            self.registry.register(module)

        return self.registry

    def export(self):
        return self.registry.all_modules()
