import os
import datetime
import base64

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask_mail import Message

from extensions import db
from extensions import mail
from models import NDAForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/aig_nda_form'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = r'kmt.aigbusiness@gmail.com'
app.config['MAIL_PASSWORD'] = r'test@123456'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db.init_app(app)
mail.init_app(app)


def save_signature(base64_str, name_3_emp_name, frm_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', name_3_emp_name)
    file_name = '{}_{}.png'.format(path, frm_name)
    image = base64.b64decode(base64_str.split(',')[1])
    with open(file_name, 'wb') as f:
        f.write(image)
        f.close()
    return file_name


def send_document(**kwargs):
    msg = Message('NDA Form', sender='reset@aigbusiness.in', recipients=[
        'pkaur@aigbusiness.com'
    ])
    msg.html = render_template(
        'document.html',
        signature=kwargs['signature'],
        signature1=kwargs['signature1'],
        signature2=kwargs['signature2'],
        signature3=kwargs['signature3'],
        signature4=kwargs['signature4'],
        nda_1_date=kwargs['nda_1_date'],
        nda2_date_a=kwargs['nda2_date_a'],
        nda2_date_b=kwargs['nda2_date_b'],
        nda3_date_a=kwargs['nda3_date_a'],
        nda3_date_b=kwargs['nda3_date_b'],
        nda2_print_name_a=kwargs['nda2_print_name_a'],
        nda2_print_name_b=kwargs['nda2_print_name_b'],
        nda3_name=kwargs['nda3_name'],
        nda3_org_name=kwargs['nda3_org_name'],
        nda3_employee_name=kwargs['nda3_employee_name'],
        nda3_employer_title=kwargs['nda3_employer_title']
    )
    mail.send(msg)


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/savedata" , methods=['POST'])
def save_data():
    emp_name = request.form.get('nda3_employee_name')
    signature = save_signature(request.form.get('signature'), request.form.get('nda3_employee_name'), 'signature')
    signature1 = save_signature(request.form.get('signature1'), request.form.get('nda3_employee_name'), 'signature1')
    signature2 = save_signature(request.form.get('signature2'), request.form.get('nda3_employee_name'), 'signature2')
    signature3 = save_signature(request.form.get('signature3'), request.form.get('nda3_employee_name'), 'signature3')
    signature4 = save_signature(request.form.get('signature4'), request.form.get('nda3_employee_name'), 'signature4')

    nda_form = NDAForm(
        signaturepath = signature,
        signaturepath1 = signature1,
        signaturepath2 = signature2,
        signaturepath3 = signature3,
        signaturepath4 = signature4,
        date1 = request.form.get('nda_1_date'),
        date1a = request.form.get('nda2_date_a'),
        date1b = request.form.get('nda2_date_b'),
        date3a = request.form.get('nda3_date_a'),
        date3b = request.form.get('nda3_date_b'),
        name_2a = request.form.get('nda2_print_name_a'),
        name_2b = request.form.get('nda2_print_name_b'),
        name_3 = request.form.get('nda3_name'),
        name_3_org_name = request.form.get('nda3_org_name'),
        name_3_emp_name = request.form.get('nda3_employee_name'),
        name_3_emp_title = request.form.get('nda3_employer_title'),
        IP_addr = request.remote_addr,
        Location = request.form.get('location'),
        UserAgent = request.user_agent.browser,
        OperatingSystem = request.user_agent.platform,
        Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    db.session.add(nda_form)
    db.session.commit()

    send_document(
        signature='http://{}/static/uploads/{}_signature.png'.format(request.host, emp_name),
        signature1='http://{}/static/uploads/{}_signature1.png'.format(request.host, emp_name),
        signature2='http://{}/static/uploads/{}_signature2.png'.format(request.host, emp_name),
        signature3='http://{}/static/uploads/{}_signature3.png'.format(request.host, emp_name),
        signature4='http://{}/static/uploads/{}_signature4.png'.format(request.host, emp_name),
        nda_1_date=request.form.get('nda_1_date'),
        nda2_date_a=request.form.get('nda2_date_a'),
        nda2_date_b=request.form.get('nda2_date_b'),
        nda3_date_a=request.form.get('nda3_date_a'),
        nda3_date_b=request.form.get('nda3_date_b'),
        nda2_print_name_a=request.form.get('nda2_print_name_a'),
        nda2_print_name_b=request.form.get('nda2_print_name_b'),
        nda3_name=request.form.get('nda3_name'),
        nda3_org_name=request.form.get('nda3_org_name'),
        nda3_employee_name=request.form.get('nda3_employee_name'),
        nda3_employer_title=request.form.get('nda3_employer_title')
    )

    return redirect('/thankyou')

