{
    'name': "Medical Portal",

    'summary': """Hospital Management""",

    'description': """
        Medical Portal module for managing:
            - Doctors
            - Doctors Card Report
            - Students
            - Students Card Report
            - Patients
            - Patients Card Report
            - Appointments
            - Prescriptions
            - Prescription Report
            - Hospital            
    """,
    'sequence': -100,
    'author': "Nutshell Infosoft Pvt.Ltd",
    'website': "https://www.nutshellinfosoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_sale', 'website', 'sale'],

    # always loaded
    'data': [
        'data/alld.xml',
        'data/lifed.xml',
        'data/medicineslists.xml',
        'data/medquantity.xml',
        'data/roomnumber.xml',
        'data/bloodgroup.xml',
        'data/blooddisease.xml',
        'data/department.xml',
        'data/medical_department.xml',
        'data/student_bloodgroup.xml',
        'data/crondoc.xml',
        'data/patient_bloodgroup.xml',
        'data/majord.xml',

        'report/report.xml',
        'report/hospitalreport.xml',
        'report/student_report.xml',
        'report/doctoreport.xml',
        'report/hospitals.xml',
        'report/newrep.xml',

        'security/hospsecurity.xml',
        'security/ir.model.access.csv',

        'views/demo.xml',
        # 'views/new.xml',
        'views/website_form.xml',
        'views/website_form_student.xml',
        'views/patient_website_form.xml',
        'views/prescription.xml',

        # 'static/description/features/index.html'
    ],
    'i18n': [
        'hi_lN.po',
    ],
    'images': [
        'static/src/img/sc.png',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
