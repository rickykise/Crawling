# wedisk(pc)

# 기존 코드
table = soup.find('table').find('tbody')
td = table.find_all('tr')[1].find_all('div')[1]['class']
if len(td) == 1:
    cnt_chk = 1
else:
    cnt_chk = 0


# ------------------------------------------------------------------------------

# 수정코드
table = soup.find('table').find('tbody')
td = table.find_all('tr')[1].find_all('div')[1]['class']
if len(td) == 1:
    cnt_chk = 1
else:
    cnt_chk = 0
if td[0] != 'no_jw':
    td = table.find_all('tr')[1].find_all('div')[5]['class']
    if len(td) == 1:
        cnt_chk = 1
    else:
        cnt_chk = 0
