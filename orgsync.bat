@ECHO OFF

rem Script to sync org-mode files stored in the home directory to cloude storage.
rem 
rem Windows version

SET logdir=%USERPROFILE%\orglogs\

rem https://stackoverflow.com/a/19163883/4276832
for /f %%a in ('powershell -Command "Get-Date -format yyyy_MM_dd__HH_mm_ss"') do set datetime=%%a
SET logfile="%logdir%orglog-%datetime%.log"

echo %logfile%

IF NOT EXIST %logdir% mkdir %logdir%

REM Create logfile is it does not exist - https://stackoverflow.com/a/211045/4276832
IF NOT EXIST %logfile% copy /y NUL %logfile% >NUL

rclone copy google:org %USERPROFILE%\org -v -u --log-file %logfile%
rclone sync %USERPROFILE%\org google:org -v -u --log-file %logfile%