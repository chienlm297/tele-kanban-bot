# ========================================
# TELEGRAM KANBAN BOT - RUN SCRIPT (PowerShell)
# ========================================
# Script này giúp bạn dễ dàng chạy project trên Windows PowerShell
# 
# Cách sử dụng:
# .\run.ps1          # Chạy cả bot và dashboard
# .\run.ps1 bot      # Chỉ chạy bot
# .\run.ps1 web      # Chỉ chạy dashboard
# .\run.ps1 test     # Test proxy connection
# .\run.ps1 install  # Cài đặt dependencies
# .\run.ps1 help     # Hiển thị hướng dẫn
# ========================================

param(
    [Parameter(Position=0)]
    [string]$Mode = "both"
)

# Màu sắc cho output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$Purple = "Magenta"
$Cyan = "Cyan"
$White = "White"

# Logo và thông tin
function Show-Logo {
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor $Cyan
    Write-Host "║                    🤖 TELEGRAM KANBAN BOT                   ║" -ForegroundColor $Cyan
    Write-Host "║                                                              ║" -ForegroundColor $Cyan
    Write-Host "║  📱 Bot Telegram tự động ghi nhận và quản lý công việc      ║" -ForegroundColor $Cyan
    Write-Host "║  🌐 Dashboard web để quản lý và theo dõi tasks              ║" -ForegroundColor $Cyan
    Write-Host "║  🎯 Hỗ trợ BigData workflow và team collaboration           ║" -ForegroundColor $Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor $Cyan
    Write-Host ""
}

# Kiểm tra Python
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $script:PythonCmd = "python"
            Write-Host "✅ Python: $pythonVersion" -ForegroundColor $Green
            return $true
        }
    } catch {
        try {
            $python3Version = python3 --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $script:PythonCmd = "python3"
                Write-Host "✅ Python: $python3Version" -ForegroundColor $Green
                return $true
            }
        } catch {
            Write-Host "❌ Python không được cài đặt!" -ForegroundColor $Red
            Write-Host "Vui lòng cài đặt Python 3.7+ trước khi chạy project" -ForegroundColor $Red
            return $false
        }
    }
    return $false
}

# Kiểm tra pip
function Test-Pip {
    try {
        $pipVersion = pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $script:PipCmd = "pip"
            Write-Host "✅ pip: $pipVersion" -ForegroundColor $Green
            return $true
        }
    } catch {
        try {
            $pip3Version = pip3 --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $script:PipCmd = "pip3"
                Write-Host "✅ pip: $pip3Version" -ForegroundColor $Green
                return $true
            }
        } catch {
            Write-Host "❌ pip không được cài đặt!" -ForegroundColor $Red
            Write-Host "Vui lòng cài đặt pip trước khi chạy project" -ForegroundColor $Red
            return $false
        }
    }
    return $false
}

# Kiểm tra file settings
function Test-Settings {
    if (-not (Test-Path "src\config\settings.py")) {
        Write-Host "❌ File settings.py không tồn tại!" -ForegroundColor $Red
        Write-Host "Vui lòng copy src\config\example.py thành src\config\settings.py và điền thông tin" -ForegroundColor $Red
        return $false
    }
    
    Write-Host "✅ File settings.py đã sẵn sàng" -ForegroundColor $Green
    return $true
}

# Cài đặt dependencies
function Install-Dependencies {
    Write-Host "📦 Đang cài đặt dependencies..." -ForegroundColor $Blue
    
    if (Test-Path "requirements.txt") {
        & $PipCmd install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Cài đặt dependencies thành công!" -ForegroundColor $Green
        } else {
            Write-Host "❌ Cài đặt dependencies thất bại!" -ForegroundColor $Red
            return $false
        }
    } else {
        Write-Host "❌ File requirements.txt không tồn tại!" -ForegroundColor $Red
        return $false
    }
    return $true
}

# Test proxy connection
function Test-Proxy {
    Write-Host "🔍 Đang test kết nối proxy..." -ForegroundColor $Blue
    & $PythonCmd test_proxy.py
}

