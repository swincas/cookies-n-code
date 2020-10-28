import numpy as np
import datetime

def get_hash_tables(years):
    venues = []
    teams = []
    for yr in years:
        data = np.load(f'{yr}_data.npz',allow_pickle=True)
        infos = data['arr_1'].item()
        games = data['arr_0']

        for i in range(games.shape[0]):
            inf = infos[i]
            if inf['team1'] not in teams: teams.append(inf['team1'])
            if inf['Venue'] not in venues: venues.append(inf['Venue'])

    team_dic = {}
    for i,tm in enumerate(teams):
        team_dic[tm] = i
    venue_dic = {}
    for i,vn in enumerate(venues):
        venue_dic[vn] = i

    return team_dic,venue_dic

def load_year(fnm,td,vd):
    data = np.load(fnm,allow_pickle=True)

    games = data['arr_0']
    infos = data['arr_1'].item()

    results = []
    times = []
    dates = []
    rounds = []
    rgseason = []
    for i in range(games.shape[0]):
        inf = infos[i]
        try:
            if inf['result'] != 2:
                rounds.append(float(inf['Round']))
                results.append(inf['result'])
                rgseason.append(i)
                time = inf['time'].split(':')
                times.append(float(time[0]+time[1]))
                dates.append(inf['date'])
        except:
            pass

    for n,i in enumerate(rgseason):
        inf = infos[i]
        game = games[i]
        tm1,tm2 = td[inf['team1']],td[inf['team2']]
        tm_features = np.array([rounds[n],vd[inf['Venue']],tm1,tm2,times[n]])
        tm_features = np.concatenate((tm_features,game))
        if n == 0:
            features = tm_features
        else:
            features = np.vstack((features,tm_features))

    return features,np.array(results)

def make_date(date_raw):
    month_hash = {
        'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'Jun':6,
        'Jul':7,
        'Aug':8,
        'Sep':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
    }

    dlist = date_raw.split('-')
    return datetime.date(int(dlist[2]),month_hash[dlist[1]],int(dlist[0]))
    

def get_gdate_table(fnm,td,vd):
    
    data = np.load(fnm,allow_pickle=True)

    games = data['arr_0']
    infos = data['arr_1'].item()

    # Make Team Game Date Lookup
    gdates = {}
    for team in td.keys(): gdates[team] = {'games':0,'wins':0}
    for i in range(games.shape[0]):
        inf = infos[i]
        try:
            rnd = float(inf['Round'])
            tm1,tm2 = inf['team1'],inf['team2']
            dtt = make_date(inf['date'])
            res = inf['result']
            if res == 1:
                r2 = 0
            elif res == 0:
                r2 = 1
            else:
                res = 0.5
                r2 = 0.5

            t1k = list(gdates[tm1].keys())
            t2k = list(gdates[tm2].keys())

            if len(t1k) > 2:
                gdates[tm1][rnd] = [dtt,float(gdates[tm1]['wins'])/float(gdates[tm1]['games'])]
            else:
                gdates[tm1][rnd] = [dtt,0]

            if len(t2k) > 2:
                gdates[tm2][rnd] = [dtt,float(gdates[tm2]['wins'])/float(gdates[tm2]['games'])]
            else:
                gdates[tm2][rnd] = [dtt,0]
            
            gdates[tm1]['games']+=1
            gdates[tm2]['games']+=1
            gdates[tm1]['wins']+=res
            gdates[tm2]['wins']+=r2
            
        except:
            pass

    return gdates

def load_year_plus(fnm,td,vd):
    
    data = np.load(fnm,allow_pickle=True)

    games = data['arr_0']
    infos = data['arr_1'].item()

    gdates = get_gdate_table(fnm,td,vd)
    
    results = []
    times = []
    rounds = []
    rgseason = []
    for i in range(games.shape[0]):
        inf = infos[i]
        try:
            if inf['result'] != 2:
                rounds.append(float(inf['Round']))
                results.append(inf['result'])
                rgseason.append(i)
                time = inf['time'].split(':')
                times.append(float(time[0]+time[1]))
        except:
            pass

    resout = []
    for n,i in enumerate(rgseason):
        inf = infos[i]
        game = games[i]
        tm1,tm2 = inf['team1'],inf['team2']
        tm_features = np.array([rounds[n],vd[inf['Venue']],td[tm1],td[tm2],times[n]])
        gm = list(np.copy(game))
        if rounds[n] == 1:
            days1 = 21
            days2 = 21
            cwp1 = 0
            cwp2 = 0
        else:
            try:
                days1 = (gdates[tm1][rounds[n]][0]-gdates[tm1][rounds[n]-1][0]).days
            except:
                try:
                    days1 = (gdates[tm1][rounds[n]][0]-gdates[tm1][rounds[n]-2][0]).days
                except:
                    days1 = -99.
                    
            try:
                days2 = (gdates[tm2][rounds[n]][0]-gdates[tm2][rounds[n]-1][0]).days
            except:
                try:
                    days2 = (gdates[tm2][rounds[n]][0]-gdates[tm2][rounds[n]-2][0]).days
                except:
                    days2 = -99.
                    
            cwp1 = gdates[tm1][rounds[n]][1]
            cwp2 = gdates[tm2][rounds[n]][1]
                
        gm.insert(5,days1)
        gm.insert(5,cwp1)
        gm.insert(15,days2)
        gm.insert(15,cwp2)

        if days1 != -99 and days2 != -99:
            tm_features = np.concatenate((tm_features,gm))
            if n == 0:
                features = tm_features
            else:
                features = np.vstack((features,tm_features))
            resout.append(results[n])

    print(fnm,features.shape)
    return features,np.array(resout)


def load_year_minus(fnm):
    nmelb_teams = ['Port Adelaide','West Coast','Brisbane Lions','Adelaide','Fremantle','Sydney','Gold Coast','Greater Western Sydney']
    melb_vens = ['M.C.G.','Docklands','Kardinia Park']
    
    data = np.load(fnm,allow_pickle=True)

    games = data['arr_0']
    infos = data['arr_1'].item()

    results = []
    times = []
    dates = []
    rounds = []
    rgseason = []
    for i in range(games.shape[0]):
        inf = infos[i]
        try:
            if inf['result'] != 2:
                rounds.append(float(inf['Round']))
                results.append(inf['result'])
                rgseason.append(i)
                time = inf['time'].split(':')
                times.append(float(time[0]+time[1]))
                dates.append(inf['date'])
        except:
            pass

    for n,i in enumerate(rgseason):
        inf = infos[i]
        game = games[i]
        tm1,tm2 = inf['team1'],inf['team2']
        ven = inf['Venue']

        if tm1 not in nmelb_teams:
            tm1 = 1
        else:
            tm1 = 0

        if tm2 not in nmelb_teams:
            tm2 = 1
        else:
            tm2 = 0

        if ven in melb_vens:
            ven = 1
        else:
            ven = 0
        

        gm = [
            np.log10(game[1]), # total games home
            np.log10(game[3]), # total goals home
            np.log10(game[6]), # total games home coach
            np.log10(game[8]), # total games away
            np.log10(game[10]),# total goals away
            np.log10(game[13]),# total games away coach
            game[2]/game[9], # win % home / win % away
            game[7]/game[14], # win % home coach / win % away coach
        ]
            
        tm_features = np.array([rounds[n],ven,tm1,tm2])
        tm_features = np.concatenate((tm_features,gm))
        if n == 0:
            features = tm_features
        else:
            features = np.vstack((features,tm_features))

    return features,np.array(results)
