import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime


class bg(models.Model):
    _name = 'hospital.bloodgroup'
    _rec_name = 'bg'
    bg = fields.Char(string="Blood group")


class doc(models.Model):
    _name = 'doctor.document'
    _rec_name = 'documentname'

    documentname = fields.Char(string='Document Name')
    documents = fields.Binary(string="Documents")


class docu(models.Model):
    _name = 'doct.document'
    _rec_name = 'docnames'

    docnames = fields.Char(string='Document Name')
    documents = fields.Binary(string="Documents")


class sdoc(models.Model):
    _name = 'stud.document'
    _rec_name = 'sdocnames'

    sdocnames = fields.Char(string='Document Name')
    sdocuments = fields.Binary(string="Documents")


class hospitaldoc(models.Model):
    _name = 'hospital.doc'

    hospitaldname = fields.Char(string='Document Name')
    hdocuments = fields.Binary(string="Document")


# class SaleOrderInherit(models.Model):
# _inherit = 'sale.order'
#  Doctor_name = fields.Char(string="Name")
# class SaleOrderLineInherit(models.Model):
#   _inherit = 'sale.order.line'
#  Doctor_name = fields.Char(string="Name")


class Hospital(models.Model):
    _name = 'hospital.management'
    _rec_name = 'name'
    _inherit = 'mail.thread'

    dForm = fields.Char(string="Form no", readonly=True, required=True, copy=False, default='New')
    Doctor_photo = fields.Binary(string='Photo')
    name = fields.Char(string="Name")
    Doctor_Address = fields.Char(string="Address")
    Doctor_Address1 = fields.Char(string='   ')
    Mobile_number = fields.Char(string="Mobile number")
    dob = fields.Date(string='D.O.B')
    Doctor_country = fields.Many2one('res.country', string='Country')
    state = fields.Many2one('res.country.state', string='State')
    city_name = fields.Char(string='City')
    dpincode = fields.Char(string='Pin code')
    CurrentHospital = fields.Char(string='Current Hospital')
    login = fields.Char(string='Email')
    Doctor_Education = fields.Char(string="Education")
    License_Number = fields.Char(string="License number")
    certificate = fields.Binary(string='Upload certificate', attachment="true")
    HospitalHistorylist = fields.Many2many('hospital.history', string='Hospital Name')
    Experience = fields.Char(string='Experience')
    DegreeFromInstitute = fields.Char(string='Degree From Institute')
    age = fields.Char(string='Age', compute='_compute_age')
    Gender = fields.Selection([('5', 'Male'), ('6', 'Female')], string='Gender')
    BloodGroup = fields.Many2one('hospital.bloodgroup', string='Blood Group')
    MaritialStatus = fields.Selection([('11', 'Married'), ('22', 'Unmarried'), ('32', 'Divorcee')],
                                      string='Maritial Status')
    OtherClinic = fields.Char(string='Other Clinic\Hospital')
    specialization = fields.Char(string='Specialization')
    Docuname = fields.Many2many('doct.document', string='Document name')
    signature = fields.Binary(string="Upload Signature", attachment="true")

    # @api.multi
    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                delta = relativedelta(datetime.now().date(), record.dob)
                record.age = "{} Years".format(delta.years)
            else:
                record.age = ""

    # @api.onchange('login')
    # def vali_email(self):
    #     for record in self:
    #         if record.login:
    #             match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', record.login)
    #             if match is None:
    #                 raise ValidationError('Not a valid E-mail ID')
    @api.onchange('login')
    def validate_email(self):
        for record in self:
            if record.login:
                if not re.match(r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$', record.login):
                    raise ValidationError('Invalid email address')

    #
    # @api.onchange('dpincode')
    # def validate_dpincode(self):
    #     for record in self:
    #         if record.dpincode:
    #             match = re.match('^[1-9][0-9]{5}$', record.dpincode)
    #             if not match:
    #                 raise ValidationError('Invalid pincode')
    #
    @api.model
    def create(self, vals):
        if vals.get('dForm', 'New') == 'New':
            vals['dForm'] = self.env['ir.sequence'].next_by_code('hospital.management') or 'New'
        result = super(Hospital, self).create(vals)
        return result

    #
    #
    @api.onchange('Mobile_number')
    def validate_Mobile_number(self):
        for record in self:
            if record.Mobile_number:
                match = re.match('^[0-9]{10}$', record.Mobile_number)
                if not match:
                    raise ValidationError('Mobile number is invalid. (Only 10 digits are allowed)')


class Historylist(models.Model):
    _name = 'hospital.history'
    _inherit = 'mail.thread'
    _rec_name = 'hospital_name'

    hospital_name = fields.Char(string='Name')
    hospital_address = fields.Char(string='Address')
    hospital_country = fields.Many2one('res.country', string='Country')
    hospital_state = fields.Many2one('res.country.state', string='State')
    hospital_zip = fields.Integer(string='Zip')
    hospital_number = fields.Char(string='hospital number')
    emergency_number = fields.Char(string='Emergency number')
    ambulance_number1 = fields.Char(string='Ambulance number')
    ambulance_number2 = fields.Char(string='     ')
    ambulance_number3 = fields.Char(string='     ')
    Type = fields.Selection(
        [('1', 'Multispeciality Hospital'), ('2', 'Teaching-cum- Research Hospital'), ('3', 'General Hospital'),
         ('4', 'Ayurvedic Hospital'), ('5', 'Homeopathic hospital'), ('6', 'Unani Hospital'),
         ('7', 'Medical College Hospital'), ('8', 'Private Hospital'), ('9', 'Other')], string='Type')
    docname = fields.Many2many('hospital.management', string='Doctors')
    hospitalicense_Number = fields.Char(string="License number")
    Establish = fields.Char(string='Established in')
    Logo = fields.Binary(string='Logo')
    Gstno = fields.Integer(string='Gst no')
    beds = fields.Integer(string='Total no. of beds ')
    theatre = fields.Integer(string='No. of operation theatre')
    nonicu = fields.Integer(string='In patient beds(Non ICU)')
    icu = fields.Integer(string='In patient beds(ICU)')
    Oxygen = fields.Integer(string='Oxygen Tanks')
    hospital_department = fields.Many2many('hospital.department', string='Hospital department ')
    hospital_email = fields.Char(string='Email')
    hdname = fields.One2many('hospital.doc', 'hospitaldname', string='Document name')
    hwebsite = fields.Char(string='Website')
    registraionNo = fields.Char(string="Registration no")

    @api.onchange('ambulance_number3')
    def validate_ambulance_number3(self):
        for record in self:
            if record.ambulance_number3:
                match = re.match('^[0-9]{10}$', record.ambulance_number3)
                if not match:
                    raise ValidationError('Invalid number for ambulance')

    @api.onchange('ambulance_number2')
    def validate_ambulance_number2(self):
        for record in self:
            if record.ambulance_number2:
                match = re.match('^[0-9]{10}$', record.ambulance_number2)
                if not match:
                    raise ValidationError('Invalid number for ambulance')

    @api.onchange('ambulance_number1')
    def validate_ambulance_number1(self):
        for record in self:
            if record.ambulance_number1:
                match = re.match('^[0-9]{10}$', record.ambulance_number1)
                if not match:
                    raise ValidationError('Invalid number for ambulance')

    @api.onchange('hospital_email')
    def validate_email(self):
        for record in self:
            if record.hospital_email:
                if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                self.hospital_email):
                    raise ValidationError('Invalid email address')

    @api.onchange('emergency_number')
    def validate_emergency_number(self):
        for record in self:
            if record.emergency_number:
                match = re.match('^[0-9]{10}$', record.emergency_number)
                if not match:
                    raise ValidationError('Invalid number for ambulance')

    @api.onchange('hospital_number')
    def validate_hospital_number(self):
        for record in self:
            if record.hospital_number:
                match = re.match('^[0-9]{10}$', record.hospital_number)
                if not match:
                    raise ValidationError('Invalid hospital number')

    @api.onchange('hwebsite')
    def validate_url(self):
        for record in self:
            if record.hwebsite:
                match = re.match(
                    r"((http|https)://)(www.)?" + r"[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\.[a-z]" + r"{2,6}\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)",
                    record.hwebsite)
                if match is None:
                    raise ValidationError('Not a valid URL')


