#!/usr/bin/env python

import os
import jinja2
import tempfile

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait, letter
from reportlab.lib.units import inch, cm


STUDENT = 'Fulano de Tal'
INSTRUCTOR = 'Sicrano de Tal'
COURSE = 'Python Legal'
HOURS = 10
TEXT_PATH = 'text.html'
TEMPLATE_PATH = 'template.pdf'
SAVE_AS = 'certificado.pdf'


def render(template_path, context):
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def main():
    context = {
        'instructor': INSTRUCTOR,
        'course': COURSE,
        'student': STUDENT,
        'hours': HOURS,
    }
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name='Justify', alignment=TA_JUSTIFY, fontSize=16, leading=22
        )
    )
    elements = []
    certificate_txt = render(TEXT_PATH, context)
    paragraphs = certificate_txt.split(os.linesep)
    elements.append(Spacer(1, 50))
    for p in paragraphs:
        elements.append(Paragraph(p, styles['Justify']))
        elements.append(Spacer(1, 16))

    certificate = tempfile.NamedTemporaryFile()
    doc = SimpleDocTemplate(certificate, topMargin=3 * cm, bottomMargin=0)
    doc.pagesize = landscape(A4)
    doc.build(elements)

    output = PdfFileWriter()
    template_file = open('template.pdf', 'rb')
    input1 = PdfFileReader(template_file)
    page1 = input1.getPage(0)
    content = PdfFileReader(certificate)
    page1.mergePage(content.getPage(0))
    output.addPage(page1)
    save_file = open(SAVE_AS, 'wb')
    output.write(save_file)
    print('Certificado gerado com sucesso em %s' % SAVE_AS)

if __name__ == '__main__':
    main()
