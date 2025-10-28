"""
Automated Mobile App Testing Agent Package
"""

__version__ = "1.0.0"
__author__ = "Hasib Nirjhar"

from .emulator_manager import EmulatorManager
from .apk_installer import APKInstaller
from .ui_explorer import UIExplorer
from .test_executor import TestExecutor
from .report_generator import ReportGenerator

__all__ = [
    'EmulatorManager',
    'APKInstaller',
    'UIExplorer',
    'TestExecutor',
    'ReportGenerator'
]