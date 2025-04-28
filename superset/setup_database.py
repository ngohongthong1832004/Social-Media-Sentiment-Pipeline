from superset.app import create_app

# Tạo Flask App
app = create_app()
app.app_context().push()

# Sau khi có context, mới import Database
from superset import db
from superset.models.core import Database

# Bắt đầu xử lý
db_name = "Trino"
database = db.session.query(Database).filter_by(database_name=db_name).first()

if not database:
    database = Database(
        database_name=db_name,
        sqlalchemy_uri="trino://admin@trino:8080",
    )
    db.session.add(database)
    db.session.commit()
    print(f"✅ Created Trino database connection successfully.")
else:
    print(f"✅ Trino database connection already exists.")
