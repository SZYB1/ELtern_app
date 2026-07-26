[app]

# (str) Title of your application
title = Eltern App

# (str) Package name
package.name = elternapp

# (str) Package domain (needed for android packaging)
package.domain = org.eltern

# (list) Source files to include (let it include all files by default)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# Trage hier deine Bibliotheken ein, z.B. kivy (oder was deine eltern_app_android.py braucht)
requirements = python3,kivy

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
