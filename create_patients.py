from patient import Patient
import os
import re
import csv

def create_csv():
    fields = ["id", "active_phase_ground_truth", "active_phase_prediction", "icd10_multiclass_ground_truth", "icd10_multiclass_prediction", "icd10_binary_ground_truth", "icd10_binary_prediction", "codes"]
    with open("patients.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fields)

def save_into_csv(**patient):
    with open("patients.csv", "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(patient.keys()))
        writer.writerow(patient)

def read_patients():
    with open(os.path.join(os.getcwd(), "catalog.txt"), "r") as catalog:
        patient_index = 0
        current_patient = {}
        patients = []
        for line in catalog:
            if "ID" in line:
                current_patient["id"] = int(''.join([i for i in line if i.isdigit()]))
                
            elif "ACTIVE PHASE" in line:
                if "Ground truth" in line:
                    current_patient["active_phase_ground_truth"] = [int(i) for i in line if i.isdigit()]
                else:
                    current_patient["active_phase_prediction"] = [int(i) for i in line if i.isdigit()]
                    
            elif "ICD10 MULTICLASS" in line:
                if "Ground truth" in line:
                    current_patient["icd10_multiclass_ground_truth"] = [re.sub("'|]|\n", "", i) for i in line.split("[")[1].split(" ")]
                else:
                    current_patient["icd10_multiclass_prediction"] = [int(i) for i in list(line.split("[")[1]) if i.isdigit()]
                    
            elif "ICD10 BINARY" in line:
                if "Ground truth" in line:
                    current_patient["icd10_binary_ground_truth"] = [re.sub("'|]|\n", "", i) for i in line.split("[")[1].split(" ")]
                else:
                    current_patient["icd10_binary_prediction"] = [int(i) for i in list(line.split("[")[1]) if i.isdigit()]
                    
            elif "Codes" in line:
                current_patient["codes"] = re.sub("]|'", "", line.split("[")[1]).replace("\n", "")
                    
            elif line.strip() == "" and current_patient:
                patient = Patient(**current_patient)
                save_into_csv(**current_patient)
                #print(patient)
                patients.append(patient)
                current_patient = {}
                patient_index += 1
                if patient_index >= 200:
                    break
                
        return patients
    
if __name__ == "__main__":
    create_csv()
    read_patients()