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
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from re import match as re_match
from subprocess import run

from qgis.core import QgsMessageLog
from qgis.PyQt.QtWidgets import QMessageBox


def once_pip():
    cp = ConfigParser()
    cp.read(Path(__file__).parent / "metadata.txt")
    # cp.read(Path().cwd() / "metadata.txt")
    plugin_name = cp.get("general", "name")
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
            QgsMessageLog().logMessage(f"{plugin_name}: {requirement} satisfied!", tag="Plugins", level=0)
            return

    except PackageNotFoundError:
        msg = "is not installed"

    response = QMessageBox.question(
        None,
        f"{plugin_name} Question:",
        "Allow automatic pip install of "
        + requirement
        + "?\nBecause: {msg}.\nProbably need to restart QGIS afterwards, if the plugin doesn't appear or toggling the checkbox from the plugin manager doesn't make it available",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if response == QMessageBox.Yes:
        result = run(["python3", "-m", "pip", "install", requirement], capture_output=True, text=True)
        if result.returncode == 0:
            QgsMessageLog().logMessage(f"{plugin_name}: Installation success!", tag="Plugins", level=1)
            QMessageBox.information(None, f"{plugin_name}: Installation success!", None)
            return
        QgsMessageLog().logMessage(f"{plugin_name}: Installation failed! " + result.stderr, tag="Plugins", level=1)
        QMessageBox.information(None, f"{plugin_name}: Installation failed! " + result.stderr, None)
    elif response == QMessageBox.No:
        QgsMessageLog().logMessage(f"{plugin_name}: User declined installation!", tag="Plugins", level=1)
        QMessageBox.information(None, f"{plugin_name}: User declined installation!", None)
