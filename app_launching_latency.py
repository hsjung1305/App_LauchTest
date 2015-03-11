import logging
import os
import re
import sys
import time

test_name = 'app_launching_latency'
curdir = os.path.realpath(os.path.dirname(__file__))

APP_JAVA_PKG = 'com.redlicense.benchmark.sqlite'
APP_MAIN_ACTIVITY = '.Main'

# Systrace duration : 5
kWaitingForSystrace = 2
kTracingDuration = 7


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

os.system('python ./systrace/systrace.py --time %s -o tracedata.html am &'\
        % kTracingDuration)

time.sleep(kWaitingForSystrace)

os.system('adb shell am start -n %s/%s' %(APP_JAVA_PKG, APP_MAIN_ACTIVITY))

time.sleep(kTracingDuration+5)

getDataCmd = 'grep \"launching\" tracedata.html'
timeChecker = re.compile(r'.*\s+(?P<start>\d+\.\d+):\s+tracing_mark_write.*\n'\
        '.*\s+(?P<end>\d+\.\d+):\s+tracing_mark_write.*')
timedata = timeChecker.match(os.popen(getDataCmd).read())

startTime = float(timedata.group('start'))
endTime = float(timedata.group('end'))

launchingTime = float(timedata.group('end')) - float(timedata.group('start'))

logging.debug('Start : %f ms' % (startTime*1000))
logging.debug('End : %f ms' % (endTime*1000))
logging.debug('App Lauch Latency : %f ms' % (launchingTime*1000))

sys.exit(0)

