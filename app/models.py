from database import db
from flask_login import UserMixin

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    comments = db.relationship("Comment",back_populates="incident",cascade="all, delete-orphan",lazy="select")
    creator = db.relationship("User", foreign_keys=[created_by_id], back_populates="created_incidents")
    assignee = db.relationship("User", foreign_keys=[assigned_to_id],back_populates="assigned_incidents")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commented_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_system = db.Column(db.Boolean, nullable=False, default=False)

    commenter = db.relationship("User", foreign_keys=[commented_by_id], back_populates="comments")
    incident = db.relationship("Incident", back_populates="comments")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    comments = db.relationship("Comment", foreign_keys="Comment.commented_by_id", back_populates="commenter", cascade="all, delete-orphan", lazy="select")
    created_incidents  = db.relationship("Incident", foreign_keys="Incident.created_by_id", back_populates="creator")
    assigned_incidents = db.relationship("Incident", foreign_keys="Incident.assigned_to_id", back_populates="assignee")
