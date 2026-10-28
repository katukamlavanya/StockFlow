# StockFlow — Inventory Management MVP

A ready-to-run Django inventory management app with organization-scoped products, signup/login, dashboard metrics, low-stock tracking, search, product CRUD, and organization settings.

## Quick start (Windows)

1. Extract the `StockFlow.zip` folder.
2. Open Command Prompt in the extracted `StockFlow` folder (the folder containing `manage.py`).
3. Run:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python manage.py makemigrations organizations accounts inventory
   python manage.py migrate
   python manage.py runserver
   ```

4. Open `http://127.0.0.1:8000/` in your browser.
5. Create an account and organization from the Sign up page.

A Windows helper file `run_stockflow.bat` automates setup and starts the server. Run it from the extracted folder if you prefer.

## Database

For quickest setup, StockFlow uses SQLite by default. It creates `db.sqlite3` locally and requires no database server.

To use MySQL instead, set these environment variables before running Django:
- `STOCKFLOW_DB_ENGINE=mysql`
- `STOCKFLOW_DB_NAME=stockflow_db`
- `STOCKFLOW_DB_USER=your_mysql_user`
- `STOCKFLOW_DB_PASSWORD=your_mysql_password`
- `STOCKFLOW_DB_HOST=localhost`
- `STOCKFLOW_DB_PORT=3306`

Install a compatible MySQL driver in your virtual environment (`pip install mysqlclient`) and then run migrations. Do not put real passwords into source control.

## Main features

- Organization signup and Django authentication
- Each signed-in user sees only products belonging to their organization
- Dashboard metrics: product count, total quantity, low-stock count
- Create, edit, and delete products
- Search by product name or SKU
- Per-product low-stock threshold, falling back to organization default
- Organization settings for default low-stock threshold
- Django admin support

## Notes

- This is a development MVP. Before production deployment, configure a strong secret key via environment variables, set `DEBUG=False`, configure `ALLOWED_HOSTS`, enable HTTPS/security settings, and use a production database.
- Bootstrap is loaded from its public CDN, so the browser needs internet access for the styling.
