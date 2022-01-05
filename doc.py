# Roman Ramirez, rr8rk@virginia.edu
# Code for Generating Semester 6 Dates

import datetime
from collections import defaultdict
from num2words import num2words
import re

MONTHS = (
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September,'
    'October',
    'November',
    'December'
)

def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + datetime.timedelta(n)

def parse_txt(path):
    
    my_input = []
    with open(path, 'r') as f:
        for line in f:
            my_input.append(line.strip('\n'))
            
    events = list()
    dates = list()
            
    for i in range(len(my_input) - 1):
        if any([m in my_input[i+1] for m in MONTHS]):
            events.append(my_input[i])
            dates.append(my_input[i+1])
                
    # print(events)
    # print(dates)
    
    delims = (' , ', ' - ')
    clean_dates = list()
    for event, date in zip(events, dates):
        
        datelist = list()
       
        for d in delims:
            if d in date:
                d0, d1 = date.split(d)
                datelist.append(d0)
                datelist.append(d1)
        if len(datelist) == 0:
            datelist.append(date)
            
        # print(event, datelist)
        clean_dates.append(datelist)
        
    retVal = defaultdict()
        
    for event, date_range in zip(events, clean_dates):
        # print(event)
        
        cdr = list()
        for date in date_range:
            s_month, s_date, s_year = date.split(' ')
            month = MONTHS.index(s_month) + 1
            day = int(s_date[:-1])
            year = int(s_year)
            
            cdr.append((month, day, year))
            
        start_dt = datetime.date(cdr[0][2], cdr[0][0], cdr[0][1])
        if len(cdr) == 2:
            end_dt = datetime.date(cdr[1][2], cdr[1][0], cdr[1][1])
        else:
            end_dt = start_dt
        
        for dt in daterange(start_dt, end_dt):
            # print(dt.strftime('%Y-%m-%d'))
            retVal[dt] = event
        
    return retVal

def school_day_diff(datedict, date1, date2): # date1 is earlier date, date2 is later date
    currdate = date2
    retVal = 1
    while (currdate != date1):
        if currdate not in datedict.keys():
            if currdate.weekday() < 5:
                retVal += 1
        currdate = currdate - datetime.timedelta(1)
    return retVal 

def dict_to_message(doc, days_after, abv=False):
    retVal = ''

    if isinstance(doc, int):
        doc_word = num2words(doc, lang='en', to='ordinal')  
    else:
        doc_word = 'last'
    da_word = num2words(days_after, lang='en', to='cardinal')
    
    retVal += 'Happy '

    if days_after > 0:
        retVal += f'{da_word} days after the '
    retVal += f'{doc_word} day of class!'

    if abv:
        word_list = re.findall(r"[\w']+", retVal[len('Happy '):])
        retVal = 'Happy '
        for word in word_list:
            retVal += word[0]

    retVal += "!"
    return retVal

def main():
    
    d = parse_txt('sp22.txt')
    
    fdoc = None
    ldoc = None
    # find first day of class
    for k, v in d.items():
        if v == 'Courses begin':
            fdoc = k
        elif v == 'Courses end':
            ldoc = k
    # today = datetime.date.today()
    
    datedoc = defaultdict()
    
    starting = fdoc
    while starting != ldoc + datetime.timedelta(1):
        sdd = school_day_diff(d, fdoc, starting)
        datedoc[starting] = sdd
        
        starting += datetime.timedelta(1)
    
    newdatedoc = defaultdict()
    is_skip = 0
    for i, (k, v) in enumerate(datedoc.items()):
        vi = 0
        if i != 0:
            vi = datedoc[k - datetime.timedelta(1)]
            if vi-v > -1:
                is_skip += 1
            else:
                is_skip = 0
        # print(k, v, is_skip)
        
        newdatedoc[k] = (v, is_skip)
        
    # for k, v in newdatedoc.items():
    #     print(k, v)

    with open('output.txt', 'w') as f:
        for k, v in newdatedoc.items():
            abv = True
            if k != ldoc:
                message = dict_to_message(*v, abv)
            else:
                message = dict_to_message(ldoc, 0, abv)
            print(k, message)
            f.write(str(k) + " " + message + '\n')
    
       
if __name__ == '__main__':
    main()