# -*- coding: utf-8 -*-

hour   = [6, 7, 8, 9, 10, 11]
minute = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    
for h in hour:
    for m in minute:
        if (h==11 and m ==35):
            break
        
        cdf_name = "wrfout_d02_2014-06-05_"+"{:0>2d}".format(h)+":"+"{:0>2d}".format(m)+":00"
        print cdf_name