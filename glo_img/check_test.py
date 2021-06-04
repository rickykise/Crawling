def checkTitle(title, keyword):
    returnValue = {
        'm' : None,
        'i' : None,
        'k' : None
    }
    a = 0

    for s, p in keyword.items():
        title = title.replace(' ', '').lower()
        s = s.replace(' ', '').lower()

        if title.find(s) != -1 :
            returnValue['m'] = s
            returnValue['i'] = p[0]
            returnValue['k'] = p[1]
            getDelKey = getDel(p[0])
            if getDelKey == []:
                returnValue['m'] = s
                returnValue['i'] = p[0]
                returnValue['k'] = p[1]
            else:
                for d in getDelKey:
                    d = d.replace(' ', '').lower()
                    if title.find(d) != -1:
                        a = a+1
            if a != 0:
                returnValue['m'] = None

            return returnValue
