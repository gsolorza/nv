from src import app
from src.db import Base,engine
from src.crud import create_default_accounts


Base.metadata.create_all(bind=engine)
create_default_accounts()
# app.run(debug=True, port=5000)
