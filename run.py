from src import app
from src.db import Base, engine, db
from src.crud import create_admin_account
from src import models


models.Base.metadata.create_all(bind=engine)
create_admin_account(db())
# app.run(debug=True, port=5000)
