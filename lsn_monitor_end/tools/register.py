import pkgutil
import logging

import os

import lsn_monitor_end


class Register(object):
    def __init__(self, app, exclude_packages=list()):
        core_packages = ["db", "common", "update", "scripts", "tools", "service",
                         "upload",  "es", "public", "tag", "config", "rpc",
                         "resource", "db_full_text", "expand_dict"]
        core_packages.extend(exclude_packages)
        self.flask_app = app
        self.core_packages = core_packages
        self.reg_packages = []
        self.run()

    def get_reg_packages(self):
        pkgpath = os.path.dirname(lsn_monitor_end.__file__)
        for _, name, is_package in pkgutil.iter_modules([pkgpath]):
            if is_package and name not in self.core_packages:
                self.reg_packages.append(name)

    def register(self):
        for package in self.reg_packages:
            module_name = "lsn_monitor_end." + package + ".views"
            try:
                module = __import__(module_name, fromlist=["views"])
                reg = getattr(module, package)
                self.flask_app.register_module(reg, url_prefix="/lsn/" + package) if reg and package else None
            except Exception, e:
                logging.warn("Register: " + str(module_name) + ":" + str(e), exc_info=1)

    def run(self):
        self.get_reg_packages()
        self.register()
