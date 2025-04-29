from app import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }