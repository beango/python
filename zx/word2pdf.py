# -*- encoding: utf-8 -*-
import os
import sys
 
from win32com import client
 
# pip install win32com
def templateDoc2pdf(doc_name, pdf_name):
    """
    :word文件转pdf
    :param doc_name word文件名称
    :param pdf_name 转换后pdf文件名称
    """
    try:
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name, ReadOnly=1)
        worddoc.SaveAs(pdf_name+".jpg", FileFormat=17)
        worddoc.Close()
        return pdf_name
    except:
        return 1
 
templateDoc2pdf(sys.argv[1], sys.argv[2])
