python -m zipapp .\RRO_savefile_editor\ --python="/usr/bin/env python3" --main=main:main --output=ROSE_0310.pyz
pyinstaller.exe --onefile .\main4exe.py -n ROSE_0310.exe
Get-FileHash .\dist\ROSE_0310b.exe
Get-FileHash .\ROSE_0310b.pyz