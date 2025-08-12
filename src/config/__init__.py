# Configuration package
# Môi trường local - sử dụng development config
from . import settings
from . import production
from . import render_production

# Tạo alias để có thể import settings
globals().update(settings.__dict__)
