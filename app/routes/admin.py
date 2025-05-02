from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Upload
from .. import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('dashboard.dashboard'))

    users = User.query.all()
    uploads = Upload.query.order_by(Upload.upload_time.desc()).all()
    return render_template('admin_dashboard.html', users=users, uploads=uploads)
