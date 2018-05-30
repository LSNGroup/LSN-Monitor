# -*- coding: utf-8 -*-
"""start run webmanage"""
import sys
sys.path.insert(0, "/root/lsn_env/env/")
import os
from apps import create_app

def execute_manager():
    flask_app = create_app()
    flask_app.secret_key = os.urandom(24)
    flask_app.run(debug=True, host='0.0.0.0', port=8888)


def main():
    execute_manager()


if __name__ == "__main__":
    main()


