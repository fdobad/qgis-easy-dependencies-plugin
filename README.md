# QGIS EASY DEPENDENCIES PLUGIN

This dummy plugin implements a method that on initialization, checks for the presence of plugin_dependencies (in metadata.txt) in the python environment. If the dependencies are not present or version mismatched, the user is prompted to allow installation.

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
