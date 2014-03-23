import time

how_often = ['', 'Weekly', 'Monthly', 'Quarterly', 'Yearly', 'Less often', 'Never']

what_helped = [
    '',                                             # 0
    'Acupuncture',                                  # 1
    'Alan Carr books (alcohol related "Easy Way")', # 2
    'Alcoholics Anonymous',                         # 3
    'Antabuse (Disulfiram)',                        # 4
    'Cognitive Behavioral Therapy (CBT)',           # 5
    'Counseling - one on one',                      # 6
    'Craig Beck book "Alcohol Lied to Me"',         # 7
    'Group Therapy',                                # 8
    'Hypnosis',                                     # 9
    'Internet message boards (Not reddit based)',   # 10
    'Moderation Management',                        # 11
    'Naltrexone'                                    # 12
    'Narcotics Anonymous (NA)',                     # 13
    'None',                                         # 14
    'Not applicable',                               # 15
    'Other',                                        # 16
    'Reddit - /r/stopdrinking IRC channel',         # 17
    'Reddit - /r/stopdrinking subreddit',           # 18
    'Reddit - other recovery subreddit',            # 19
    'SMART Recovery',                               # 20
    'Treatment facility - Inpatient',               # 21
    'Treatment facility - Outpatient',              # 22
    'Women For Sobriety',                           # 23
]


def timestamp_convert(t):
    if not t: return 0
    try:
        return int(time.mktime(time.strptime(t,'%Y/%m/%d %I:%M:%S %p AST')))
    except ValueError:
        print 'Failed to convert: "%s"' % t
        raise

def date_convert(d):
    if not d: return 0
    try:
        return int(time.mktime(time.strptime(d,'%Y-%m-%d')))
    except ValueError:
        print 'Failed to convert: "%s"' % d
        raise

def numberwang(typ=float, unset=0.0):
    def converter(x):
        if not x: return unset
        return typ(x)
    return converter


def scaled(scale):
    def converter(x):
        if not x: return 0.0
        return float(x)*scale
    return converter

def indexed(lst):
    def converter(x):
        try:
            return lst.index(x)
        except ValueError:
            return -1
    return converter

