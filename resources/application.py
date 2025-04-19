from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import render_template, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

from models.application import ApplicationModel
from models.user import UserModel, AccountType
from schemas import ApplicationSchema
from forms import ApplicationForm
from db import db

blp = Blueprint("Applications", "applications", description="Operations on applications")

@blp.route("/application")
class ApplicationList(MethodView):
    @jwt_required()
    @blp.response(200, ApplicationSchema(many=True))
    def get(self):
        """Get all applications via the API"""
        try:
            # Get current user from JWT token
            current_user_id = get_jwt_identity()
            user = UserModel.query.get(current_user_id)
            
            # Check if user exists and is admin
            if not user or user.account_type != AccountType.ADMIN:
                abort(403, message="Only admin users can access this endpoint")
            
            applications = ApplicationModel.query.all()
            return applications
        except Exception as e:
            abort(500, message=str(e))

    @blp.arguments(ApplicationSchema)
    @blp.response(201, ApplicationSchema)
    def post(self, application_data):
        """Create a new application via the API"""
        try:
            application = ApplicationModel(**application_data)
            db.session.add(application)
            db.session.commit()
            return application
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))



@blp.route("/apply", methods=['GET', 'POST'])
def apply():
    """Create a new application via the webpage form"""
    form = ApplicationForm()
    if form.validate_on_submit():
        
        transcript = form.transcript.data
        id_proof = form.id_proof.data
        
        transcript_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'transcripts')
        id_proof_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'id_proofs')
        os.makedirs(transcript_dir, exist_ok=True)
        os.makedirs(id_proof_dir, exist_ok=True)
        
        transcript_filename = secure_filename(transcript.filename)
        id_proof_filename = secure_filename(id_proof.filename)
        
        transcript_path = os.path.join(transcript_dir, transcript_filename)
        id_proof_path = os.path.join(id_proof_dir, id_proof_filename)
        
        transcript.save(transcript_path)
        id_proof.save(id_proof_path)
        
        application = ApplicationModel(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            dob=form.dob.data,
            email=form.email.data,
            phone=form.phone.data,
            degree=form.degree.data,
            field_of_study=form.field_of_study.data,
            institution=form.institution.data,
            cgpa=form.cgpa.data,
            transcript_filename=transcript_filename,
            id_proof_filename=id_proof_filename
        )
        
        db.session.add(application)
        db.session.commit()
        
        return redirect(url_for('Applications.success'))
    
    return render_template('apply.html', form=form)

@blp.route("/success")
def success():
    """Show success message after application submission"""
    return "Application submitted successfully!"


