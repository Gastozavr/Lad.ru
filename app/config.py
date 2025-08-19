import os

jwt_secret = os.getenv('JWT_SECRET')
pg_username = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_url = os.getenv('PG_HOST')
pg_db = os.getenv('PG_DB')
admin_username = os.getenv('USERNAME', 'admin')
admin_password = os.getenv('PASSWORD', 'admin')