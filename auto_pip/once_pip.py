#!/bin/env python3
"""
this module:
- if file exists, it wont install the package
- gets the pip package name, operator and version from a file
- call subprocess to install the package if it is not installed
- if returns ok, it will write the package name, version, and timestamp to a file
"""
from configparser import ConfigParser
from distutils.version import LooseVersion
from importlib import import_module, reload
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from re import match as re_match
from subprocess import run

from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtWidgets import QCheckBox, QMessageBox


def once_pip():
    cp = ConfigParser()
    cp.read(Path(__file__).parent / "metadata.txt")
    # cp.read(Path().cwd() / "metadata.txt")
    plugin_name = cp.get("general", "name")
    if cp.get("general", "skip_checking", fallback="False") == "True":
        QgsMessageLog().logMessage(
            f"{plugin_name}: is set to skip_checking=True versions in metadata.txt! (remove this line to re-enable checking)",
            tag="Plugins",
            level=Qgis.Warning,
        )
        return
    requirement = cp.get("general", "plugin_dependencies")

    match = re_match(r"(.*?)([=<>!]{1,2})([\d.]+)", requirement)
    if match:
        req_pkg_name = match.group(1)
        req_operator = match.group(2)
        req_version = match.group(3)

    try:
        found_version = distribution(req_pkg_name).version
        if LooseVersion(req_version) != LooseVersion(found_version):
            msg = "version mismatch, found: " + found_version
        else:
            QgsMessageLog().logMessage(f"{plugin_name}: {requirement} satisfied!", tag="Plugins", level=Qgis.Success)
            return

    except PackageNotFoundError:
        msg = "is not installed"

    response = QMessageBox.question(
        None,
        f"{plugin_name} Question:",
        f"Allow automatic pip install of {requirement} ?\n"
        f"Because: {msg}\n"
        + "Probably need to restart QGIS afterwards (if the plugin gets hidden or toggling the checkbox from the plugin manager installed list doesn't make it available)",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if response == QMessageBox.Yes:
        result = run(["python3", "-m", "pip", "install", requirement], capture_output=True, text=True)
        if result.returncode == 0:
            QgsMessageLog().logMessage(f"{plugin_name}: Installation success!", tag="Plugins", level=Qgis.Success)
            msg = f"pip install {requirement} success\n"
            try:
                for module_name in get_module_names(req_pkg_name):
                    module = import_module(module_name)
                    reload(module)
                    msg = f"reload {module_name} success\n"
                    alevel = Qgis.Success
            except Exception:
                msg = f"reloading {req_pkg_name} packages failed\n"
                alevel = Qgis.Critical
            QMessageBox.information(None, f"{plugin_name}", f"{plugin_name}: {msg}")
            QgsMessageLog().logMessage(f"{plugin_name}: {e} attempting to reload modules", tag="Plugins", level=alevel)
            return
        QgsMessageLog().logMessage(
            f"{plugin_name}: Installation failed! " + result.stderr, tag="Plugins", level=Qgis.Critical
        )
        QMessageBox.critical(None, f"{plugin_name}", f"{plugin_name}: Installation failed! " + result.stderr)
    elif response == QMessageBox.No:
        QgsMessageLog().logMessage(f"{plugin_name}: User declined installation!", tag="Plugins", level=Qgis.Warning)

        qmb = QMessageBox(
            QMessageBox.Warning,
            f"{plugin_name}",
            f"{plugin_name}: User declined installation! Please resolve manually in QGIS Python Console, typing:\n\n\t!pip install {requirement}\n",
        )
        qcb = QCheckBox("Do not attempt to check and install dependencies again!")
        qmb.setCheckBox(qcb)
        qmb.exec_()
        if qcb.isChecked():
            QgsMessageLog().logMessage(f"{plugin_name}: User disabled installation!", tag="Plugins", level=Qgis.Warning)
            with open(Path(__file__).parent / "metadata.txt", "a") as f:
                f.write("skip_checking=True\n")


def get_module_names(distribution_name="your-package-name"):
    try:
        dist_info = distribution(distribution_name)
        unique_parents = set()

        for file in dist_info.files:
            path = Path(str(file))
            if name := path.parent.name:
                if name != "__pycache__" and name.find(".") == -1:
                    unique_parents.add(path.parent.name)

        return unique_parents

    except PackageNotFoundError as e:
        QgsMessageLog().logMessage(
            f"{plugin_name}: {e} attempting to get module names", tag="Plugins", level=Qgis.Critical
        )
        return []
