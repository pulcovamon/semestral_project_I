class Patient:
    
    def __init__(self, id, codes,
                 active_phase_ground_truth, active_phase_prediction,
                 icd10_multiclass_ground_truth, icd10_multiclass_prediction,
                 icd10_binary_ground_truth, icd10_binary_prediction
                 ) -> None:
        self.id = id
        self.codes = codes
        
        self.active_phase = {}
        self.active_phase["ground_truth"] = active_phase_ground_truth
        self.active_phase["prediction"] = active_phase_prediction
        
        self.icd10_multiclass = {}
        self.icd10_multiclass["ground_truth"] = icd10_multiclass_ground_truth
        self.icd10_multiclass["prediction"] = icd10_multiclass_prediction
        
        self.icd10_binary = {}
        self.icd10_binary["ground_truth"] = icd10_binary_ground_truth
        self.icd10_binary["prediction"] = icd10_binary_prediction
        
    def __str__(self) -> str:
        return f"""Patient ID: {self.id}\n
                ACTIVE PHASE Ground Truth: {self.active_phase["ground_truth"]}\n
                ACTIVE PHASE Prediction: {self.active_phase["prediction"]}\n
                ICD10 MULTICLASS Ground Truth: {self.icd10_multiclass["ground_truth"]}\n
                ICD10 MULTICLASS Prediction: {self.icd10_multiclass["prediction"]}\n
                ICD10 BINARY Ground Truth: {self.icd10_binary["ground_truth"]}\n
                ICD10 BINARY Prediction: {self.icd10_binary["prediction"]}\n
                Codes: {self.codes}"""