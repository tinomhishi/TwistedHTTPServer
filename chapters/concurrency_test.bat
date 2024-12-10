@echo off
REM Number of requests to send
set COUNT=100

REM Target URL
set URL=http://localhost:8080

REM Loop through and send requests
for /L %%i in (1,1,%COUNT%) do (
    echo Sending request %%i
    curl -s -o nul %URL%
    REM Add a delay if needed (e.g., 1 second)
    REM timeout /t 1 /nobreak > nul
)
echo Done!
pause
