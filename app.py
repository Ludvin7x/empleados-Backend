from app import create_app
from app.db import init_db
import os

app = create_app()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)