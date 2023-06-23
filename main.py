#!/usr/bin/env python

import sys
from src.io_tools import read_data, clean_data, write_logs
from src.engine import TrialIdentificationEngine

def main():
    try:
        clinical_trial_csv = sys.argv[1]
        patient_feed_csv = sys.argv[2]
        output_file = sys.argv[3]
    except IndexError:
        print('Required files were not specified.')
        sys.exit(1)

    clinical_trials = read_data(clinical_trial_csv, ['diagnoses', 'anatomic_site', 'age_requirement'])
    patient_feed = read_data(patient_feed_csv, ['diagnosis', 'anatomic_site', 'age'])
    
    clinical_trials_cleaned = clean_data(clinical_trials, False)
    patient_feed_cleaned = clean_data(patient_feed, True)

    engine = TrialIdentificationEngine(clinical_trials_cleaned, patient_feed_cleaned)
    engine.process_trials()

    write_logs(output_file, engine.write_stream)

if __name__ == "__main__":
    main()