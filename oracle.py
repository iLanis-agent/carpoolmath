#!/usr/bin/env python3
# Oracle for carpoolmath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

L_PER_100, WORKDAYS, DETOUR_KMH = 8, 5, 40

def jround(x):
    return math.floor(x + 0.5)
def money(x):
    return jround(x * 100) / 100
def round1(x):
    return jround(x * 10) / 10

def tripSplit(km, price, riders):
    total = money(km * 2 / 100 * L_PER_100 * price)
    per = money(total / riders)
    verdict = 'cheaper than the bus' if per < 2 else 'a fair split' if per < 6 else 'pricey - check the route'
    return {'total': total, 'per_person': per, 'verdict': verdict}

def rotation(drivers, weeks):
    total = weeks * WORKDAYS
    base = total // drivers
    extra = total % drivers
    verdict = 'perfectly even' if extra == 0 else f"{extra} driver{'s' if extra != 1 else ''} take{'s' if extra == 1 else ''} one extra day"
    return {'drives': total, 'min_drives': base, 'max_drives': base if extra == 0 else base + 1, 'verdict': verdict}

def detour(km, price, riders, detourKm):
    solo = money(km * 2 / 100 * L_PER_100 * price)
    shared = money((km + detourKm) * 2 / 100 * L_PER_100 * price / riders)
    saving = money(solo - shared)
    detourMin = round1(detourKm * 2 / DETOUR_KMH * 60)
    verdict = 'marginal - your call' if saving < 1 else 'worth the detour' if saving < 5 else 'a clear win'
    return {'solo': solo, 'shared': shared, 'saving': saving, 'detour_min': detourMin, 'verdict': verdict}

FUN = {'tripSplit': tripSplit, 'rotation': rotation, 'detour': detour}

CASES = [
  {'card':'tripSplit','args':[25,7.5,4]},  {'card':'tripSplit','args':[10,6,2]},
  {'card':'tripSplit','args':[40,8.2,3]},  {'card':'tripSplit','args':[5,5.9,2]},
  {'card':'tripSplit','args':[60,9,5]},    {'card':'tripSplit','args':[15,7,4]},
  {'card':'tripSplit','args':[100,7,6]},   {'card':'tripSplit','args':[30,10.5,2]},
  {'card':'tripSplit','args':[12,6.4,3]},  {'card':'tripSplit','args':[80,12,4]},
  {'card':'tripSplit','args':[150,8,7]},   {'card':'tripSplit','args':[45,7.9,5]},
  {'card':'tripSplit','args':[0,7,4],'error':'positive'},
  {'card':'tripSplit','args':[25,7,1],'error':'at least 2'},
  {'card':'tripSplit','args':[25,7,2.5],'error':'whole people'},
  {'card':'tripSplit','args':[250,7,4],'error':'under 200'},
  {'card':'tripSplit','args':[25,25,4],'error':'under 20'},
  {'card':'rotation','args':[2,1]}, {'card':'rotation','args':[3,3]},
  {'card':'rotation','args':[4,2]}, {'card':'rotation','args':[5,1]},
  {'card':'rotation','args':[2,4]}, {'card':'rotation','args':[6,6]},
  {'card':'rotation','args':[7,7]}, {'card':'rotation','args':[3,10]},
  {'card':'rotation','args':[4,13]},{'card':'rotation','args':[5,52]},
  {'card':'rotation','args':[2,26]},{'card':'rotation','args':[6,11]},
  {'card':'rotation','args':[1,4],'error':'at least 2'},
  {'card':'rotation','args':[3,0],'error':'positive'},
  {'card':'rotation','args':[2.5,4],'error':'whole people'},
  {'card':'rotation','args':[8,4],'error':'under 8'},
  {'card':'rotation','args':[4,60],'error':'under 53'},
  {'card':'detour','args':[25,7.5,3,4]}, {'card':'detour','args':[25,7.5,2,4]},
  {'card':'detour','args':[10,6,2,1]},   {'card':'detour','args':[40,8,4,10]},
  {'card':'detour','args':[15,7,3,0]},   {'card':'detour','args':[60,9,5,6]},
  {'card':'detour','args':[8,5.5,2,2]},  {'card':'detour','args':[30,10,3,8]},
  {'card':'detour','args':[50,8.4,4,3]}, {'card':'detour','args':[20,7,2,12]},
  {'card':'detour','args':[0,7,3,4],'error':'positive'},
  {'card':'detour','args':[25,7,1,4],'error':'at least 2'},
  {'card':'detour','args':[25,7,3,-2],'error':'zero or more'},
  {'card':'detour','args':[25,7,3,60],'error':'under 50'},
]

out = []
for c in CASES:
    row = dict(c)
    if 'error' not in c:
        row['expect'] = FUN[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as fh:
    json.dump(out, fh, indent=1)
    fh.write('\n')
print(len(out), 'cases written')
