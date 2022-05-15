# Custom onverters for pandas are defined here

### zip_xxxxx_xxxx - converts zip code to xxxxx-xxxx, takes 5 digit zip code as input
zip_xxxxx_xxxx = lambda x: (str(int(x)//10000).zfill(5)+ "-" + str(int(x)%1000).zfill(4))

### Rounds the data to two decimal places 
round_2 = lambda x: ("{:.2f}".format(x))

### removes the decimal value in interegr 
nodecimal = lambda x: ("{:.0f}".format(x))


def converter(v):
    if v == 'zip_xxxxx_xxxx':
        return zip_xxxxx_xxxx
    if v == 'round_2':
        return round_2
    if v == 'nodecimal':
        return nodecimal