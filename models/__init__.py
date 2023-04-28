import bcrypt
from sqlalchemy import event
from .material import Material
from .database import db


@event.listens_for(Material.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(
        Material("blick",1.0,1.0,1.0,1.0,1.0))
    db.session.commit()

