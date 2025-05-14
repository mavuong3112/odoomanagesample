# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date


class Teacher(models.Model):
    _name = 'language.center.teacher'
    _description = 'Teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Họ và tên', required=True, tracking=True)
    code = fields.Char('Mã giáo viên', required=True, tracking=True)
    date_of_birth = fields.Date('Ngày sinh')
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính')
    phone = fields.Char('Số điện thoại')
    email = fields.Char('Email')
    address = fields.Text('Địa chỉ')
    date_hired = fields.Date('Ngày tuyển dụng', default=fields.Date.today)
    language_ids = fields.Many2many('language.center.language', string='Ngôn ngữ giảng dạy')
    course_ids = fields.One2many('language.center.course', 'teacher_id', string='Khóa học đang dạy')
    qualification = fields.Text('Bằng cấp/Chứng chỉ')
    experience = fields.Text('Kinh nghiệm giảng dạy')
    active = fields.Boolean('Active', default=True)
    image = fields.Binary('Ảnh')
    
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Mã giáo viên phải là duy nhất!')
    ]
    
    @api.model
    def create(self, vals):
        # Auto-generate teacher code if not provided
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('language.center.teacher') or 'TCH-001'
        return super(Teacher, self).create(vals)
    
    def unlink(self):
        # Check if teacher is assigned to any course
        for teacher in self:
            if teacher.course_ids:
                raise models.ValidationError(_('Không thể xóa giáo viên này vì đang được phân công giảng dạy!'))
        return super(Teacher, self).unlink()
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        for teacher in self:
            if teacher.date_of_birth:
                today = date.today()
                teacher.age = today.year - teacher.date_of_birth.year - \
                    ((today.month, today.day) < (teacher.date_of_birth.month, teacher.date_of_birth.day))
            else:
                teacher.age = 0
    
    age = fields.Integer(string='Tuổi', compute='_compute_age', store=True)
    
    def name_get(self):
        result = []
        for teacher in self:
            name = f"{teacher.name} [{teacher.code}]"
            result.append((teacher.id, name))
        return result 