class department(models.Model):
    _name = 'hospital.department'
    _rec_name = 'dname'
    dname = fields.Char(string='Department name')


#  -----------------patient-------------------------------------------------------------------------------------#


class patient(models.Model):
    _name = 'patients'
    _inherit = 'mail.thread'

    _rec_name = 'name'

    name = fields.Char(string="Name")
    patient_adharnumber = fields.Char(string="Aaadhar number")
    patient_country = fields.Many2one('res.country', string="Country")
    pstate = fields.Many2one('res.country.state', string="State")
    patient_city = fields.Char(string="City")
    pincode = fields.Char(string=" ")
    homephone = fields.Char(string="Home phone")
    patient_address = fields.Char(string="Address")
    patient_address1 = fields.Char(string=" ")
    age = fields.Char(string='Age', compute='_compute_age')
    Bloodgroup = fields.Many2one('hospitalbg', string='Blood group')
    Consuming_alcohol = fields.Selection([('0', 'Yes'), ('1', 'No')], string="Consuming alcohol")
    Smoking = fields.Selection([('0', 'Yes'), ('1', 'No')], string="Smoking")
    Doctor_prescription = fields.One2many('prescription', 'presc', string="Prescription")
    checkup = fields.Date(string="Last body check up")
    checkupdoc = fields.Binary(string="Last prescription", attachment="true")
    Past_doctor = fields.Selection([('0', 'Yes'), ('1', 'No')], string='Past doctor')
    # doctorpre = fields.Many2many('doct', string="Prescription")
    # doctornm = fields.Many2many('doct', string="Past doctor details")
    Security_relation = fields.Char(string="Security relation")
    renual_alert = fields.Selection([('0', 'Yes'), ('1', 'No')], string='Renual alert')
    marital_status = fields.Selection([('0', 'Married'), ('1', 'Unmarried'), ('2', 'Divorcee')],
                                      string="Marital status")
    Height = fields.Char(string="Height (in cm)")
    Weight = fields.Char(string="Weight (in kg)")
    Gaurdian_name = fields.Char(string="Gaurdian name")
    Gaurdian_phone = fields.Char(string="Gaurdian phone")
    occupation = fields.Char(string="Occupation")
    occupation_address = fields.Char(string="Occupation address")
    Image = fields.Binary("Photo", help="Photo")
    ltdisease = fields.Many2many('lifedisease', string="Lifetime disease")
    diseasepre = fields.Char(string="Lifetime disease description")
    mdname = fields.Many2many('mdisease', string="Major disease name")
    all = fields.Many2many('allergy', string="Allergy name")
    names = fields.Char(string="Form number", readonly=True, required=True, copy=False, default='New')
    mobilephone = fields.Char(string="Mobile number")
    login = fields.Char(string="Email ID")
    emergency_number = fields.Char(string="Emergency number")
    pGender = fields.Selection([('0', 'Female'), ('1', 'Male')], string="Gender")
    Birthdate = fields.Date(string="Birthdate")
    insuranceno = fields.Many2many('ins', string="  ")
    Docname = fields.Many2many('doctor.document', string='Document details')
    admittedtype = fields.Selection([('0', 'ADMITTED'), ('1', 'NOT ADMITTED')], string="Admission type")
    tamc = fields.Selection([('0', 'Yes'), ('1', 'No')], string="Taking any medication currently")
    ifyesnotes = fields.Text(string="List of medicines")
    roomtype = fields.Selection(
        [('0', 'ICU'), ('1', 'General ward'), ('2', 'Causality'), ('3', 'CCU'), ('4', 'Semi-special room'),
         ('5', 'Special ward'), ('6', 'Deluxe room')], string="Ward type")
    roomno = fields.Many2one('icurn', string="Room no")
    roomno1 = fields.Many2one('icurn', string="Room no")
    roomno2 = fields.Many2one('icurn', string="Room no")
    roomno3 = fields.Many2one('icurn', string="Room no")
    roomno4 = fields.Many2one('icurn', string="Room no")
    roomno5 = fields.Many2one('icurn', string="Room no")
    roomno6 = fields.Many2one('icurn', string="Room no")
    visit = fields.Char(string='Visitor')
    v = fields.Many2one('patient_visitor')

    #
    @api.onchange('Patient_name')
    def _onchange_Patient_name(self):
        if self.Patient_name:
            self.contact = self.Patient_name.mobilephone

    @api.depends('Birthdate')
    def _compute_age(self):
        for record in self:
            if record.Birthdate:
                delta = relativedelta(datetime.now().date(), record.Birthdate)
                record.age = "{} Years".format(delta.years)
            else:
                record.age = ""

    # @api.onchange('v')
    # def _compute_field_value(self):
    #     for rec in self:
    #         if rec.v.pname:
    #             rec.visit = rec.v.vname

    # @api.depends('v')
    # def _compute_field_value(self):
    #     for each in self:
    #         each.visit = each.v.vname
    @api.onchange('homephone')
    def validate_homephone(self):
        for record in self:
            if record.homephone:
                match = re.match('^[0-9]{10}$', record.homephone)
                if not match:
                    raise ValidationError('Invalid phone number')

    @api.onchange('patient_adharnumber')
    def validate_adhar_number(self):
        if self.patient_adharnumber:
            match = re.match('^[0-9]{12}$', self.patient_adharnumber)
            if not match:
                raise ValidationError('Invalid Number (Only 12 digits are allowed)')

    @api.onchange('mobilephone')
    def validate_mobilephone(self):
        for record in self:
            if record.mobilephone:
                match = re.match('^[0-9]{10}$', record.mobilephone)
                if not match:
                    raise ValidationError('Invalid mobile number')

    @api.onchange('login')
    def validate_login(self):
        for record in self:
            if record.login:
                if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                self.login):
                    raise ValidationError('Invalid email address')

    #
    #

    #
    # #@api.onchange('Gaurdian_name')
    # #def validate_gaurdian_name(self):
    #     #if self.Gaurdian_name:
    #        # match = re.match(r"^[ a-zA-Z]{25}$", self.Gaurdian_name)
    #        # if not match:
    #            # raise ValidationError('Invalid(Only characters are allowed)')
    #
    # @api.onchange('emergency_number')
    # def validate_emergency_number(self):
    #     for record in self:
    #         if record.emergency_number:
    #             match = re.match('^[0-9]{10}$', record.emergency_number)
    #             if not match:
    #                 raise ValidationError('Invalid emergency_number number')
    #
    #         raise ValidationError('Invalid emergency number(Only 10 digits are allowed)')

    @api.model
    def create(self, vals):
        if vals.get('names', 'New') == 'New':
            vals['names'] = self.env['ir.sequence'].next_by_code(
                'patients') or 'New'
        result = super(patient, self).create(vals)
        return result
    #
    #
    #
    #
    # @api.onchange('dname')
    # def _onchange_ldescription(self):
    #     if self.dname:
    #         self.diseasepre = self.dname.ldescription
    #
    #
    @api.onchange('pincode')
    def validate_pincode(self):
        if self.pincode:
            match = re.match('^[1-9][0-9]{5}$', self.pincode)
            if not match:
                return {
                    'warning': {
                        'title': 'Invalid Pincode',
                        'message': 'Invalid pincode. Only digits are allowed.'
                    }
                }
    # @api.onchange('pincode')
    # def validate_pincode(self):
    #     if self.pincode:
    #         match = re.match('^[1-9][0-9]{5}$', self.pincode)
    #         if not match:
    #             raise ValidationError('Invalid pincode(Only digits are allowed)')
    #
    #


