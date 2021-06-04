

# cnt_osp = 'wedisk'

html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
soup = BeautifulSoup(html,'html.parser')

cnt_price = soup.find('span', 'price').text.replace(',', '').split('캐시')[0].strip()
table = soup.find('table').find('tbody')
td = table.find_all('tr')[1].find_all('div')[1]['class']
if len(td) == 1:
    cnt_chk = 1
else:
    cnt_chk = 0



# --------------------------------------------------------------------------------------

# cnt_osp = 'filenori'

html = driver.find_element_by_id("body_view").get_attribute('innerHTML')
soup = BeautifulSoup(html,'html.parser')
table = soup.find('table', 'tbl_type_view')
cnt_chk = 0

cnt_price = table.find_all('td')[2].text.replace(',', '').split('캐시')[0].strip()
if soup.find('div', 'cooperateIcon'):
    cnt_chk = 1
