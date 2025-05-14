# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ClassSchedule(models.Model):
    _name = 'language.center.class.schedule'
    _description = 'Class Schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên buổi học', compute='_compute_name', store=True)
    course_id = fields.Many2one('language.center.course', string='Khóa học', required=True, tracking=True)
    date = fields.Date('Ngày học', required=True, tracking=True)
    start_time = fields.Float('Giờ bắt đầu', required=True)
    end_time = fields.Float('Giờ kết thúc', required=True)
    description = fields.Text('Mô tả nội dung')
    room = fields.Char('Phòng học')
    state = fields.Selection([
        ('planned', 'Lên kế hoạch'),
        ('in_progress', 'Đang diễn ra'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy')
    ], string='Trạng thái', default='planned', tracking=True)
    attendance_ids = fields.One2many('language.center.attendance', 'class_schedule_id', string='Điểm danh')
    
    @api.depends('course_id', 'date')
    def _compute_name(self):
        for record in self:
            if record.course_id and record.date:
                record.name = f'{record.course_id.name} - {record.date}'
            else:
                record.name = 'New'
                
    def action_in_progress(self):
        self.write({'state': 'in_progress'})
        
    def action_done(self):
        self.write({'state': 'done'})
        
    def action_cancel(self):
        self.write({'state': 'cancel'})
        
    def action_planned(self):
        self.write({'state': 'planned'})


class Attendance(models.Model):
    _name = 'language.center.attendance'
    _description = 'Attendance'
    
    class_schedule_id = fields.Many2one('language.center.class.schedule', string='Buổi học', required=True)
    student_id = fields.Many2one('language.center.student', string='Học viên', required=True)
    present = fields.Boolean('Có mặt', default=True)
    note = fields.Text('Ghi chú') 