# QGIS EASY DEPENDENCIES PLUGIN

This dummy plugin implements a method that on initialization, checks for the presence of plugin_dependencies (in metadata.txt) in the python environment. If the dependencies are not present or version mismatched, the user is prompted to allow installation.

## Proof of concept
Relies on setting a custom repo store and two plugin releases with metadata.txt:plugin_dependencies pointing the same package but different versions, to test what happens on update.

1. Deploy the plugin server from the v1 branch, by using the `deploy_server.yml` action workflow
2. Install the repo store from the published page link
3. Install the plugin from the repo store. Every time the plugin is loaded, dependencies are checked. __You'll be prompted to install the dependencies from metadata.txt if they are not present or version mismatched__
4. Deploy the plugin server from the v2 branch
5. Update the plugin when prompted, __you'll be prompted to install the dependencies from metadata.txt if they are not present or version mismatched__
 
