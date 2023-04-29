from .database import db

class Floor(db.Model):
    __tablename__ = 'floor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    selected = db.Column(db.String(255))
    input = db.Column(db.Float)
    hz250 = db.Column(db.Float)
    hz500 = db.Column(db.Float)
    k1 = db.Column(db.Float)
    k2 = db.Column(db.Float)
    k4 = db.Column(db.Float)

    def __init__(self, name, selected, input, hz250, hz500, k1, k2, k4):
        self.name = name
        self.selected = selected
        self.input = input
        self.hz250 = hz250
        self.hz500 = hz500
        self.k1 = k1
        self.k2 = k2
        self.k4 = k4

    @property
    def serialize(self):
        return {
            'id': self.id,
            'input': self.input,
            'selected': self.selected,
            'name': self.name,
            'hz250': self.hz250,
            'hz500': self.hz500,
            'k1': self.k1,
            'k2': self.k2,
            'k4': self.k4,
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]