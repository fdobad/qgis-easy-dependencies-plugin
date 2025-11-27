# QGIS EASY PYTHON DEPENDENCIES PLUGIN ADD-ON

Get interactive automatic checking and installation of python dependencies on plugin load!

## Quickstart
- Put `dependencies_handler.[py,txt]` files in your plugin folder, 
- Add two lines to your plugin initialization code:

    def __init__(self):
        self.provider = None
        from . import dependencies_handler

        dependencies_handler.run()

A example plugin named `auto_pip` is provided!

## Description

This addon code `dependencies_handler.py` runs on plugin initialization, checking for the presence of a python dependency listed in `dependencies_handler.txt` in the python environment. If the dependency is not and exact match, the user is prompted to allow running of `pip install <package>` to install the required dependency.
Also included is logic to reload the installed package modules in the current QGIS python environment, so that the plugin can use the newly installed package without restarting QGIS.
Finally, the user is given the option to disable future dependency checks implemented by writing a `skip_checking=True` line in the `dependencies_handler.txt` file. This feature is also useful for plugin developers to avoid prompting users during development!

## Proof of concept
Relies on setting a custom repo store and two plugin releases with metadata.txt:plugin_dependencies pointing the same package but different versions, to test what happens on update.

1. Deploy the plugin server from the v1 branch, by using the `deploy_server.yml` action workflow
2. Install the repo store from the published page link
3. Install the plugin from the repo store. Every time the plugin is loaded, dependencies are checked. __You'll be prompted to install the dependencies from metadata.txt if they are not present or version mismatched__
4. Deploy the plugin server from the v2 branch
5. Update the plugin when prompted, __you'll be prompted to install the dependencies from metadata.txt if they are not present or version mismatched__

 ```mermaid
 graph TD
    Start(QGIS loads plugin) --> ReadMetadata[Read plugin metadata]
    ReadMetadata --> CheckSkipOption{skip_checking?}
    CheckSkipOption -->|True| Log1(Log Warning)
    CheckSkipOption -->|False| ParseRequirement[Parse plugin_dependencies & version]
    ParseRequirement --> TryFindVersion[Try to find installed package version]
    TryFindVersion -->|Found| CompareVersions{Compare<br>versions}
    TryFindVersion -->|Not Found| AskInstall
    CompareVersions -->|Mismatch| VersionMismatch[Version mismatch]
    CompareVersions -->|Match| Log2(Log Sucess)
    VersionMismatch --> AskInstall[Ask user to allow pip install]
    AskInstall -->|Yes| RunPipInstall[Run pip install command]
    AskInstall -->|No| ShowWarning[Show warning message box]
    RunPipInstall -->|Success| ReloadModules[Try to reload modules]
    RunPipInstall -->|Failure| LogEnd3(Log Critical)
    ReloadModules -->|Success| LogEnd4(Log Success)
    ReloadModules -->|Failure| LogReloadFail(Log Critical)
    ShowWarning --> CheckDisable{user disables<br>future checks?}
    CheckDisable -->|Yes| DisableChecking[write skip_checking=True in plugin metadata]
    DisableChecking --> LogEnd5(Log Warning)
    CheckDisable -->|No| LogEnd6(Log Info)
    
```