class icuroom(models.Model):
    _name = 'icurn'
    _rec_name = 'IcuRoomno'
    IcuRoomno = fields.Char(string="Room no")


class Lifetimedisease(models.Model):
    _name = 'lifedisease'
    _rec_name = 'ldiseasename'

    ldiseasename = fields.Char(string="lifetime disease name")
    ldescription = fields.Char(string="lifetime disease description")


class Majortimedisease(models.Model):
    _name = 'mdisease'
    _rec_name = 'mdiseasename'
    mdiseasename = fields.Char(string="Major disease name")


class alergies(models.Model):
    _name = 'allergy'
    _rec_name = 'aname'
    aname = fields.Char(string="Allergy name")


class bg(models.Model):
    _name = 'hospitalbg'
    _rec_name = 'BloodGroup'
    BloodGroup = fields.Char(string="Blood group")


class doctor(models.Model):
    _name = 'doct'

    doctor_name = fields.Char(string="doctor name")
    doctor_pre = fields.Binary(string="doctor prescription", attachment="true")


class Dprescription(models.Model):
    _name = 'prescription'
    _rec_name = 'Patient_name'
    Patient_name = fields.Many2one('patients', string="Patient name")
    contact = fields.Char(string="Contact")
    medsname = fields.Many2many('medicine', string="Medicine details")
    presc = fields.Char(string="Prescription")
    bydoctor = fields.Many2one('hospital.management', string="By doctor/Examiner")
    emailadd = fields.Char(string="Email Id")
    patient_age = fields.Char(string="Age")
    patient_gender = fields.Selection([('0', 'Female'), ('1', 'Male')], string="Gender")
    company1 = fields.Many2one('res.partner')
    prenames = fields.Char(string="Form number", readonly=True, required=True, copy=False, default='New')

    lt = fields.Text(string="lab test ")

    @api.onchange('Patient_name')
    def _onchange_Patient_name(self):
        if self.Patient_name:
            self.contact = self.Patient_name.mobilephone
            self.emailadd = self.Patient_name.login
            self.patient_age = self.Patient_name.age  # Assuming 'age' is the field name in the 'Patient_name' model
            self.patient_gender = self.Patient_name.pGender  # Assuming 'gender' is the field name in the 'Patient_name' model

    @api.model
    def create(self, vals):
        if 'prenames' not in vals or vals.get('prenames') == 'New':
            vals['prenames'] = self.env['ir.sequence'].next_by_code('prescription') or 'New'
        return super(Dprescription, self).create(vals)

    def action_done(self):
        self.contact = 'done'


