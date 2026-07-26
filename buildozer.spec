[app]

# (str) Title of your application
title = Eltern App

# (str) Package name
package.name = elternapp

# (str) Package domain (needed for android packaging)
package.domain = org.eltern

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let it include all files by default)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[buildozer]
log_level = 2
