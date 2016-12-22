"""mylinux bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as BaseController.

from mylinux.cli.controllers.base import BaseController

def load(app):
    app.handler.register(BaseController)