class Medicine(models.Model):
    _name = 'medicine'
    _rec_name = 'mname'
    _inherit = 'mail.thread'
    # medicine_name=fields.Many2one('medicinelists',string="Medicine name")
    mname = fields.Many2one('medicinelists', string="Medicine")
    Morning = fields.Boolean('Morning')
    Night = fields.Boolean('Night')
    Afternoon = fields.Boolean('Afternoon')
    Evening = fields.Boolean('Evening')
    MAN = fields.Boolean('Morning-Afternoon-Night')
    MN = fields.Boolean('Morning-Night')
    AN = fields.Boolean('Afternoon-Night')
    Quantity = fields.Many2one('quantities', string="Quantity")

    # medslist=fields.Many2one('medicinelists',string="Medicine name")

    class Qua(models.Model):
        _name = 'quantities'
        _rec_name = 'qty'

        qty = fields.Char(string="Quantity")

    class Medicinelist(models.Model):
        _name = 'medicinelists'
        _rec_name = 'medlist'
        medlist = fields.Char(string="Medicine name")

    # @api.onchange('emailadd')
    # def validate_mailadd(self):
    #     if self.emailadd:
    #         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.emailadd)
    #         if match ==  None:
    #             raise ValidationError('Not a valid E-mail ID')
    @api.onchange('contact')
    def validate_contact(self):
        for record in self:
            if record.contact:
                match = re.match('^[0-9]{10}$', record.contact)
                if not match:
                    raise ValidationError('Invalid mobile number')

    # @api.onchange('contact')
    # def validate_phone_number(self):
    #     if self.contact:
    #         match = re.match('^[0-9]{10}$', self.contact)
    #         if not match:
    #             raise ValidationError('Invalid contact number(Only 10 digits are allowed)')


