#!/usr/bin/python

# AL's Code based on Udacity's Testing Week4 video.
#
#    1. 5-line fuzzer below is from Charlie Miller's
#        "Babysitting an Army of Monkeys"
#       -- Part 1 - http://www.youtube.com/watch?v=Xnwodi2CBws (verified)
#        -- Part 2 - http://www.youtube.com/watch?v=lK5fgCvS2N4 (verified)

# List of files to use as initial seed.
file_list=[
    "/home/jasnow/PS4-FUZZER/DATA/agilerecord_08.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/agile-web-development-with-rails_p2_2.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/icsea_2011_2_10_10057.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/RackIntro-2011-12-21.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/ReversingtheHiringProcess-ReferenceGuide2012-01-14.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/al-snow-full-resume-2012-01-08.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/GitandGitHub.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/rails2-sample.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/ruby-on-rails-tutorial-2.3.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/ruby-on-rails-tutorial-3.0.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/ruby-on-rails-tutorial-bold-2.3.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/ruby-on-rails-tutorial-bold-3.0.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide_et.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide_fr.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide_hr.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide_it.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide_ja.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FM_Key_Mappings_Quick_Guide_ru.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/subway.html",
    "/home/jasnow/PS4-FUZZER/DATA/2SeedsKariakooProgrammingAssistanceRequest.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/3705222012-getting_real.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/agilepatternsbookonline.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/ca_swdev_report_2012-06-07.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/em_public_20120522.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/Free_Memorial_Preferences_Planner_PDF.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/FullFnetReports_Tanzania_Footnet_PDF.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/happiness-article-2012-04-26.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/kaiser-application-2012-04-ViewNoticeDetails.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/last-wishes-form.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/MethodsAndTools-2012-Summer.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/Open-Advice-On-Open-Source-Projects.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/rails_upgrade_handbook.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/Ruby-Under-a-Microscope-Rough-Draft-2012-May.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/sqe_bettersoftware_0312.pdf",
    "/home/jasnow/PS4-FUZZER/DATA/TCoCrashPlanBackups-1.0-sample.pdf"
]


# List of applications to test
apps = [
    "C:/Program Files/Calibre2/ebook-viewer.exe"
    ]

############### end configuration #################

import os
import sys
import math
import random
import string
import subprocess
import time

lngth = 37
fuzz_output = "fuzz.pdf"
FuzzFactor  = 333
num_tests   = lngth - 1 # 10000
sleep_delay = 6.
crashes = 0
os.system("rm -rf OUTFILES 2> /dev/null")
os.system("mkdir  OUTFILES 2> /dev/null")
t1 = time.time()
for i in range(num_tests):
    #WAS: file_choice = random.choice(file_list)
    file_choice = file_list[i % lngth]
    app = random.choice(apps)

    buf = bytearray(open(file_choice, 'rb').read())

    # start Charlie Miller code
    numwrites = random.randrange(math.ceil((float(len(buf)) / FuzzFactor))) + 1
    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)
    # end Charlie Miller code

    fuzz_output = os.path.join("OUTFILES/", "_%d_fuzz.pdf" % i)
    open(fuzz_output, 'wb').write(buf)

    #WAS: process = subprocess.Popen([app, fuzz_output])
    process = subprocess.Popen([app, fuzz_output], stderr=subprocess.STDOUT, stdout=sys.stdout)
    time.sleep(sleep_delay)

    crashed = process.poll()
    if not crashed:
        process.terminate()
        print i, "OK", file_choice
    else:
        "it crashed, so save the fuzzed file"
        print i, "NOT", file_choice, "****************************************"
        crashes += 1
        #open(fuzzed_filename, 'wb').write(buf)
        
t2 = time.time()
print "Total crashes:", crashes
print "FuzzFactor=", FuzzFactor
print "Number of tests=", num_tests
print "Sleep Delay=", sleep_delay
#EOF

