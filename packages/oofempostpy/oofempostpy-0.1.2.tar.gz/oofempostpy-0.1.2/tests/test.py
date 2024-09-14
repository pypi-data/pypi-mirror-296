import sys
import os
sys.path.append('../oofempostpy')
import parser as of
# from oofempostpy import parse_simulation_log, export_to_csv

of.export_to_csv('./test.log', 'test.csv')

os.system('python extract.py -f test.in > 1.csv')
# et.main('test.in','1.csv')