class Bydoctors(models.Model):
    _name = 'bydoct'
    _rec_name = 'bdoctor_name'

    bdoctor_name = fields.Char(string=" By doctor")


class insurance(models.Model):
    _name = 'ins'
    _rec_name = 'insurance_no'
    insurance_no = fields.Char(string="Policy number")
    insurance_name = fields.Char(string="Plan")
    insurance_provider = fields.Char(string="Provider")
    Group_no = fields.Char(string="Group number")
    Subscriberfn = fields.Char(string="Subscriber first name")
    Subscribermn = fields.Char(string="Subscriber middle name")
    Subscriberln = fields.Char(string="Subscriber Last name")
    Subscriberrel = fields.Char(string="Subscriber relationship")


#   STUDENT


class collegeName(models.Model):
    _name = 'student.college'

    _rec_name = 'cname'

    cname = fields.Char(string=" Previous college name")
    cadd = fields.Char(string="College address")


class medicaldept(models.Model):
    _name = 'medicaldepartment'
    _rec_name = 'md'
    md = fields.Char(string="medical dept")


class bloodgroup(models.Model):
    _name = 'student_bg'
    _rec_name = 'bg'
    bg = fields.Char(string="Blood-Group")


class Student_Hospital(models.Model):
    _name = 'hospital.student'
    _inherit = 'mail.thread'

    Form = fields.Char(string="Form no", readonly=True, required=True, copy=False, default='New')
    student_picture = fields.Binary(string='Student picture')
    prn = fields.Char(string="PRN number")
    name = fields.Char(string="Student name")
    gender = fields.Selection([('0', 'Male'), ('1', 'Female'), ('2', 'Other')], string="Gender")
    Student_college = fields.Char(string="Student college")
    Student_Address = fields.Char(string="Student address")
    line2 = fields.Char(string="   ")
    percuing_year = fields.Char(string="Percuing year")
    clg_idcard = fields.Binary(string='Attach your college Id-card', attachment="true")
    speciality = fields.Char(string="Speciality")
    Aadhaar = fields.Char(string="Aadhaar number")
    dob = fields.Date(string="Date Of Birth")
    Student_city = fields.Char(string='City')
    State = fields.Many2one('res.country.state', string='State')
    country = fields.Many2one('res.country', string='Country')
    Area_code = fields.Char(string='Area code')
    Student_education = fields.Char(string='Student education')
    login = fields.Char(string="Email")
    Mobileno = fields.Char(string="Mobile number")
    AlternateMob = fields.Char(string="Alternate mobile number")
    degree = fields.Selection([('0', 'Yes'), ('1', 'No')], string='Degree')
    specify = fields.Many2one('medicaldepartment', string="specification")
    # other = fields.Char(string="Other", compute = "_compute_other")
    clgname = fields.Many2one('student.college', string='College name')
    clgadd = fields.Char(string='College address')
    sdocument = fields.Binary(string='documents', attachment="true")
    bloodgroup = fields.Many2one('student_bg', string="Blood-group")
    studentdocname = fields.Many2many('stud.document', string='Document Details')

    # @api.onchange('Area_code')
    # def validate_Area_code(self):
    #     if self.Area_code:
    #         match = re.match('^[1-9][0-9]{5}$', self.Area_code)
    #         if not match:
    #             raise ValidationError('Invalid Area code(Only 6 digits are allowed)')
    #
    # '''@api.depends('specify')
    # def _compute_other(self):
    #     if self.specify == "Other":
    #         self.specify = True
    #     else:
    #         self.specify = False'''
    #
    #
    #
    #
    #
    @api.model
    def create(self, vals):
        if vals.get('Form', 'New') == 'New':
            vals['Form'] = self.env['ir.sequence'].next_by_code(
                'hospital.student') or 'New'
        result = super(Student_Hospital, self).create(vals)
        return result
    #
    #
    @api.onchange('Mobileno')
    def validate_Mobileno(self):
        for record in self:
            if record.Mobileno:
                match = re.match('^[0-9]{10}$', record.Mobileno)
                if not match:
                    raise ValidationError('Invalid mobile number')
    # @api.onchange('Mobileno')
    # def validate_Mobile_number(self):
    #     if self.Mobileno:
    #         match = re.match('^[0-9]{10}$', self.Mobileno)
    #         if not match:
    #             raise ValidationError('Invalid Number(Only 10 digits are allowed)')
    #
    #
    # @api.onchange('percuing_year')
    # def validate_percuing_year(self):
    #     if self.percuing_year:
    #         match = re.match('^[0-9]{4}$', self.percuing_year)
    #         if not match:
    #             raise ValidationError('Percuing year should contain only 4 digits')
    #
    # @api.onchange('Aadhaar')
    # def validate_Aadhaar_number(self):
    #     if self.Aadhaar:
    #         match = re.match('^[0-9]{12}$', self.Aadhaar)
    #         if not match:
    #             raise ValidationError('Invalid Aadhaar Number(Only 12 digits are allowed)')
    #
    @api.onchange('AlternateMob')
    def validate_AlternateMob(self):
        for record in self:
            if record.AlternateMob:
                match = re.match('^[0-9]{10}$', record.AlternateMob)
                if not match:
                    raise ValidationError('Invalid mobile number')
    # @api.onchange('AlternateMob')
    # def validate_Alternate_Mobile_number(self):
    #     if self.AlternateMob:
    #         match = re.match('^[0-9]{10}$', self.AlternateMob)
    #         if not match:
    #             raise ValidationError('Invalid alternate Number(Only 10 digits are allowed)')
    #
    # @api.onchange('login')
    # def validate_mail(self):
    #     if self.login:
    #         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.login)
    #         if match == None:
    #             raise ValidationError('Not a valid E-mail ID')
    #
    # @api.onchange('clgname')
    # def onchange_cadd(self):
    #    if self.clgname:
    #        self.clgadd=self.clgname.cadd


