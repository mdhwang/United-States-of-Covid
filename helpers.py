gradient = {-3:'#920101',
            -2:'#A43904',
            -1:'#B67B09',
            0:'#C8C70F',
            1:'#99DA15',
            2:'#63EC1C',
            3:'#26FE24',
           }

def last_week_today(state,days,data):
    days = days + 2
    data = data.iloc[-days:,:]
    data['diff'] = data.cases.diff()
    data['rate'] = data['diff'].diff()
    data['plusminus'] = data['rate'].apply(lambda x: 1 if x > 0 else -1)
    data = data.iloc[-(days-2):,:]
    total = data.plusminus.sum()
    return gradient[total]

