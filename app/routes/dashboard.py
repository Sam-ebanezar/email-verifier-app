from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from ..models import Upload
from .. import db
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('No file uploaded.')
            return redirect(url_for('dashboard.dashboard'))

        filename = secure_filename(file.filename)
        stored_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], stored_filename)
        file.save(file_path)

        new_upload = Upload(user_id=current_user.id, filename=filename, stored_filename=stored_filename, upload_time=datetime.utcnow())
        db.session.add(new_upload)
        db.session.commit()
        flash('File uploaded successfully.')
        return redirect(url_for('dashboard.dashboard'))

    uploads = Upload.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', uploads=uploads)

@bp.route('/download/<filename>')
@login_required
def download(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
