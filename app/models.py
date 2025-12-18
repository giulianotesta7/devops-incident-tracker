from database import db
from flask_login import UserMixin

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    comments = db.relationship("Comment",back_populates="incident",cascade="all, delete-orphan",lazy="select")
    creator = db.relationship("User", back_populates="incidents")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    incident = db.relationship("Incident", back_populates="comments")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    incidents = db.relationship("Incident", back_populates="creator")