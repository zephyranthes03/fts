import uvicorn
from app.server.database.common import Inital_database
if __name__ == "__main__":
    Inital_database()

    uvicorn.run("server.app:app", host="0.0.0.0", port=8004, reload=True)