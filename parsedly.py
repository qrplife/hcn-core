def isLeapYear(year):
    if year % 4 != 0:
        leap = False
    elif year % 100 != 0:
        leap = True
    elif year % 400 != 0:
        leap = False
    else:
        leap = True
    return leap

daysInMonth=[31,28,31,30,31,30,31,31,30,31,30,31]
elements=["PRCP","SNOW","SNWD","TMAX","TMIN"]
mf = []
qf = []
sf = []
dlyfile = "./ghcnd_hcn/hcn.dly"
with open(dlyfile,'r') as dly:
    EOF = False
    while not EOF:
        try:
            line = dly.readline()
            if len(line) == 0:
                EOF = True
                continue
        except EOFError:
            EOF = True
            continue

        ID=line[0:11]
        YEAR=int(line[11:15])
        MONTH=int(line[15:17])
        ELEMENT=line[17:21]
        if ELEMENT not in elements:
            continue

        dayCount = daysInMonth[MONTH - 1]
        if MONTH == 2 and isLeapYear(YEAR):
            dayCount+=1

        valueRecordLength = 5
        mflagRecordLength = 1
        qflagRecordLength = 1
        sflagRecordLength = 1
        offset=21
        sql = "INSERT INTO obs VALUES (\"{}\",{},{},{},\"{}\",{},\"{}\",\"{}\",\"{}\");"
        for day in range(1,dayCount+1):
            vBegin = offset
            vEnd = vBegin+valueRecordLength
            mBegin = vEnd
            mEnd = mBegin + mflagRecordLength
            qBegin = mEnd
            qEnd = qBegin + qflagRecordLength
            sBegin = qEnd
            sEnd = sBegin + sflagRecordLength

            value=line[vBegin:vEnd]
            mflag=line[mBegin:mEnd]
            qflag=line[qBegin:qEnd]
            sflag=line[sBegin:sEnd]
            if mflag not in mf:
                mf.append(mflag)
            if qflag not in qf:
                qf.append(qflag)
            if sflag not in sf:
                sf.append(sflag)

            offset=offset+valueRecordLength+mflagRecordLength+qflagRecordLength+sflagRecordLength
            sqlLine = sql.format(
                ID,
                YEAR,
                MONTH,
                int(day),
                ELEMENT,
                int(value),
                str(mflag).strip(),
                str(qflag).strip(),
                str(sflag).strip()
                )
            print(sqlLine)


        

