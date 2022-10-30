array = ["100.100.2.12 asdasdasdasd",
"100.123.3.12 asdasdcacaca" ,
"100.123.3.12 asdasdcacaca" ,
"100.123.3.13 asdasdcacaca" ,
"100.123.3.13 asdasdcacaca" ,
"100.123.3.14 asdasdcacaca" ,]

dict = {}
result = []
def function(array):
    for line in array:
        var = line.split(" ")[0]
        if var not in dict:
            dict[var] = 1
        else:
            dict[var] = dict[var] + 1

    for x in dict.items():
        if x[1] == max(dict.values()):
            result.append(x[0])
    
    return result
print(function(array))


