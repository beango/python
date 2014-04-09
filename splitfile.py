
file_object = open('BiscuitBox.txt', 'r')
index = 1
fileindex = 1

filename = 'output/BiscuitBox-%s.txt' % (str(fileindex).zfill(2))
output = open(filename, 'w')

for line in file_object:
    if index%50 == 0:
        output.write(line.strip('\n'))
        index = 0
        output.close()
        fileindex+=1;
        filename = 'output/BiscuitBox-%s.txt' % (str(fileindex).zfill(2))
        output = open(filename, 'w')
    else :
        output.write(line)
    index+=1

output.close()
file_object.close()
