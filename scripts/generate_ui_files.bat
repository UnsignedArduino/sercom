REM Converts the UI files from designer to Python classes we can import
REM Run in the repo root by calling "scripts/generate_ui_files.bat"

REM UI files

cd src/ui

pyuic5 designer/main_window.ui -o autogenerated/main_window.py

pyuic5 designer/dialogs/enter_custom_port_dialog.ui -o autogenerated/dialogs/enter_custom_port_dialog.py
pyuic5 designer/dialogs/set_baud_rate_dialog.ui -o autogenerated/dialogs/set_baud_rate_dialog.py
