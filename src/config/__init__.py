# Configuration package
# Môi trường local - sử dụng development config
from . import settings
# Tạo alias để có thể import settings
globals().update(settings.__dict__)
