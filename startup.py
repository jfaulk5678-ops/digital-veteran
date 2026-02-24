#!/usr/bin/env python3
# startup.py - Production startup

import os

from gunicorn.app.base import BaseApplication


class FlaskApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application


def run_production():
    """Run with Gunicorn for production"""
    from dashboard import app

    options = {
        "bind": "0.0.0.0:5000",
        "workers": 4,
        "worker_class": "sync",
        "timeout": 120,
        "preload_app": True,
    }

    FlaskApplication(app, options).run()


if __name__ == "__main__":
    # Check if we're in production
    if os.getenv("FLASK_ENV") == "production":
        run_production()
    else:
        # Development mode
        from dashboard import app

        app.run(host="0.0.0.0", port=5000, debug=True)
