import os
import sys
import time

file_dir = sys.path[0]

hour   = [6, 7, 8, 9, 10, 11]
minute = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
while(1):
    fin = 0
    n_fin = 0
    for h in hour:
        for m in minute:
            if (h==11 and m ==30):
                break
            cdf_name = "wrfout_d02_2014-06-05_"+"{:0>2d}".format(h)+":"+"{:0>2d}".format(m)+":00"
            file_count=len(os.listdir(cdf_name))
            if file_count==61:
                print cdf_name+' -> ' + str(file_count)+' -> '+'finished'
                fin = fin + 1
            else:
                print cdf_name+' -> ' + str(file_count)+' -> '+'not finished'
                n_fin = n_fin + 1

    print "all data     :"+str(fin+n_fin)
    print "finished     :"+str(fin)
    print "not finished :"+str(n_fin)
    print str(1.0*fin/(fin+n_fin)*100)+'%'
    time.sleep(300)
    if n_fin==61:
        break

print "all finished"
