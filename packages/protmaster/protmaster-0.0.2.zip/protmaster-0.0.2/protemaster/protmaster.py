import pymzml
from tqdm import tqdm

def extract_tic(file):
    run = pymzml.run.Reader(file)
    rts = []
    tics= []
    for scan in tqdm(run,desc = 'Reading each scan'):
        rt = scan.scan_time_in_minutes()
        rts.append(rt)
        tic = scan.TIC
        tics.append(tic)
    return rts,tics
