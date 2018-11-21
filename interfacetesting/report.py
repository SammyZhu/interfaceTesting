import xlwt

# 新建测试报告表格
global worksheet, workbook
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

worksheet.write(0, 0, label='testCaseName')
worksheet.write(0, 1, label='url')
worksheet.write(0, 2, label='errmsg')
worksheet.write(0, 3, label='data')
worksheet.write(0, 4, label='response')
worksheet.write(0, 5, label='test_result')

def report(self, data, val):
    for key, value in data.items():
        if key == "testCaseName":
            worksheet.write(val, 0, value)
        elif key == "url":
            worksheet.write(val, 1, value)
        elif key == "errmsg":
            worksheet.write(val, 2, value)
        elif key == "data":
            worksheet.write(val, 3, value)
        elif key == "response":
            worksheet.write(val, 4, str(value))
        elif key == "test_result":
            worksheet.write(val, 5, value)
        else:
            pass
    workbook.save('testReport.xlsx')