# appointment
from odoo import fields, models


class medical_appointment1(models.Model):
    _name = "medical.appointment1"
    _rec_name = 'patient_id'

    appointment_date = fields.Datetime('Appointment Date', required=True, default=fields.Datetime.now)
    appointment_end = fields.Datetime('Appointment End', required=True)
    doctor_id = fields.Many2one('hospital.management', 'Doctor', required=True)
    patient_id = fields.Many2one('patients', string="Patient name", required=True)
    urgency_level = fields.Selection([
        ('a', 'Normal'),
        ('b', 'Urgent'),
        ('c', 'Medical Emergency'),
    ], 'Patient status', sort=False, default="b")
    symptons = fields.Text(string="Symptoms")
    # purpose  radio-new app/rutin chekup
    appointmentno = fields.Char(string="Appointment no", readonly=True, required=True, copy=False, default='New')
    Temp = fields.Char(string='Temperature')
    weight = fields.Char(string='Weight')
    sbp = fields.Char(string='SBP')
    dbp = fields.Char(string='DBP')
    heartrate = fields.Char('Heartrate')
    respiratory_rate = fields.Char('Respiratory rate')

    # @api.depends('appointment_date')  # Add dependency on appointment_date field
    # def _compute_field_value(self):
    #     for record in self:
    #         # Your computation logic here
    #         pass
    #
    # @api.model
    # def create(self, vals):
    #     if vals.get('appointmentno', 'New') == 'New':
    #         vals['appointmentno'] = self.env['ir.sequence'].next_by_code(
    #             'medical.appointment1') or 'New'
    #     result = super(medical_appointment1, self).create(vals)
    #     return result


