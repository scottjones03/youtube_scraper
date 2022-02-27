$venvPath = "venv"
# Deactivate environment if one is currently active
if (Get-Command deactivate -errorAction SilentlyContinue) {
    "Deactivate currently active virual environment."
    deactivate
}
else {
    "No need to run deactivate. No active virtual environment."
}
# Remove old environment if exists
if (Test-Path $venvPath) {
    "Remove existing environment in directory $venvPath."
    # Remove-Item can't deal with the long jupyter cache paths, so use rmdir
    # More ideas at https://superuser.com/questions/78434/how-to-delete-directories-with-path-names-too-long-for-normal-delete
    Cmd /C "rmdir /S /Q $venvPath"
}
else {
    "No need to remove old virtual environment $venvPath - does not exist."
}
# Set up fresh and new environment
"Create virtual environment"
python -m venv $venvPath
"Activate"
.\activate_venv.ps1
"Upgrade pip"
python -m pip install --upgrade pip
"Install requirements from requirements.txt"
pip install -r requirements.txt
"Install pre-commit"
pre-commit install
