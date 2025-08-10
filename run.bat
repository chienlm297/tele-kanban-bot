@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ========================================
REM TELEGRAM KANBAN BOT - RUN SCRIPT (Windows)
REM ========================================
REM Script này giúp bạn dễ dàng chạy project trên Windows
REM 
REM Cách sử dụng:
REM run.bat          REM Chạy cả bot và dashboard
REM run.bat bot      REM Chỉ chạy bot
REM run.bat web      REM Chỉ chạy dashboard
REM run.bat test     REM Test proxy connection
REM run.bat install  REM Cài đặt dependencies
REM run.bat help     REM Hiển thị hướng dẫn
REM ========================================

REM Màu sắc cho output (Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "PURPLE=[95m"
set "CYAN=[96m"
set "NC=[0m"

REM Logo và thông tin
:print_logo
echo %CYAN%
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🤖 TELEGRAM KANBAN BOT                   ║
echo ║                                                              ║
echo ║  📱 Bot Telegram tự động ghi nhận và quản lý công việc      ║
echo ║  🌐 Dashboard web để quản lý và theo dõi tasks              ║
echo ║  🎯 Hỗ trợ BigData workflow và team collaboration           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo %NC%
goto :eof

REM Kiểm tra Python
:check_python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo %RED%❌ Python không được cài đặt!%NC%
        echo Vui lòng cài đặt Python 3.7+ trước khi chạy project
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
    )
) else (
    set "PYTHON_CMD=python"
)

echo %GREEN%✅ Python: %PYTHON_CMD% --version%NC%
goto :eof

REM Kiểm tra pip
:check_pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    pip3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo %RED%❌ pip không được cài đặt!%NC%
        echo Vui lòng cài đặt pip trước khi chạy project
        pause
        exit /b 1
    ) else (
        set "PIP_CMD=pip3"
    )
) else (
    set "PIP_CMD=pip"
)

echo %GREEN%✅ pip: %PIP_CMD% --version%NC%
goto :eof

REM Kiểm tra file settings
:check_settings
if not exist "src\config\settings.py" (
    echo %RED%❌ File settings.py không tồn tại!%NC%
    echo Vui lòng copy src\config\example.py thành src\config\settings.py và điền thông tin
    pause
    exit /b 1
)

echo %GREEN%✅ File settings.py đã sẵn sàng%NC%
goto :eof

REM Cài đặt dependencies
:install_dependencies
echo %BLUE%📦 Đang cài đặt dependencies...%NC%

if exist "requirements.txt" (
    %PIP_CMD% install -r requirements.txt
    if %errorlevel% equ 0 (
        echo %GREEN%✅ Cài đặt dependencies thành công!%NC%
    ) else (
        echo %RED%❌ Cài đặt dependencies thất bại!%NC%
        pause
        exit /b 1
    )
) else (
    echo %RED%❌ File requirements.txt không tồn tại!%NC%
    pause
    exit /b 1
)
goto :eof

REM Test proxy connection
:test_proxy
echo %BLUE%🔍 Đang test kết nối proxy...%NC%
%PYTHON_CMD% test_proxy.py
goto :eof

REM Chạy bot
:run_bot
echo %BLUE%🤖 Đang khởi động Telegram Bot...%NC%
echo %YELLOW%💡 Bot sẽ tự động ghi nhận các tin nhắn được tag tên%NC%
echo %YELLOW%💡 Sử dụng /help để xem các lệnh có sẵn%NC%
echo.
%PYTHON_CMD% main.py bot
goto :eof

REM Chạy dashboard
:run_dashboard
echo %BLUE%🌐 Đang khởi động Web Dashboard...%NC%
echo %YELLOW%💡 Dashboard sẽ mở tại: http://localhost:5000%NC%
echo %YELLOW%💡 Nhấn Ctrl+C để dừng%NC%
echo.
%PYTHON_CMD% main.py web
goto :eof

REM Chạy cả bot và dashboard
:run_both
echo %BLUE%🚀 Đang khởi động cả Bot và Dashboard...%NC%
echo %YELLOW%💡 Bot sẽ chạy trong background%NC%
echo %YELLOW%💡 Dashboard sẽ mở tại: http://localhost:5000%NC%
echo %YELLOW%💡 Nhấn Ctrl+C để dừng tất cả%NC%
echo.
%PYTHON_CMD% main.py both
goto :eof

REM Hiển thị hướng dẫn
:show_help
echo %CYAN%📖 HƯỚNG DẪN SỬ DỤNG:%NC%
echo.
echo %YELLOW%Chạy cả bot và dashboard:%NC%
echo   run.bat
echo.
echo %YELLOW%Chỉ chạy bot:%NC%
echo   run.bat bot
echo.
echo %YELLOW%Chỉ chạy dashboard:%NC%
echo   run.bat web
echo.
echo %YELLOW%Test kết nối proxy:%NC%
echo   run.bat test
echo.
echo %YELLOW%Cài đặt dependencies:%NC%
echo   run.bat install
echo.
echo %YELLOW%Hiển thị hướng dẫn này:%NC%
echo   run.bat help
echo.
echo %CYAN%📱 TÍNH NĂNG CHÍNH:%NC%
echo   • Bot tự động ghi nhận công việc khi được tag tên
echo   • Dashboard web để quản lý và theo dõi tasks
echo   • Hỗ trợ proxy cho môi trường công ty
echo   • Thống kê theo người giao việc
echo   • Ghi chú khi hoàn thành task
echo.
goto :eof

REM Main function
:main
call :print_logo

REM Kiểm tra môi trường
call :check_python
call :check_pip
call :check_settings

REM Xử lý tham số
if "%1"=="" (
    call :run_both
) else if "%1"=="bot" (
    call :run_bot
) else if "%1"=="web" (
    call :run_dashboard
) else if "%1"=="both" (
    call :run_both
) else if "%1"=="test" (
    call :test_proxy
) else if "%1"=="install" (
    call :install_dependencies
) else if "%1"=="help" (
    call :show_help
) else if "%1"=="-h" (
    call :show_help
) else if "%1"=="--help" (
    call :show_help
) else (
    echo %RED%❌ Tham số không hợp lệ: %1%NC%
    echo.
    call :show_help
    pause
    exit /b 1
)

goto :eof

REM Chạy main function
call :main %*
pause
