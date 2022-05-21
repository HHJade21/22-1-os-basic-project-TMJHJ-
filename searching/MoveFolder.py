import shutil

import schedule

import time

source = 'C:\\Users\\user\\Downloads'

destination = 'C:\\Users\\user\\Desktop\\open'

 

shutil.move(source,destination)

 

schedule.every(5).seconds.do(shutil.move(source,destination))
