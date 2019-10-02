import re, os, sys, glob
job_index = 0

to_do = glob.glob("HFxOG_AllMetamonads_bmge/*bmge")
for file in to_do:
    job_index += 1
    new_name = "renamed/" + str(job_index) + ".bmge"
    os.system("cp " + file + " " + new_name)