class visitor(models.Model):
    _name = 'patient_visitor'
    _rec_name = 'vname'

    vname = fields.Char(string='Visitor name', required=True)
    pname = fields.Many2one('patients', string="Patient name", required=True)
    vdate = fields.Datetime(string='Time', required=True)


class employee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee']
    dateofjoin = fields.Datetime(string="Date of joining")


class bloodbank(models.Model):
    _name = 'blood_bank'
    _rec_name = 'Dname'

    Dname = fields.Char(string="Donor's Name")
    Ddob = fields.Date(string='Date of Birth')
    Demail = fields.Char(string='Email')
    Dphone = fields.Char(string='Phone Number')
    DAddress = fields.Char(string="Address")
    DAddress1 = fields.Char(string='   ')
    Dcity = fields.Char(string="City")
    Dcountry = fields.Many2one('res.country', string='Country')
    Dstate = fields.Many2one('res.country.state', string='Sate')
    Doccupation = fields.Char(string='Occupation')

    Dbloodtype = fields.Many2one('hospital.bloodgroup', string='Blood Group')
    Hepatitis = fields.Boolean('Hepatitis')

    Donatedbefore = fields.Selection([('0', 'Yes'), ('1', 'No')], string="Did you ever donate blood before ?")
    Lastblooddonate = fields.Date(string='When was last time you have donate blood ?')

    Disease = fields.Selection([('123', 'Yes'), ('456', 'No')], string="Do you suffer from any disease ?")
    Disease11 = fields.Text(string='Disease')

    alergies = fields.Selection([('789', 'Yes'), ('101', 'No')], string="Do you have allergies ?")
    Alergies11 = fields.Text(string='Alergies')

    bloodtest = fields.Selection([('987', 'Yes'), ('654', 'No')],
                                 string="Have you ever had positive Blood test for HbsAg,Hcv,HIV ?")
    cardiac = fields.Selection([('62', 'Yes'), ('48', 'No')], string="Do you suffer any bleeding disorders ?")

    medication = fields.Selection([('123', 'Yes'), ('456', 'No')], string="Do you take medication ?")
    meds1 = fields.Text(string="Describe the medication you take")


