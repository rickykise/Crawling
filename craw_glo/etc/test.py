from spyse import spyse

def startCrawling():
    #Using the API key allows us to go through multiple pages of results
    s = spyse('2Dz6uSLzSjbcjQE39F41Mc7ctZs3_Eru')
    # subdomains = s.subdomains('joo2video.net', param='domain')
    subdomains = s.domains_starts_with('joo2video.net', param='domain')
    print(subdomains)
    # subText = str(subdomains)
    # osp_s_nat = subText.split("country': {'name': '")[1].split("'")[0].strip()
    # osp_isp = subText.split("organization': '")[1].split("'")[0].strip()
    # print(osp_s_nat)
    # print(osp_isp)
    # print(subdomains)

if __name__=='__main__':
    startCrawling()
