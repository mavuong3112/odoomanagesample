# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Course(models.Model):
    _name = 'language.center.course'
    _description = 'Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, name'

    name = fields.Char('Tên khóa học', required=True, tracking=True)
    code = fields.Char('Mã khóa học', required=True, tracking=True)
    description = fields.Text('Mô tả')
    language_id = fields.Many2one('language.center.language', string='Ngôn ngữ', required=True, tracking=True)
    teacher_id = fields.Many2one('language.center.teacher', string='Giáo viên phụ trách', tracking=True)
    start_date = fields.Date('Ngày bắt đầu', required=True, tracking=True)
    end_date = fields.Date('Ngày kết thúc', required=True, tracking=True)
    fee = fields.Float('Học phí', digits=(16, 0))
    max_students = fields.Integer('Số học viên tối đa')
    student_ids = fields.Many2many('language.center.student', string='Học viên')
    class_schedule_ids = fields.One2many('language.center.class.schedule', 'course_id', string='Lịch học')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirm', 'Xác nhận'),
        ('in_progress', 'Đang diễn ra'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy')
    ], string='Trạng thái', default='draft', tracking=True)
    active = fields.Boolean('Active', default=True)
    
    # Additional fields
    level = fields.Selection([
        ('beginner', 'Sơ cấp'),
        ('intermediate', 'Trung cấp'),
        ('advanced', 'Cao cấp'),
    ], string='Cấp độ', default='beginner', required=True)
    student_count = fields.Integer(string='Số học viên', compute='_compute_student_count', store=True)
    class_count = fields.Integer(string='Số buổi học', compute='_compute_class_count', store=True)
    
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Mã khóa học phải là duy nhất!')
    ]
    
    @api.depends('student_ids')
    def _compute_student_count(self):
        for course in self:
            course.student_count = len(course.student_ids)
    
    @api.depends('class_schedule_ids')
    def _compute_class_count(self):
        for course in self:
            course.class_count = len(course.class_schedule_ids)
    
    @api.model
    def create(self, vals):
        # Auto-generate course code if not provided
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('language.center.course') or 'CRS-001'
        return super(Course, self).create(vals)
    
    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    def action_in_progress(self):
        self.write({'state': 'in_progress'})
        
    def action_done(self):
        self.write({'state': 'done'})
        
    def action_cancel(self):
        self.write({'state': 'cancel'})
        
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_view_students(self):
        self.ensure_one()
        return {
            'name': 'Học viên',
            'type': 'ir.actions.act_window',
            'res_model': 'language.center.student',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.student_ids.ids)],
        }
    
    def action_view_classes(self):
        self.ensure_one()
        return {
            'name': 'Lịch học',
            'type': 'ir.actions.act_window',
            'res_model': 'language.center.class.schedule',
            'view_mode': 'list,form,calendar',
            'domain': [('course_id', '=', self.id)],
        } 