# Chạy bot
function Start-Bot {
    Write-Host "🤖 Đang khởi động Telegram Bot..." -ForegroundColor $Blue
    Write-Host "💡 Bot sẽ tự động ghi nhận các tin nhắn được tag tên" -ForegroundColor $Yellow
    Write-Host "💡 Sử dụng /help để xem các lệnh có sẵn" -ForegroundColor $Yellow
    Write-Host ""
    
    & $PythonCmd main.py bot
}

# Chạy dashboard
function Start-Dashboard {
    Write-Host "🌐 Đang khởi động Web Dashboard..." -ForegroundColor $Blue
    Write-Host "💡 Dashboard sẽ mở tại: http://localhost:5000" -ForegroundColor $Yellow
    Write-Host "💡 Nhấn Ctrl+C để dừng" -ForegroundColor $Yellow
    Write-Host ""
    
    & $PythonCmd main.py web
}

# Chạy cả bot và dashboard
function Start-Both {
    Write-Host "🚀 Đang khởi động cả Bot và Dashboard..." -ForegroundColor $Blue
    Write-Host "💡 Bot sẽ chạy trong background" -ForegroundColor $Yellow
    Write-Host "💡 Dashboard sẽ mở tại: http://localhost:5000" -ForegroundColor $Yellow
    Write-Host "💡 Nhấn Ctrl+C để dừng tất cả" -ForegroundColor $Yellow
    Write-Host ""
    
    & $PythonCmd main.py both
}

# Hiển thị hướng dẫn
function Show-Help {
    Write-Host "📖 HƯỚNG DẪN SỬ DỤNG:" -ForegroundColor $Cyan
    Write-Host ""
    Write-Host "Chạy cả bot và dashboard:" -ForegroundColor $Yellow
    Write-Host "  .\run.ps1"
    Write-Host ""
    Write-Host "Chỉ chạy bot:" -ForegroundColor $Yellow
    Write-Host "  .\run.ps1 bot"
    Write-Host ""
    Write-Host "Chỉ chạy dashboard:" -ForegroundColor $Yellow
    Write-Host "  .\run.ps1 web"
    Write-Host ""
    Write-Host "Test kết nối proxy:" -ForegroundColor $Yellow
    Write-Host "  .\run.ps1 test"
    Write-Host ""
    Write-Host "Cài đặt dependencies:" -ForegroundColor $Yellow
    Write-Host "  .\run.ps1 install"
    Write-Host ""
    Write-Host "Hiển thị hướng dẫn này:" -ForegroundColor $Yellow
    Write-Host "  .\run.ps1 help"
    Write-Host ""
    Write-Host "📱 TÍNH NĂNG CHÍNH:" -ForegroundColor $Cyan
    Write-Host "  • Bot tự động ghi nhận công việc khi được tag tên"
    Write-Host "  • Dashboard web để quản lý và theo dõi tasks"
    Write-Host "  • Hỗ trợ proxy cho môi trường công ty"
    Write-Host "  • Thống kê theo người giao việc"
    Write-Host "  • Ghi chú khi hoàn thành task"
    Write-Host ""
}

# Main function
function Main {
    Show-Logo
    
    # Kiểm tra môi trường
    if (-not (Test-Python)) { return }
    if (-not (Test-Pip)) { return }
    if (-not (Test-Settings)) { return }
    
    # Xử lý tham số
    switch ($Mode.ToLower()) {
        "bot" {
            Start-Bot
        }
        "web" {
            Start-Dashboard
        }
        "both" {
            Start-Both
        }
        "test" {
            Test-Proxy
        }
        "install" {
            Install-Dependencies
        }
        "help" {
            Show-Help
        }
        default {
            Write-Host "❌ Tham số không hợp lệ: $Mode" -ForegroundColor $Red
            Write-Host ""
            Show-Help
            return
        }
    }
}

# Chạy main function
Main
