from pathlib import Path
from pymsbuild import PydFile, ImportGroup, Property, SourceFile

__all__ = ["RustPydFile", "Cargo"]

TARGETS = Path(__file__).absolute().parent / "targets"

class RustPydFile(PydFile):
    class DefaultToolsetProps(ImportGroup):
        name = "$RustPydFile.DefaultRustProps"
        imports = [
            "$(PyMsbuildTargets)/common.props",
            "$(PyMsbuildRustTargets)/rust-default-$(Platform).props",
        ]

    # Legacy name
    DefaultToolsetImports = DefaultToolsetProps

    class ToolsetProps(ImportGroup):
        name = "$RustPydFile.RustProps"
        imports = [
            "$(PyMsbuildRustTargets)/rust-$(Platform).props",
        ]

    # Legacy name, also requires pyd.props here
    class ToolsetImports(ImportGroup):
        name = "$RustPydFile.RustImports"
        imports = [
            "$(PyMsbuildRustTargets)/rust-$(Platform).props",
            "$(PyMsbuildTargets)/pyd.props",
        ]

    class ToolsetTargets(ImportGroup):
        name = "$RustPydFile.RustTargets"
        imports = [
            "$(PyMsbuildTargets)/common.targets",
            "$(PyMsbuildRustTargets)/rust-$(Platform).targets",
            "$(PyMsbuildTargets)/pyd.targets",
        ]

    def __init__(self, name, *members, project_file=None, **kwargs):
        super().__init__(name, *members, project_file=project_file, **kwargs)
        self.insert(self.GlobalProperties.name, Property("PyMsbuildRustTargets", TARGETS))

class Cargo(SourceFile):
    _ITEMNAME = "Cargo"
