# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AutoPipInstaller
                                 A QGIS plugin
 When updating, metadata plugin dependencies will be installed
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-07-16
        copyright            : (C) 2024 by fdobad
        email                : fbadilla@ing.uchile.cl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'fdobad'
__date__ = '2024-07-16'
__copyright__ = '(C) 2024 by fdobad'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AutoPipInstaller class from file AutoPipInstaller.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .auto_pip import AutoPipInstallerPlugin
    return AutoPipInstallerPlugin()