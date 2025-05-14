# -*- coding: utf-8 -*-
import base64
import tempfile
import os
from odoo import api, fields, models, _
from odoo.exceptions import UserError

try:
    import openpyxl
except ImportError:
    openpyxl = None


class ImportQuestionsWizard(models.TransientModel):
    _name = 'language.center.import.questions.wizard'
    _description = 'Import Questions Wizard'

    name = fields.Char('Tên', default='Import Câu hỏi')
    file = fields.Binary('File Excel', required=True)
    filename = fields.Char('Tên file')
    
    def action_import(self):
        if not openpyxl:
            raise UserError(_('Thư viện openpyxl chưa được cài đặt. Vui lòng cài đặt nó bằng cách chạy lệnh pip install openpyxl.'))
            
        if not self.file:
            raise UserError(_('Vui lòng chọn file trước khi import.'))
            
        # Tạm lưu file
        file_content = base64.b64decode(self.file)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp:
            temp.write(file_content)
            temp_path = temp.name
            
        try:
            # Đọc file Excel
            book = openpyxl.load_workbook(temp_path, read_only=True)
            sheet = book.active
            
            # Xử lý dữ liệu
            count = 0
            poll_question_obj = self.env['polling.question']
            poll_answer_obj = self.env['polling.answer']
            
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), 1):
                if row_index == 1:  # Bỏ qua hàng tiêu đề
                    continue
                    
                if not row[0]:  # Bỏ qua hàng trống
                    continue
                    
                # Tạo câu hỏi mới
                question_vals = {
                    'name': row[0],  # Giả sử cột đầu tiên là nội dung câu hỏi
                    'type': 'simple_choice',  # Loại câu hỏi
                    'question_type': 'text_box',  # Kiểu hiển thị
                }
                
                question = poll_question_obj.create(question_vals)
                count += 1
                
                # Tạo các đáp án
                answers = row[1:5]  # Giả sử 4 cột tiếp theo là các đáp án
                correct_answer = row[5] if len(row) > 5 else None  # Giả sử cột thứ 6 là đáp án đúng (A, B, C, D)
                
                for idx, answer_text in enumerate(answers):
                    if not answer_text:
                        continue
                        
                    answer_letter = chr(65 + idx)  # A, B, C, D
                    is_correct = correct_answer == answer_letter if correct_answer else False
                    
                    answer_vals = {
                        'value': answer_text,
                        'question_id': question.id,
                        'is_correct': is_correct,
                    }
                    
                    poll_answer_obj.create(answer_vals)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Thành công'),
                    'message': _('Đã import %s câu hỏi.') % count,
                    'sticky': False,
                }
            }
            
        except Exception as e:
            raise UserError(_('Lỗi khi import: %s') % str(e))
        finally:
            # Xóa file tạm
            try:
                os.unlink(temp_path)
            except:
                pass 