class blooddisease(models.Model):
    _name = 'bd'
    _rec_name = 'dise'
    dise = fields.Char(string='Disease')


class AdmittedPatients(models.Model):
    _name = 'admitted_patients'
    # _rec_name = 'Admitted.Patient'
    # Pid = fields.Char(string="Patient ID", default='New', readonly=True, required=True, copy=False)
    # Pid2 = fields.Char(string="Patient ID", default='New', readonly=True, required=True, copy=False)

    names = fields.Char(string="Patient")
    name = fields.Many2one('patients', string="Patient Name")
    login = fields.Char(string="Email ID")
    mobilephone = fields.Char(string="Mobile number")
    vname = fields.Many2many('patient_visitor', string="Visitor")
    admittedtype = fields.Selection([('0', 'ADMITTED'), ('1', 'NOT ADMITTED')], string="Status")
    pGender = fields.Selection([('0', 'Female'), ('1', 'Male')], string='Gender')
    # History
    Past_doctor = fields.Selection([('0', 'Yes'), ('1', 'No')], string='Past doctor')
    doctornm = fields.Char(string="Past Doctor Details")
    checkup = fields.Date(string="Last body check up")
    checkupdoc = fields.Binary(string="Last prescription", attachment="true")

    tamc = fields.Selection([('0', 'Yes'), ('1', 'No')], string="Taking any medication currently")
    ifyesnotes = fields.Text(string="List of medicines")
    # Photos
    # photos = fields.Many2many('ir.attachment', string="Photos")
    # Medication
    medsname = fields.Many2many('medicine', string="Medicine details")
    # Imaging
    # image = fields.Many2many('ir.attachment', string="Image")
    # Labs
    labs = fields.Many2many('ir.attachment', string="Labs")

    # ward_no = fields.Many2one('patient',string='Ward No')

    # @api.onchange('name')
    # def _onchange_changes(self):
    #     if self.name:
    #         self.login = self.name.login
    #         self.mobilephone = self.name.mobilephone
    #         self.pGender = self.name.pGender
    #         self.admittedtype = self.name.admittedtype
