from systemUtils import Welcome as W
from stringUtils import percentageToFloat
from timeUtils import elapsedtime as E
elapsed = E()
elapsed.printTime()

elapsed.reset()
W.print_all_libs()



print(percentageToFloat('100d%'))

elapsed.printTime()
elapsed.reset()
elapsed.printTime()