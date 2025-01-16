from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    active_membership = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    memberships = db.relationship('Membership', back_populates='member', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', back_populates='member', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='member', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Member('{self.name}', '{self.email}')"

class Membership(db.Model):
    __tablename__ = "membership"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    type = db.Column(db.Enum("Monthly","Three-month","Yearly"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)

    member = db.relationship('Member', back_populates='memberships')
    payments = db.relationship('Payment', back_populates='membership', cascade='all, delete-orphan')

    
class Trainer(db.Model):
    __tablename__ = "trainer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    classes = db.relationship('Class', back_populates='trainer', cascade='all, delete-orphan')


class Class(db.Model):
    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainer.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    canceled = db.Column(db.Boolean, default=False)

    trainer = db.relationship('Trainer', back_populates='classes')
    reservations = db.relationship('Reservation', back_populates='class_info', cascade='all, delete-orphan')

class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    cancelled = db.Column(db.Boolean, default=False)

    member = db.relationship('Member', back_populates='reservations')
    class_info = db.relationship('Class', back_populates='reservations')

class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    membership_id = db.Column(db.Integer, db.ForeignKey("membership.id"), nullable=True)
    total_price = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.Enum("Cash","Card","Online"), nullable=False)

    member = db.relationship('Member', back_populates='payments')
    membership = db.relationship('Membership', back_populates='payments')

