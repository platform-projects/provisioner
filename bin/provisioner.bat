@echo off

set binPath=%~dp0
set srcPath=%binPath%\..\src

python3 %srcPath%\provisioner.py %*