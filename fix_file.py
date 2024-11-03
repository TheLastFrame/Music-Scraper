file = open('sites.txt', 'r')
out = open('sites_fixed.txt', 'w+')

for line in file:
    parts = line.split('country')
    out.write(parts[0] + 'spotify/country' + parts[1])

file.close()
out.close()