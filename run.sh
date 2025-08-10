#!/bin/bash

# ========================================
# TELEGRAM KANBAN BOT - RUN SCRIPT
# ========================================
# Script này giúp bạn dễ dàng chạy project
# 
# Cách sử dụng:
# ./run.sh          # Chạy cả bot và dashboard
# ./run.sh bot      # Chỉ chạy bot
# ./run.sh web      # Chỉ chạy dashboard
# ./run.sh test     # Test proxy connection
# ./run.sh install  # Cài đặt dependencies
# ./run.sh help     # Hiển thị hướng dẫn
# ========================================

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logo và thông tin
print_logo() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🤖 TELEGRAM KANBAN BOT                   ║"
    echo "║                                                              ║"
    echo "║  📱 Bot Telegram tự động ghi nhận và quản lý công việc      ║"
    echo "║  🌐 Dashboard web để quản lý và theo dõi tasks              ║"
    echo "║  🎯 Hỗ trợ BigData workflow và team collaboration           ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Kiểm tra Python
check_python() {
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            echo -e "${RED}❌ Python không được cài đặt!${NC}"
            echo "Vui lòng cài đặt Python 3.7+ trước khi chạy project"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    
    echo -e "${GREEN}✅ Python: $($PYTHON_CMD --version)${NC}"
}

# Kiểm tra pip
check_pip() {
    if ! command -v pip3 &> /dev/null; then
        if ! command -v pip &> /dev/null; then
            echo -e "${RED}❌ pip không được cài đặt!${NC}"
            echo "Vui lòng cài đặt pip trước khi chạy project"
            exit 1
        else
            PIP_CMD="pip"
        fi
    else
        PIP_CMD="pip3"
    fi
    
    echo -e "${GREEN}✅ pip: $($PIP_CMD --version)${NC}"
}

# Kiểm tra file settings
check_settings() {
    if [ ! -f "src/config/settings.py" ]; then
        echo -e "${RED}❌ File settings.py không tồn tại!${NC}"
        echo "Vui lòng copy src/config/example.py thành src/config/settings.py và điền thông tin"
        exit 1
    fi
    
    echo -e "${GREEN}✅ File settings.py đã sẵn sàng${NC}"
}

# Cài đặt dependencies
install_dependencies() {
    echo -e "${BLUE}📦 Đang cài đặt dependencies...${NC}"
    
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Cài đặt dependencies thành công!${NC}"
        else
            echo -e "${RED}❌ Cài đặt dependencies thất bại!${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ File requirements.txt không tồn tại!${NC}"
        exit 1
    fi
}

# Test proxy connection
test_proxy() {
    echo -e "${BLUE}🔍 Đang test kết nối proxy...${NC}"
    $PYTHON_CMD test_proxy.py
}

# Chạy bot
run_bot() {
    echo -e "${BLUE}🤖 Đang khởi động Telegram Bot...${NC}"
    echo -e "${YELLOW}💡 Bot sẽ tự động ghi nhận các tin nhắn được tag tên${NC}"
    echo -e "${YELLOW}💡 Sử dụng /help để xem các lệnh có sẵn${NC}"
    echo ""
    
    $PYTHON_CMD main.py bot
}

# Chạy dashboard
run_dashboard() {
    echo -e "${BLUE}🌐 Đang khởi động Web Dashboard...${NC}"
    echo -e "${YELLOW}💡 Dashboard sẽ mở tại: http://localhost:5000${NC}"
    echo -e "${YELLOW}💡 Nhấn Ctrl+C để dừng${NC}"
    echo ""
    
    $PYTHON_CMD main.py web
}

# Chạy cả bot và dashboard
run_both() {
    echo -e "${BLUE}🚀 Đang khởi động cả Bot và Dashboard...${NC}"
    echo -e "${YELLOW}💡 Bot sẽ chạy trong background${NC}"
    echo -e "${YELLOW}💡 Dashboard sẽ mở tại: http://localhost:5000${NC}"
    echo -e "${YELLOW}💡 Nhấn Ctrl+C để dừng tất cả${NC}"
    echo ""
    
    $PYTHON_CMD main.py both
}

# Hiển thị hướng dẫn
show_help() {
    echo -e "${CYAN}📖 HƯỚNG DẪN SỬ DỤNG:${NC}"
    echo ""
    echo -e "${YELLOW}Chạy cả bot và dashboard:${NC}"
    echo "  ./run.sh"
    echo ""
    echo -e "${YELLOW}Chỉ chạy bot:${NC}"
    echo "  ./run.sh bot"
    echo ""
    echo -e "${YELLOW}Chỉ chạy dashboard:${NC}"
    echo "  ./run.sh web"
    echo ""
    echo -e "${YELLOW}Test kết nối proxy:${NC}"
    echo "  ./run.sh test"
    echo ""
    echo -e "${YELLOW}Cài đặt dependencies:${NC}"
    echo "  ./run.sh install"
    echo ""
    echo -e "${YELLOW}Hiển thị hướng dẫn này:${NC}"
    echo "  ./run.sh help"
    echo ""
    echo -e "${CYAN}📱 TÍNH NĂNG CHÍNH:${NC}"
    echo "  • Bot tự động ghi nhận công việc khi được tag tên"
    echo "  • Dashboard web để quản lý và theo dõi tasks"
    echo "  • Hỗ trợ proxy cho môi trường công ty"
    echo "  • Thống kê theo người giao việc"
    echo "  • Ghi chú khi hoàn thành task"
    echo ""
}

# Main function
main() {
    print_logo
    
    # Kiểm tra môi trường
    check_python
    check_pip
    check_settings
    
    # Xử lý tham số
    case "${1:-both}" in
        "bot")
            run_bot
            ;;
        "web")
            run_dashboard
            ;;
        "both")
            run_both
            ;;
        "test")
            test_proxy
            ;;
        "install")
            install_dependencies
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Tham số không hợp lệ: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Chạy main function
main "$@"
