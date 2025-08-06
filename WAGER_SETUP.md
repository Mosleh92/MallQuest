# Wager Module Setup

This guide walks through preparing and integrating the optional **MallQuest Wager** module.

## 1. Run database migrations
```bash
flask db migrate -m "wager tables"
flask db upgrade
```

## 2. Register the Wager blueprint
Add the following to your Flask application after creating the `app` instance:
```python
from mallquest_wager.routes import wager_bp
app.register_blueprint(wager_bp, url_prefix="/wager")
```

## 3. Seed the wager catalog
```bash
python - <<'PY'
from mallquest_wager.wager_wheel import seed_catalog
seed_catalog()
PY
```

## 4. Start the server and access wager routes
Launch the application and navigate to the wager section:
```bash
python web_interface.py
```
Then open `http://localhost:5000/wager` in your browser to explore the wager features.
