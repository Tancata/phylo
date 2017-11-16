#run two pb chains, keep them running, periodically check for convergence
import subprocess, sys, time, re, os

def start_pb_jobs(infile, bn):
    os.system('pb -d ' + infile + ' -catfix C60 -lg ' + bn + '_c60_lg_chain1 &')
    os.system('pb -d ' + infile + ' -catfix C60 -lg ' + bn + '_c60_lg_chain2 &')
    return

def check_convergence(infile, bn):
    #first check whether enough points have been sampled
    num_samples = sum(1 for line in open(bn + '_c60_lg_chain1.trace'))
    if num_samples >= 6667:
        burnin = int(float(num_samples)/4.0)
        #enough samples. Check bpcomp and tracecomp diagnostics
        #bp_proc = subprocess.Popen('bpcomp -o ' + infile[:-4] + '_c60_lg -x ' + str(burnin) + ' ' + infile[:-4] + '_c60_lg_chain1 ' + infile[:-4] + '_c60_lg_chain2',stdout=subprocess.PIPE) 
        bp_res = 0
        tr_res = 0
        bpcheck = os.popen('bpcomp -o ' + bn + '_c60_lg -x ' + str(burnin) + ' ' + bn + '_c60_lg_chain1 ' + bn + '_c60_lg_chain2').read()
        lines = bpcheck.splitlines()
        print "Bpcomp:"
        for line in lines:
            print line.rstrip()
            if line.startswith("maxdiff"):
                fields = re.split("\s+", line.rstrip())
                if float(fields[-1]) <= 0.3:
                    print "Converged because maxdiff is " + str(fields[-1])
                    bp_res = 1
                else:
                    print "Not converged yet: maxdiff is " + str(fields[-1])
        #now check tracecomp
        trcheck = os.popen('tracecomp -x ' + str(burnin) + ' ' + bn + '_c60_lg_chain1 ' + bn + '_c60_lg_chain2').read()
        
        t_lines = trcheck.splitlines()
        print "Tracecomp:"
        for line in t_lines:
            print line.rstrip()
            fields = re.split('\s+', line.rstrip())
            if len(fields) > 1:
                if fields[0] == 'name':
                    continue
                else:
                    if float(fields[1]) >= 50.0:
                        print "Converged : " + fields[0] + " " + fields[1]
                        tr_res += 1
                    else:
                        print "Not converged yet : " + fields[1]
                    if float(fields[2]) <= 0.3:
                        tr_res += 1
                        print "Converged : " + fields[0] + " " + fields[2]
                    else:
                        print "Not converged yet : " + fields[2]
            if bp_res == 1 and tr_res == 16:
                stop1 = os.system('stoppb ' + bn + '_c60_lg_chain1')
                stop2 = os.system('stoppb ' + bn + '_c60_lg_chain2')
                quit()
        return
    else:
        return

base_name = sys.argv[1][:-4]
start_pb_jobs(sys.argv[1], base_name)
while True:
    time.sleep(3600) #check for convergence once an hour
    check_convergence(sys.argv[1], base_name)
