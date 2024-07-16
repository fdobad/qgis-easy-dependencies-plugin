# QGIS EASY DEPENDENCIES PLUGIN

This dummy plugin implements a method that on initialization, checks for the presence of plugin_dependencies (in metadata.txt) in the python environment. If the dependencies are not present or version mismatched, the user is prompted to allow installation.

## Proof of concept
Relies on setting a custom repo store and two plugin releases with metadata.txt:plugin_dependencies pointing the same package but different versions, to test what happens on update.

1. Deploy the plugin server from the v1 branch, by using the `deploy_server.yml` action workflow
2. Install the repo store from the published page link
3. Install the plugin from the repo store. Every time the plugin is loaded, dependencies are checked. __You'll be prompted to install the dependencies from metadata.txt if they are not present or version mismatched__
4. Deploy the plugin server from the v2 branch
5. Update the plugin when prompted, __you'll be prompted to install the dependencies from metadata.txt if they are not present or version mismatched__
 
 graph TD
    Start(Start) --> ReadMetadata[Read plugin metadata]
    ReadMetadata --> CheckSkipOption{Check if skip_checking is True}
    CheckSkipOption -->|True| LogSkip[Log skip checking message]
    CheckSkipOption -->|False| ParseRequirement[Parse plugin_dependencies]
    ParseRequirement --> TryFindVersion[Try to find installed package version]
    TryFindVersion -->|Found| CompareVersions{Compare versions}
    TryFindVersion -->|Not Found| PackageNotFound[Package not installed]
    CompareVersions -->|Mismatch| VersionMismatch[Version mismatch]
    CompareVersions -->|Match| LogSuccess[Log version requirement satisfied]
    VersionMismatch --> AskInstall[Ask user to allow pip install]
    PackageNotFound --> AskInstall
    AskInstall -->|Yes| RunPipInstall[Run pip install command]
    AskInstall -->|No| UserDeclined[Log user declined installation]
    RunPipInstall -->|Success| ReloadModules[Try to reload modules]
    RunPipInstall -->|Failure| LogInstallFail[Log installation failed]
    ReloadModules -->|Success| LogReloadSuccess[Log reload success]
    ReloadModules -->|Failure| LogReloadFail[Log reload failure]
    UserDeclined --> ShowWarning[Show warning message box]
    ShowWarning --> CheckDisable[Check if user disables future checks]
    CheckDisable -->|Disabled| DisableChecking[Disable future checks]
