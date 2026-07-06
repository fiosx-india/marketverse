"""
MarketVerse Guardian
registry.py

Purpose:
Maintain the official registry of all project modules.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ModuleInfo:
    """Information about a single project module."""

    name: str
    path: str
    purpose: str = ""
    version: str = "1.0.0"
    status: str = "UNKNOWN"
    dependencies: List[str] = field(default_factory=list)


class ProjectRegistry:
    """
    Stores information about every module in the project.
    """

    def __init__(self):
        self.modules: Dict[str, ModuleInfo] = {}

    def register(self, module: ModuleInfo):
        """Register or update a module."""
        self.modules[module.name] = module

    def get(self, name: str):
        """Return a module by name."""
        return self.modules.get(name)

    def all_modules(self):
        """Return all registered modules."""
        return list(self.modules.values())

    def remove(self, name: str):
        """Remove a module from the registry."""
        self.modules.pop(name, None)
