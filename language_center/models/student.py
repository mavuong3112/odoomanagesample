# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date


class Student(models.Model):
    _name = 'language.center.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Họ và tên', required=True, tracking=True)
    code = fields.Char('Mã học viên', required=True, tracking=True)
    date_of_birth = fields.Date('Ngày sinh')
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính')
    phone = fields.Char('Số điện thoại')
    email = fields.Char('Email')
    address = fields.Text('Địa chỉ')
    course_ids = fields.Many2many('language.center.course', string='Khóa học đã đăng ký')
    active = fields.Boolean('Active', default=True)
    image = fields.Binary('Ảnh')
    
    # Additional fields
    registration_date = fields.Date('Ngày đăng ký', default=fields.Date.today, tracking=True)
    parent_name = fields.Char('Họ tên phụ huynh')
    parent_phone = fields.Char('Số điện thoại phụ huynh')
    attendance_ids = fields.One2many('language.center.attendance', 'student_id', string='Điểm danh')
    course_count = fields.Integer(string='Số khóa học', compute='_compute_course_count', store=True)
    
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Mã học viên phải là duy nhất!')
    ]
    
    @api.depends('course_ids')
    def _compute_course_count(self):
        for student in self:
            student.course_count = len(student.course_ids)
            
    @api.depends('date_of_birth')
    def _compute_age(self):
        for student in self:
            if student.date_of_birth:
                today = date.today()
                student.age = today.year - student.date_of_birth.year - \
                    ((today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day))
            else:
                student.age = 0
    
    age = fields.Integer(string='Tuổi', compute='_compute_age', store=True)
            
    @api.model
    def create(self, vals):
        # Auto-generate student code if not provided
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('language.center.student') or 'STU-001'
        return super(Student, self).create(vals)
    
    def action_view_courses(self):
        self.ensure_one()
        return {
            'name': 'Khóa học',
            'type': 'ir.actions.act_window',
            'res_model': 'language.center.course',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.course_ids.ids)],
        }
    
    def action_view_attendance(self):
        self.ensure_one()
        return {
            'name': 'Điểm danh',
            'type': 'ir.actions.act_window',
            'res_model': 'language.center.attendance',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        } 