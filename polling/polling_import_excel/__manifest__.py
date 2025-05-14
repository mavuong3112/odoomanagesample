# -*- coding: utf-8 -*-
{
    "name": "Polling – Import Excel",
    "version": "1.0",
    "summary": "Import câu hỏi khảo sát / trắc nghiệm từ Excel (Google Form)",
    "description": "Cho phép quản trị viên import nhanh danh sách câu hỏi và đáp án từ file Excel (tải về từ Google Form) vào mô‑đun Polling.",
    "author": "Your Name",
    "website": "https://example.com",
    "license": "LGPL-3",
    "application": False,
    "depends": ["polling"],
    "external_dependencies": {"python": ["openpyxl"]},
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/import_question_wizard_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
}