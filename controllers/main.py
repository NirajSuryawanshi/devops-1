from odoo import http
from odoo.http import request

class Hospital(http.Controller):
   @http.route('/Docto/form', type='http', auth='public', website=True)
   def doc_detail(self, **kw):
       return request.render('hospital.create_doctor', {})

   @http.route('/doctor/form/submit', type='http', auth="public", website=True)
   def create_doctor(self, **kw):
       request.env['hospital_managment'].sudo().create(kw)
       request.env['res.users'].sudo().create(kw)
       return request.render("hospital.doc_success", {})

class student_website(http.Controller):
       @http.route('/student/webform', type="http", auth="public", website=True)
       def student_form(self, **kw):
           return http.request.render('hospital.create_student', {})

       @http.route('/create/webstudent', type="http", auth="public", website=True)
       def create_webstudent(self, **kw):
           print("jjjjjjjjjjjjj", kw)
           request.env['hospital_student'].sudo().create(kw)
           request.env['res.users'].sudo().create(kw)

           return request.render("hospital.student_thanks", {})




class patient_website(http.Controller):
   @http.route('/Patient_form', type='http', auth='public', website=True)
   def pat_detail(self, **kwargs):
       return request.render('hospital.create_patient_form', {})

   @http.route('/patient/form/submit', type="http", auth="public", website=True)
   def create_web(self, **kw):
       print("jjjjjjjjjjjjj", kw)
       request.env['patients'].sudo().create(kw)
       request.env['res.users'].sudo().create(kw)
       return request.render("hospital.patient_submit", {})








