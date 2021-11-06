from settings import RHYTMS

y = RHYTMS.copy()

y['aplha'] = 100
del y['betha']

print(RHYTMS)
print(y)