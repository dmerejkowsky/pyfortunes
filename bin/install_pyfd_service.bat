@echo off
:: Start Pyfortunes Windows service

:: On Windows Vista and later, you need to right click on this file and
:: choose 'Run as administrator'

set PYTHONPATH=c:\Users\yannick\work\pyfortunes
c:\Python32\python.exe c:\Users\yannick\work\pyfortunes\bin\pyfd_service.py

pause
