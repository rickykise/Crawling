import time
from imgCheckTest import *

# osp_id = 'filekuki'
# url = 'http://www.filekuki.com/popup/kukicontview.jsp?id=2181391'
# osp_id = 'filelon'
# url = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx=4408063'
# osp_id = 'fileham'
# url = 'http://www.fileham.com/main/popup.php?doc=bbsInfo&idx=86497203'
osp_id = 'gdisk'
url = 'http://g-disk.co.kr/contents/view.htm?idx=496706'

def startCrawling():
    check = imgCheck(osp_id, url)
    print(check['Cnt_price'])
    print(check['Cnt_chk'])

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
