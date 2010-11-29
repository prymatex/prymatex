from pyonig import Regex

r = Regex(r'a(.*)b|[e-f]+')
match = r.match(r'zzzzaffffffffb')

if match:
    print match
else:
    print "No matches :("

