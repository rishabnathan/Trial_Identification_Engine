import pandas as pd

class TrialIdentificationEngine:
    """
    This is a trial identification engine that matches patient data against clinical trial data for Anatomic Site, Diagnosis, and Age Requirement.
    """
    def __init__(self, trials, patients):
        self.trials = trials
        self.patients = patients
        self.write_stream = []
    
    # Checks for match of non-required critera (age requirement) based off of the symbol (<, >, <=, and >=) and number given in the clinical_trial.csv.
    def match_non_required_criteria(self, trial_id, trial, patient) -> bool:
        age_requriement_match = True

        if pd.isna(patient.at['age']):
            return age_requriement_match

        if pd.isna(trial.at['age_requirement']):
            raise Exception(f'Clinical trial age requirement missing for trial {trial_id}.')

        trial_age_requirement = trial.at['age_requirement'].strip()

        first_digit_idx = 0
        for i, c in enumerate(trial_age_requirement):
            if i == 0:
                if c.isdigit():
                    age_requriement_match = False
            if c.isdigit():
                first_digit_idx = i
                break
        
        trial_age_requirement_symbol = trial_age_requirement[:first_digit_idx]
        trial_age_requirement_threshold = int(trial_age_requirement[first_digit_idx:])
        patient_age = int(patient.at['age'])

        if trial_age_requirement_symbol == '>=':
            if patient_age < trial_age_requirement_threshold:
                age_requriement_match = False
        elif trial_age_requirement_symbol == '<=':
            if patient_age > trial_age_requirement_threshold:
                age_requriement_match = False
        elif trial_age_requirement_symbol == '>':
            if patient_age <= trial_age_requirement_threshold:
                age_requriement_match = False
        elif trial_age_requirement_symbol == '<':
            if patient_age >= trial_age_requirement_threshold:
                age_requriement_match = False
        else:
            raise Exception('Clinical trial age requirement contains invalid data.')

        return age_requriement_match    

    # Checks for match of required criteria (diagnosis, anatomic site) between patient and clinical trial.
    def match_required_criteria(self, trial_id, trial, patient) -> bool:
        required_criteria_matched = False
        if (pd.isna(patient.at['diagnosis']) or pd.isna(patient.at['anatomic_site'])):
            return required_criteria_matched
        
        if pd.isna(trial.at['diagnoses']):
            raise Exception(f'Clinical trial diagnosis missing for trial {trial_id}.')

        trial_diagnoses = trial.at['diagnoses'].lower().split('|')
        patient_diagnosis_words = set(patient.at['diagnosis'].split(' '))
        diagnosis_match = any(diagnosis in patient_diagnosis_words for diagnosis in trial_diagnoses)

        if pd.isna(trial.at['anatomic_site']):
            raise Exception(f'Clinical trial anatomic site missing for trial {trial_id}')

        trial_anatomic_site = trial.at['anatomic_site'].lower()
        patient_anatomic_site_words = set(patient.at['anatomic_site'].split(' '))
        anatomic_site_match = trial_anatomic_site in patient_anatomic_site_words

        required_criteria_matched = diagnosis_match and anatomic_site_match
        
        return required_criteria_matched

    # Calls functions for checking required and non-required criteria and evaluates if patient can be identified for the clinical trial being looked at.
    def evaluate_patient(self, trial_id, trial, patient) -> bool:
        # evalute required criteria separate from non-requrired criteria
        required_criteria_match = self.match_required_criteria(trial_id, trial, patient)

        non_required_criteria_matched = self.match_non_required_criteria(trial_id, trial, patient)

        all_criteria_matched = required_criteria_match and non_required_criteria_matched
        return all_criteria_matched
    
    # Logs each patient that is being evaluated and for which clinical trial. Then it calls the evaluation logic.
    def evaluate_patients(self, trial_id, trial):
        patients_identified = []
        for i in range(self.patients.shape[0]):
            patient = self.patients.iloc[i]

            patient_id = patient.at['patient_id']
            patient_age = patient.at['age'] if not pd.isna(patient.at['age']) else "N/A"
            patient_gender = patient.at['gender'] if not pd.isna(patient.at['gender']) else "N/A"
            patient_diagnosis = patient.at['diagnosis'] if not pd.isna(patient.at['diagnosis']) else "N/A"

            # Acceptance Criteria #2
            self.write_stream.append(f'Processing patient {patient_id}, age {patient_age}, gender {patient_gender}, with diagnosis {patient_diagnosis}, for trial {trial_id}\n')

            identified = self.evaluate_patient(trial_id, trial, patient)
            if identified:
                patients_identified.append(patient_id)
        
        return patients_identified
    
    # Processes all of the clinical trials. Logs which clinical trial is currently being processed and routes to logic that processes it.
    # Also logs which patients ended up being identified for each trial.
    def process_trials(self):
        for i in range(self.trials.shape[0]):
            curr_trial = self.trials.iloc[i]

            trial_id = self.trials.at[i, 'trial_id']
            condition = self.trials.at[i, 'condition']
            num_patients = self.patients.shape[0]

            # Acceptance Criteria #1
            self.write_stream.append(f'Processing trial id {trial_id} for condition {condition} with {num_patients} potential patients.\n')

            elligble_patients = self.evaluate_patients(trial_id, curr_trial)

            # Acceptance Criteria #5
            self.write_stream.append(f'\nThe following {len(elligble_patients)} patients were identified for trial {trial_id}:\n')

            for patient in elligble_patients:
                self.write_stream.append(f'-- {patient}\n')
            self.write_stream.append('\n')
