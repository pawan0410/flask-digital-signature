from extensions import db


class NDAForm(db.Model):
    __tablename__ = 'nda_form'
    id = db.Column(db.Integer, primary_key=True)
    signaturepath = db.Column(db.String(255))
    signaturepath1 = db.Column(db.String(255))
    signaturepath2 = db.Column(db.String(255))
    signaturepath3 = db.Column(db.String(255))
    signaturepath4 = db.Column(db.String(255))
    date1 = db.Column(db.Date)
    date1a = db.Column(db.Date)
    date1b = db.Column(db.Date)
    date3a = db.Column(db.Date)
    date3b = db.Column(db.Date)
    name_2a = db.Column(db.String(255))
    name_2b = db.Column(db.String(255))
    name_3 = db.Column(db.String(255))
    name_3_org_name = db.Column(db.String(255))
    name_3_emp_name = db.Column(db.String(255))
    name_3_emp_title = db.Column(db.String(255))
    IP_addr = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    UserAgent = db.Column(db.String(255))
    OperatingSystem = db.Column(db.String(255))
    Time = db.Column(db.DateTime)