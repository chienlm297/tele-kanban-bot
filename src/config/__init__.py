# Configuration package
import os

# Kiểm tra môi trường để quyết định import config nào
if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RENDER') or os.getenv('HEROKU'):
    # Môi trường cloud - sử dụng production config
    from . import production
    # Tạo alias để có thể import settings
    globals().update(production.__dict__)
    settings = production
else:
    # Môi trường local - sử dụng development config
    from . import settings
    # Tạo alias để có thể import settings
    globals().update(settings.__dict__)
