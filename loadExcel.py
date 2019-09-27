# -*- coding: utf-8 -*-

#   2019/9/27 0027 上午 10:15     

__author__ = 'RollingBear'

import xlrd

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

excelPath = 'G:\\烟盒标注\\整合\\香烟盒标注信息汇总20190305-2.xlsx'
xmlPath = 'G:\\烟盒标注\\整合\\cig-img-train\\1\\OAT\\img (1).oa'
txtPath = 'G:\\烟盒标注\\整合\\cig-img-train\\1\\OAT\\img (1).txt'


def loadExcel(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheet_by_name(excel.sheet_names()[0])
    keyList = []
    valueList = []

    for i in range(sheet.nrows):
        key = sheet.cell_value(i, 0)
        keyList.append(key)
        value = sheet.cell_value(i, 1)
        valueList.append(value)

    return keyList, valueList


def loadXml(xmlPath, txtPath, keyList, valueList):
    tree = ET.ElementTree(file=xmlPath)
    root = tree.getroot()
    i = 0
    with open(txtPath, 'r') as f:
        txtList = f.readlines()

    with open(txtPath, 'w+') as f:
        for child_of_root in root.iter(tag='Text'):
            if valueList[keyList.index(child_of_root.text)] == '':
                f.write(txtList[i])
                i += 1
                continue
            else:
                txtList[i].replace(child_of_root.text, valueList[keyList.index(child_of_root.text)])
                f.write(txtList[i])
                child_of_root.text = valueList[keyList.index(child_of_root.text)]
                i += 1
        tree.write(xmlPath)


if __name__ == '__main__':
    keyList, valueList = loadExcel(excelPath)

    loadXml(xmlPath, txtPath, keyList, valueList)
