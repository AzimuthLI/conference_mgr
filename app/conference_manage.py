from flask import (Blueprint, flash, g, redirect, request, url_for)
from werkzeug.exceptions import abort
from app.auth import login_required

bp = Blueprint('conference_manage', __name__)


