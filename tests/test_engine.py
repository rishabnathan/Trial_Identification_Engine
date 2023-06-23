import unittest
import pandas as pd
from src.engine import TrialIdentificationEngine

class TestIdentificationEngineLogic(unittest.TestCase):
    def setUp(self):
        self.trials = pd.DataFrame({'trial_id': ['test_trial_id'], 
            'title': ['test_trial_title'], 
            'description': ['test_trial_description'],
            'phase': [1],
            'condition': ['test_trial_condition'],
            'anatomic_site': ['testsite'],
            'diagnoses': ['testdiag1|testdiag2'],
            'age_requirement': ['>20']})
        self.patients = pd.DataFrame({'patient_id': ['p1', 'p2'],
            'age': [25, 22],
            'gender': ['male', 'female'],
            'diagnosis': ['testdiag2', 'testdiag1'],
            'anatomic_site': ['testsite', 'testsite']})
        self.engine = TrialIdentificationEngine(self.trials, self.patients)

    def test_match_required_criteria_pass(self):
        res = self.engine.match_required_criteria(self.trials.at[0, 'trial_id'], self.trials.iloc[0], self.patients.iloc[0])
        self.assertTrue(res)

    def test_match_non_required_criteria_pass(self):
        res = self.engine.match_non_required_criteria(self.trials.at[0, 'trial_id'], self.trials.iloc[0], self.patients.iloc[0])
        self.assertTrue(res)

    def test_evaluate_patient_pass(self):
        res = self.engine.evaluate_patient(self.trials.at[0, 'trial_id'], self.trials.iloc[0], self.patients.iloc[0])
        self.assertTrue(res)

    def test_evaluate_patients_pass(self):
        res = self.engine.evaluate_patients(self.trials.at[0, 'trial_id'], self.trials.iloc[0])
        self.assertEqual(res, ['p1', 'p2'])
    
    def test_process_trials_pass(self):
        self.engine.process_trials()
        self.assertEqual(self.engine.write_stream[-3:-1], ['-- p1\n', '-- p2\n'])