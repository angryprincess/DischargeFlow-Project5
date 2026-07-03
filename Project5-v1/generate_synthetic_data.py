"""
Synthetic Data Generator for Project 5 — Hospital Discharge Coordination System
Generates 150+ records for EHR, Pharmacy, and Billing servers with embedded traps/edge cases.
"""
import json
import random
import csv
import os

random.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# 1. MASTER MEDICATION DATABASE — 150 Brand-Generic Mappings
# =============================================================================

DRUG_CLASSES = {
    "penicillin": ["amoxicillin", "amoxicillin + clavulanate", "ampicillin", "piperacillin + tazobactam", "flucloxacillin"],
    "cephalosporin": ["cefixime", "ceftriaxone", "cephalexin", "cefuroxime", "cefpodoxime", "cefoperazone + sulbactam"],
    "macrolide": ["azithromycin", "clarithromycin", "erythromycin", "roxithromycin"],
    "fluoroquinolone": ["ciprofloxacin", "levofloxacin", "moxifloxacin", "ofloxacin", "norfloxacin"],
    "tetracycline": ["doxycycline", "minocycline", "tetracycline"],
    "aminoglycoside": ["gentamicin", "amikacin", "tobramycin"],
    "sulfonamide": ["sulfamethoxazole + trimethoprim", "sulfasalazine"],
    "nsaid": ["ibuprofen", "diclofenac", "naproxen", "piroxicam", "ketorolac", "indomethacin", "mefenamic acid", "aceclofenac", "etoricoxib", "celecoxib"],
    "analgesic": ["paracetamol", "tramadol", "ibuprofen + paracetamol"],
    "antihypertensive": ["amlodipine", "telmisartan", "losartan", "ramipril", "enalapril", "metoprolol", "atenolol", "valsartan", "olmesartan", "telmisartan + hydrochlorothiazide", "losartan + hydrochlorothiazide", "amlodipine + atenolol", "clonidine", "prazosin", "nifedipine"],
    "antidiabetic": ["metformin", "glimepiride", "glipizide", "sitagliptin", "voglibose", "pioglitazone", "metformin + glimepiride", "empagliflozin", "dapagliflozin", "insulin glargine"],
    "statin": ["atorvastatin", "rosuvastatin", "simvastatin", "pitavastatin"],
    "antiplatelet": ["aspirin", "clopidogrel", "ticagrelor", "prasugrel", "aspirin + clopidogrel"],
    "anticoagulant": ["warfarin", "heparin", "enoxaparin", "rivaroxaban", "apixaban", "dabigatran"],
    "ppi": ["pantoprazole", "omeprazole", "rabeprazole", "esomeprazole", "lansoprazole"],
    "antacid": ["ranitidine", "famotidine", "sucralfate", "aluminium hydroxide + magnesium hydroxide"],
    "antiemetic": ["ondansetron", "domperidone", "metoclopramide", "promethazine"],
    "bronchodilator": ["salbutamol", "ipratropium", "theophylline", "formoterol", "tiotropium", "montelukast", "budesonide", "fluticasone"],
    "corticosteroid": ["prednisolone", "dexamethasone", "methylprednisolone", "hydrocortisone", "budesonide"],
    "antifungal": ["fluconazole", "itraconazole", "voriconazole", "amphotericin b", "clotrimazole"],
    "antiviral": ["acyclovir", "valacyclovir", "oseltamivir", "remdesivir"],
    "antihistamine": ["cetirizine", "levocetirizine", "fexofenadine", "chlorpheniramine", "loratadine", "hydroxyzine"],
    "antidepressant": ["sertraline", "fluoxetine", "escitalopram", "amitriptyline", "venlafaxine", "duloxetine"],
    "antiepileptic": ["levetiracetam", "valproate sodium", "carbamazepine", "phenytoin", "gabapentin", "pregabalin", "lamotrigine"],
    "vasopressor": ["dopamine", "dobutamine", "norepinephrine", "epinephrine", "vasopressin"],
    "sedative": ["midazolam", "diazepam", "lorazepam", "alprazolam", "zolpidem"],
    "muscle_relaxant": ["tizanidine", "baclofen", "cyclobenzaprine", "chlorzoxazone", "thiocolchicoside"],
    "antispasmodic": ["dicyclomine", "hyoscine", "mebeverine", "drotaverine"],
    "thyroid": ["levothyroxine", "carbimazole", "propylthiouracil"],
    "migraine": ["sumatriptan", "rizatriptan", "naratriptan", "ergotamine"],
    "controlled": ["morphine", "fentanyl", "oxycodone", "codeine", "buprenorphine"],
}

# 150 Brand → Generic mappings (including traps)
BRAND_GENERIC_MAP = [
    # --- Penicillin class (allergy trap) ---
    {"brand": "Augmentin", "generic": "amoxicillin + clavulanate", "class": "penicillin", "strengths": ["625 mg", "1g"]},
    {"brand": "Moxclav", "generic": "amoxicillin + clavulanate", "class": "penicillin", "strengths": ["625 mg", "1g"]},
    {"brand": "Clavam", "generic": "amoxicillin + clavulanate", "class": "penicillin", "strengths": ["625 mg"]},
    {"brand": "Mox", "generic": "amoxicillin", "class": "penicillin", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Amoxil", "generic": "amoxicillin", "class": "penicillin", "strengths": ["500 mg"]},
    {"brand": "Ampilox", "generic": "ampicillin", "class": "penicillin", "strengths": ["500 mg"]},
    {"brand": "Piptaz", "generic": "piperacillin + tazobactam", "class": "penicillin", "strengths": ["4.5g"]},
    {"brand": "Floxapen", "generic": "flucloxacillin", "class": "penicillin", "strengths": ["500 mg"]},
    # --- Cephalosporins ---
    {"brand": "Taxim-O", "generic": "cefixime", "class": "cephalosporin", "strengths": ["200 mg"]},
    {"brand": "Cefix", "generic": "cefixime", "class": "cephalosporin", "strengths": ["200 mg"]},
    {"brand": "Monocef", "generic": "ceftriaxone", "class": "cephalosporin", "strengths": ["1g"]},
    {"brand": "Ceff", "generic": "cephalexin", "class": "cephalosporin", "strengths": ["500 mg"]},
    {"brand": "Altacef", "generic": "cefuroxime", "class": "cephalosporin", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Cefpo", "generic": "cefpodoxime", "class": "cephalosporin", "strengths": ["200 mg"]},
    {"brand": "Magnex", "generic": "cefoperazone + sulbactam", "class": "cephalosporin", "strengths": ["1.5g"]},
    # --- Macrolides ---
    {"brand": "Azithral", "generic": "azithromycin", "class": "macrolide", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Zithromax", "generic": "azithromycin", "class": "macrolide", "strengths": ["500 mg"]},
    {"brand": "Azee", "generic": "azithromycin", "class": "macrolide", "strengths": ["500 mg"]},
    {"brand": "Claribid", "generic": "clarithromycin", "class": "macrolide", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Erythrocin", "generic": "erythromycin", "class": "macrolide", "strengths": ["250 mg"]},
    {"brand": "Roxid", "generic": "roxithromycin", "class": "macrolide", "strengths": ["150 mg"]},
    # --- Fluoroquinolones ---
    {"brand": "Ciplox", "generic": "ciprofloxacin", "class": "fluoroquinolone", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Cifran", "generic": "ciprofloxacin", "class": "fluoroquinolone", "strengths": ["500 mg"]},
    {"brand": "Levoflox", "generic": "levofloxacin", "class": "fluoroquinolone", "strengths": ["500 mg", "750 mg"]},
    {"brand": "Tavanic", "generic": "levofloxacin", "class": "fluoroquinolone", "strengths": ["500 mg"]},
    {"brand": "Avelox", "generic": "moxifloxacin", "class": "fluoroquinolone", "strengths": ["400 mg"]},
    {"brand": "Moxicip", "generic": "moxifloxacin", "class": "fluoroquinolone", "strengths": ["400 mg"]},
    {"brand": "Oflox", "generic": "ofloxacin", "class": "fluoroquinolone", "strengths": ["200 mg", "400 mg"]},
    {"brand": "Norflox", "generic": "norfloxacin", "class": "fluoroquinolone", "strengths": ["400 mg"]},
    # --- Tetracyclines ---
    {"brand": "Doxy-1", "generic": "doxycycline", "class": "tetracycline", "strengths": ["100 mg"]},
    {"brand": "Doxt", "generic": "doxycycline", "class": "tetracycline", "strengths": ["100 mg"]},
    {"brand": "Minoz", "generic": "minocycline", "class": "tetracycline", "strengths": ["100 mg"]},
    # --- Aminoglycosides ---
    {"brand": "Garamycin", "generic": "gentamicin", "class": "aminoglycoside", "strengths": ["80 mg"]},
    {"brand": "Amicin", "generic": "amikacin", "class": "aminoglycoside", "strengths": ["500 mg"]},
    {"brand": "Tobra", "generic": "tobramycin", "class": "aminoglycoside", "strengths": ["80 mg"]},
    # --- Sulfonamides (allergy trap) ---
    {"brand": "Bactrim", "generic": "sulfamethoxazole + trimethoprim", "class": "sulfonamide", "strengths": ["400+80 mg", "800+160 mg"]},
    {"brand": "Septran", "generic": "sulfamethoxazole + trimethoprim", "class": "sulfonamide", "strengths": ["400+80 mg"]},
    {"brand": "Saaz", "generic": "sulfasalazine", "class": "sulfonamide", "strengths": ["500 mg"]},
    # --- Analgesics / Antipyretics ---
    {"brand": "Crocin", "generic": "paracetamol", "class": "analgesic", "strengths": ["500 mg", "650 mg"]},
    {"brand": "Dolo", "generic": "paracetamol", "class": "analgesic", "strengths": ["650 mg"]},
    {"brand": "Calpol", "generic": "paracetamol", "class": "analgesic", "strengths": ["500 mg"]},
    {"brand": "Tylenol", "generic": "paracetamol", "class": "analgesic", "strengths": ["500 mg"]},
    {"brand": "Metacin", "generic": "paracetamol", "class": "analgesic", "strengths": ["500 mg"]},
    {"brand": "Ultracet", "generic": "tramadol + paracetamol", "class": "analgesic", "strengths": ["37.5+325 mg"]},
    {"brand": "Contramal", "generic": "tramadol", "class": "analgesic", "strengths": ["50 mg", "100 mg"]},
    {"brand": "Combiflam", "generic": "ibuprofen + paracetamol", "class": "nsaid", "strengths": ["400+325 mg"]},
    # --- NSAIDs ---
    {"brand": "Brufen", "generic": "ibuprofen", "class": "nsaid", "strengths": ["400 mg", "600 mg"]},
    {"brand": "Ibugesic", "generic": "ibuprofen", "class": "nsaid", "strengths": ["400 mg"]},
    {"brand": "Voveran", "generic": "diclofenac", "class": "nsaid", "strengths": ["50 mg", "75 mg"]},
    {"brand": "Voltaren", "generic": "diclofenac", "class": "nsaid", "strengths": ["50 mg"]},
    {"brand": "Naprosyn", "generic": "naproxen", "class": "nsaid", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Pirox", "generic": "piroxicam", "class": "nsaid", "strengths": ["20 mg"]},
    {"brand": "Ketorol", "generic": "ketorolac", "class": "nsaid", "strengths": ["10 mg"]},
    {"brand": "Indocap", "generic": "indomethacin", "class": "nsaid", "strengths": ["25 mg"]},
    {"brand": "Meftal", "generic": "mefenamic acid", "class": "nsaid", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Hifenac", "generic": "aceclofenac", "class": "nsaid", "strengths": ["100 mg"]},
    {"brand": "Arcoxia", "generic": "etoricoxib", "class": "nsaid", "strengths": ["60 mg", "90 mg", "120 mg"]},
    {"brand": "Celebrex", "generic": "celecoxib", "class": "nsaid", "strengths": ["100 mg", "200 mg"]},
    # --- Antihypertensives ---
    {"brand": "Amlopress", "generic": "amlodipine", "class": "antihypertensive", "strengths": ["5 mg", "10 mg"]},
    {"brand": "Norvasc", "generic": "amlodipine", "class": "antihypertensive", "strengths": ["5 mg"]},
    {"brand": "Telma", "generic": "telmisartan", "class": "antihypertensive", "strengths": ["20 mg", "40 mg", "80 mg"]},
    {"brand": "Telma-H", "generic": "telmisartan + hydrochlorothiazide", "class": "antihypertensive", "strengths": ["40+12.5 mg"]},
    {"brand": "Losar", "generic": "losartan", "class": "antihypertensive", "strengths": ["25 mg", "50 mg"]},
    {"brand": "Cozaar", "generic": "losartan", "class": "antihypertensive", "strengths": ["50 mg"]},
    {"brand": "Losar-H", "generic": "losartan + hydrochlorothiazide", "class": "antihypertensive", "strengths": ["50+12.5 mg"]},
    {"brand": "Cardace", "generic": "ramipril", "class": "antihypertensive", "strengths": ["2.5 mg", "5 mg"]},
    {"brand": "Envas", "generic": "enalapril", "class": "antihypertensive", "strengths": ["5 mg", "10 mg"]},
    {"brand": "Betaloc", "generic": "metoprolol", "class": "antihypertensive", "strengths": ["25 mg", "50 mg"]},
    {"brand": "Aten", "generic": "atenolol", "class": "antihypertensive", "strengths": ["25 mg", "50 mg"]},
    {"brand": "Valent", "generic": "valsartan", "class": "antihypertensive", "strengths": ["80 mg", "160 mg"]},
    {"brand": "Olmezest", "generic": "olmesartan", "class": "antihypertensive", "strengths": ["20 mg", "40 mg"]},
    {"brand": "Amlopres-AT", "generic": "amlodipine + atenolol", "class": "antihypertensive", "strengths": ["5+50 mg"]},
    {"brand": "Arkamin", "generic": "clonidine", "class": "antihypertensive", "strengths": ["100 mcg"]},
    {"brand": "Prazopress", "generic": "prazosin", "class": "antihypertensive", "strengths": ["1 mg", "2.5 mg"]},
    {"brand": "Depin", "generic": "nifedipine", "class": "antihypertensive", "strengths": ["10 mg", "20 mg"]},
    # --- Antidiabetics ---
    {"brand": "Glycomet", "generic": "metformin", "class": "antidiabetic", "strengths": ["500 mg", "850 mg", "1000 mg"]},
    {"brand": "Glucophage", "generic": "metformin", "class": "antidiabetic", "strengths": ["500 mg"]},
    {"brand": "Amaryl", "generic": "glimepiride", "class": "antidiabetic", "strengths": ["1 mg", "2 mg"]},
    {"brand": "Glynase", "generic": "glipizide", "class": "antidiabetic", "strengths": ["5 mg"]},
    {"brand": "Januvia", "generic": "sitagliptin", "class": "antidiabetic", "strengths": ["50 mg", "100 mg"]},
    {"brand": "Volix", "generic": "voglibose", "class": "antidiabetic", "strengths": ["0.2 mg", "0.3 mg"]},
    {"brand": "Pioz", "generic": "pioglitazone", "class": "antidiabetic", "strengths": ["15 mg", "30 mg"]},
    {"brand": "Glycomet-GP", "generic": "metformin + glimepiride", "class": "antidiabetic", "strengths": ["500+1 mg", "500+2 mg"]},
    {"brand": "Jardiance", "generic": "empagliflozin", "class": "antidiabetic", "strengths": ["10 mg", "25 mg"]},
    {"brand": "Forxiga", "generic": "dapagliflozin", "class": "antidiabetic", "strengths": ["10 mg"]},
    {"brand": "Lantus", "generic": "insulin glargine", "class": "antidiabetic", "strengths": ["100 IU/mL"]},
    # --- Statins ---
    {"brand": "Atorva", "generic": "atorvastatin", "class": "statin", "strengths": ["10 mg", "20 mg", "40 mg"]},
    {"brand": "Lipitor", "generic": "atorvastatin", "class": "statin", "strengths": ["20 mg"]},
    {"brand": "Rozavel", "generic": "rosuvastatin", "class": "statin", "strengths": ["5 mg", "10 mg", "20 mg"]},
    {"brand": "Crestor", "generic": "rosuvastatin", "class": "statin", "strengths": ["10 mg"]},
    {"brand": "Simvas", "generic": "simvastatin", "class": "statin", "strengths": ["20 mg", "40 mg"]},
    {"brand": "Pitava", "generic": "pitavastatin", "class": "statin", "strengths": ["2 mg", "4 mg"]},
    # --- Antiplatelets / Anticoagulants ---
    {"brand": "Ecosprin", "generic": "aspirin", "class": "antiplatelet", "strengths": ["75 mg", "150 mg"]},
    {"brand": "Disprin", "generic": "aspirin", "class": "antiplatelet", "strengths": ["350 mg"]},
    {"brand": "Clopilet", "generic": "clopidogrel", "class": "antiplatelet", "strengths": ["75 mg"]},
    {"brand": "Plavix", "generic": "clopidogrel", "class": "antiplatelet", "strengths": ["75 mg"]},
    {"brand": "Brilinta", "generic": "ticagrelor", "class": "antiplatelet", "strengths": ["90 mg"]},
    {"brand": "Effient", "generic": "prasugrel", "class": "antiplatelet", "strengths": ["10 mg"]},
    {"brand": "Deplatt-A", "generic": "aspirin + clopidogrel", "class": "antiplatelet", "strengths": ["75+75 mg", "150+75 mg"]},
    {"brand": "Warf", "generic": "warfarin", "class": "anticoagulant", "strengths": ["1 mg", "2 mg", "5 mg"]},
    {"brand": "Clexane", "generic": "enoxaparin", "class": "anticoagulant", "strengths": ["40 mg", "60 mg"]},
    {"brand": "Xarelto", "generic": "rivaroxaban", "class": "anticoagulant", "strengths": ["10 mg", "15 mg", "20 mg"]},
    {"brand": "Eliquis", "generic": "apixaban", "class": "anticoagulant", "strengths": ["2.5 mg", "5 mg"]},
    {"brand": "Pradaxa", "generic": "dabigatran", "class": "anticoagulant", "strengths": ["110 mg", "150 mg"]},
    # --- PPIs / Antacids ---
    {"brand": "Pan", "generic": "pantoprazole", "class": "ppi", "strengths": ["20 mg", "40 mg"]},
    {"brand": "Pantocid", "generic": "pantoprazole", "class": "ppi", "strengths": ["40 mg"]},
    {"brand": "Omez", "generic": "omeprazole", "class": "ppi", "strengths": ["20 mg"]},
    {"brand": "Rablet", "generic": "rabeprazole", "class": "ppi", "strengths": ["20 mg"]},
    {"brand": "Neksium", "generic": "esomeprazole", "class": "ppi", "strengths": ["20 mg", "40 mg"]},
    {"brand": "Lanzol", "generic": "lansoprazole", "class": "ppi", "strengths": ["15 mg", "30 mg"]},
    {"brand": "Rantac", "generic": "ranitidine", "class": "antacid", "strengths": ["150 mg"]},
    {"brand": "Famocid", "generic": "famotidine", "class": "antacid", "strengths": ["20 mg", "40 mg"]},
    {"brand": "Sucrafil", "generic": "sucralfate", "class": "antacid", "strengths": ["1g"]},
    {"brand": "Digene", "generic": "aluminium hydroxide + magnesium hydroxide", "class": "antacid", "strengths": ["10 mL"]},
    # --- Antiemetics ---
    {"brand": "Emeset", "generic": "ondansetron", "class": "antiemetic", "strengths": ["4 mg", "8 mg"]},
    {"brand": "Domstal", "generic": "domperidone", "class": "antiemetic", "strengths": ["10 mg"]},
    {"brand": "Perinorm", "generic": "metoclopramide", "class": "antiemetic", "strengths": ["10 mg"]},
    {"brand": "Phenergan", "generic": "promethazine", "class": "antiemetic", "strengths": ["10 mg", "25 mg"]},
    # --- Bronchodilators / Respiratory ---
    {"brand": "Asthalin", "generic": "salbutamol", "class": "bronchodilator", "strengths": ["2 mg", "4 mg", "100 mcg inhaler"]},
    {"brand": "Ipravent", "generic": "ipratropium", "class": "bronchodilator", "strengths": ["20 mcg inhaler"]},
    {"brand": "Deriphyllin", "generic": "theophylline", "class": "bronchodilator", "strengths": ["200 mg", "300 mg"]},
    {"brand": "Foracort", "generic": "formoterol + budesonide", "class": "bronchodilator", "strengths": ["6+200 mcg"]},
    {"brand": "Tiova", "generic": "tiotropium", "class": "bronchodilator", "strengths": ["18 mcg"]},
    {"brand": "Montair", "generic": "montelukast", "class": "bronchodilator", "strengths": ["10 mg"]},
    {"brand": "Budecort", "generic": "budesonide", "class": "corticosteroid", "strengths": ["0.5 mg/mL", "1 mg/mL"]},
    {"brand": "Flohale", "generic": "fluticasone", "class": "corticosteroid", "strengths": ["125 mcg", "250 mcg"]},
    # --- Corticosteroids ---
    {"brand": "Omnacortil", "generic": "prednisolone", "class": "corticosteroid", "strengths": ["5 mg", "10 mg", "20 mg"]},
    {"brand": "Decdan", "generic": "dexamethasone", "class": "corticosteroid", "strengths": ["0.5 mg", "4 mg"]},
    {"brand": "Solu-Medrol", "generic": "methylprednisolone", "class": "corticosteroid", "strengths": ["125 mg", "500 mg"]},
    {"brand": "Efcorlin", "generic": "hydrocortisone", "class": "corticosteroid", "strengths": ["100 mg"]},
    # --- Antifungals ---
    {"brand": "Forcan", "generic": "fluconazole", "class": "antifungal", "strengths": ["150 mg", "200 mg"]},
    {"brand": "Canditral", "generic": "itraconazole", "class": "antifungal", "strengths": ["100 mg", "200 mg"]},
    {"brand": "Vfend", "generic": "voriconazole", "class": "antifungal", "strengths": ["200 mg"]},
    {"brand": "Fungizone", "generic": "amphotericin b", "class": "antifungal", "strengths": ["50 mg"]},
    # --- Antivirals ---
    {"brand": "Zovirax", "generic": "acyclovir", "class": "antiviral", "strengths": ["200 mg", "400 mg", "800 mg"]},
    {"brand": "Valcivir", "generic": "valacyclovir", "class": "antiviral", "strengths": ["500 mg", "1000 mg"]},
    {"brand": "Tamiflu", "generic": "oseltamivir", "class": "antiviral", "strengths": ["75 mg"]},
    # --- Antihistamines ---
    {"brand": "Alerid", "generic": "cetirizine", "class": "antihistamine", "strengths": ["10 mg"]},
    {"brand": "Xyzal", "generic": "levocetirizine", "class": "antihistamine", "strengths": ["5 mg"]},
    {"brand": "Allegra", "generic": "fexofenadine", "class": "antihistamine", "strengths": ["120 mg", "180 mg"]},
    {"brand": "Avil", "generic": "chlorpheniramine", "class": "antihistamine", "strengths": ["4 mg"]},
    {"brand": "Claritin", "generic": "loratadine", "class": "antihistamine", "strengths": ["10 mg"]},
    {"brand": "Atarax", "generic": "hydroxyzine", "class": "antihistamine", "strengths": ["10 mg", "25 mg"]},
    # --- Antidepressants ---
    {"brand": "Zoloft", "generic": "sertraline", "class": "antidepressant", "strengths": ["50 mg", "100 mg"]},
    {"brand": "Fludac", "generic": "fluoxetine", "class": "antidepressant", "strengths": ["20 mg"]},
    {"brand": "Nexito", "generic": "escitalopram", "class": "antidepressant", "strengths": ["5 mg", "10 mg"]},
    {"brand": "Tryptomer", "generic": "amitriptyline", "class": "antidepressant", "strengths": ["10 mg", "25 mg"]},
    {"brand": "Venlor", "generic": "venlafaxine", "class": "antidepressant", "strengths": ["37.5 mg", "75 mg"]},
    {"brand": "Cymbalta", "generic": "duloxetine", "class": "antidepressant", "strengths": ["20 mg", "30 mg", "60 mg"]},
    # --- Antiepileptics ---
    {"brand": "Levipil", "generic": "levetiracetam", "class": "antiepileptic", "strengths": ["250 mg", "500 mg"]},
    {"brand": "Encorate", "generic": "valproate sodium", "class": "antiepileptic", "strengths": ["200 mg", "500 mg"]},
    {"brand": "Tegretol", "generic": "carbamazepine", "class": "antiepileptic", "strengths": ["200 mg"]},
    {"brand": "Eptoin", "generic": "phenytoin", "class": "antiepileptic", "strengths": ["100 mg", "300 mg"]},
    {"brand": "Gabapin", "generic": "gabapentin", "class": "antiepileptic", "strengths": ["100 mg", "300 mg"]},
    {"brand": "Pregabalin-NT", "generic": "pregabalin", "class": "antiepileptic", "strengths": ["75 mg", "150 mg"]},
    {"brand": "Lamictal", "generic": "lamotrigine", "class": "antiepileptic", "strengths": ["25 mg", "50 mg", "100 mg"]},
    # --- Vasopressors (similar name trap: dopamine vs dobutamine) ---
    {"brand": "Dopmin", "generic": "dopamine", "class": "vasopressor", "strengths": ["200 mg/5mL"]},
    {"brand": "Dobutrex", "generic": "dobutamine", "class": "vasopressor", "strengths": ["250 mg/20mL"]},
    # --- Sedatives / Controlled ---
    {"brand": "Frisium", "generic": "clobazam", "class": "sedative", "strengths": ["5 mg", "10 mg"]},
    {"brand": "Calmpose", "generic": "diazepam", "class": "sedative", "strengths": ["5 mg", "10 mg"]},
    {"brand": "Ativan", "generic": "lorazepam", "class": "sedative", "strengths": ["1 mg", "2 mg"]},
    {"brand": "Alprax", "generic": "alprazolam", "class": "sedative", "strengths": ["0.25 mg", "0.5 mg"]},
    {"brand": "Stilnoct", "generic": "zolpidem", "class": "sedative", "strengths": ["5 mg", "10 mg"]},
    # --- Controlled Substances (billing trap — must NOT see clinical details) ---
    {"brand": "Morphine Sulfate", "generic": "morphine", "class": "controlled", "strengths": ["10 mg", "15 mg", "30 mg"]},
    {"brand": "Durogesic", "generic": "fentanyl", "class": "controlled", "strengths": ["25 mcg/hr patch", "50 mcg/hr patch"]},
    {"brand": "OxyContin", "generic": "oxycodone", "class": "controlled", "strengths": ["5 mg", "10 mg"]},
    {"brand": "Codeine Phosphate", "generic": "codeine", "class": "controlled", "strengths": ["15 mg", "30 mg"]},
    {"brand": "Buprigesic", "generic": "buprenorphine", "class": "controlled", "strengths": ["0.3 mg"]},
    # --- Muscle Relaxants ---
    {"brand": "Sirdalud", "generic": "tizanidine", "class": "muscle_relaxant", "strengths": ["2 mg", "4 mg"]},
    {"brand": "Liofen", "generic": "baclofen", "class": "muscle_relaxant", "strengths": ["10 mg", "25 mg"]},
    {"brand": "Myoril", "generic": "thiocolchicoside", "class": "muscle_relaxant", "strengths": ["4 mg", "8 mg"]},
    # --- Antispasmodics ---
    {"brand": "Cyclopam", "generic": "dicyclomine", "class": "antispasmodic", "strengths": ["10 mg", "20 mg"]},
    {"brand": "Buscopan", "generic": "hyoscine", "class": "antispasmodic", "strengths": ["10 mg"]},
    {"brand": "Mebex", "generic": "mebeverine", "class": "antispasmodic", "strengths": ["135 mg"]},
    {"brand": "Drotin", "generic": "drotaverine", "class": "antispasmodic", "strengths": ["40 mg", "80 mg"]},
    # --- Thyroid ---
    {"brand": "Thyronorm", "generic": "levothyroxine", "class": "thyroid", "strengths": ["25 mcg", "50 mcg", "75 mcg", "100 mcg"]},
    {"brand": "Eltroxin", "generic": "levothyroxine", "class": "thyroid", "strengths": ["50 mcg", "100 mcg"]},
    {"brand": "Neo-Mercazole", "generic": "carbimazole", "class": "thyroid", "strengths": ["5 mg"]},
    # --- Migraine ---
    {"brand": "Suminat", "generic": "sumatriptan", "class": "migraine", "strengths": ["25 mg", "50 mg"]},
    {"brand": "Rizora", "generic": "rizatriptan", "class": "migraine", "strengths": ["5 mg", "10 mg"]},
]

assert len(BRAND_GENERIC_MAP) >= 150, f"Only {len(BRAND_GENERIC_MAP)} brand-generic mappings, need 150"

# =============================================================================
# 2. PHARMACY INVENTORY — 150 records
# =============================================================================

def generate_inventory(brand_generic_map):
    """Generate pharmacy inventory from brand-generic map. One record per generic+strength."""
    inventory = []
    seen = set()
    idx = 0

    for entry in brand_generic_map:
        if entry["generic"] is None:
            continue
        for strength in entry["strengths"]:
            key = (entry["generic"], strength)
            if key in seen:
                continue
            seen.add(key)
            idx += 1

            # Deliberately make some items out of stock for traps
            if entry["generic"] == "amoxicillin + clavulanate" and strength == "625 mg":
                stock = 0
                alts = ["amoxicillin + clavulanate 1g"]
            elif entry["generic"] == "cefixime" and strength == "200 mg":
                stock = 0
                alts = ["cefpodoxime 200 mg"]
            elif entry["generic"] == "ranitidine" and strength == "150 mg":
                stock = 0
                alts = ["famotidine 20 mg"]
            elif entry["generic"] == "diclofenac" and strength == "50 mg":
                stock = 0
                alts = ["aceclofenac 100 mg"]
            elif entry["generic"] == "metformin" and strength == "500 mg":
                stock = 0
                alts = ["metformin 850 mg"]
            elif entry["generic"] == "amlodipine" and strength == "5 mg":
                stock = 0
                alts = ["amlodipine 10 mg"]
            elif entry["generic"] == "losartan" and strength == "25 mg":
                stock = 0
                alts = ["losartan 50 mg"]
            elif entry["generic"] == "azithromycin" and strength == "250 mg":
                stock = 0
                alts = ["azithromycin 500 mg"]
            elif entry["generic"] == "prednisolone" and strength == "5 mg":
                stock = 0
                alts = ["prednisolone 10 mg"]
            elif entry["generic"] == "pantoprazole" and strength == "20 mg":
                stock = 0
                alts = ["pantoprazole 40 mg"]
            else:
                stock = random.choice([10, 20, 30, 50, 75, 100, 120, 150, 200])
                alts = []

            record = {
                "generic_name": entry["generic"].title() if "+" not in entry["generic"] else entry["generic"].title().replace(" + ", " + "),
                "strength": strength,
                "stock": stock,
                "alternatives": alts,
                "drug_class": entry["class"]
            }
            inventory.append(record)

    return inventory

# =============================================================================
# 3. BILLING CATALOG — 150 records
# =============================================================================

def generate_billing_catalog(inventory):
    """Generate billing catalog from inventory. One entry per generic+strength."""
    catalog = []
    base_prices = {
        "penicillin": 1.75, "cephalosporin": 3.00, "macrolide": 2.50,
        "fluoroquinolone": 2.00, "tetracycline": 1.50, "aminoglycoside": 5.00,
        "sulfonamide": 1.00, "analgesic": 0.50, "nsaid": 0.75,
        "antihypertensive": 1.50, "antidiabetic": 2.00, "statin": 1.75,
        "antiplatelet": 1.50, "anticoagulant": 8.00, "ppi": 1.25,
        "antacid": 0.50, "antiemetic": 1.00, "bronchodilator": 2.50,
        "corticosteroid": 2.00, "antifungal": 4.00, "antiviral": 5.00,
        "antihistamine": 0.75, "antidepressant": 1.50, "antiepileptic": 2.00,
        "vasopressor": 10.00, "sedative": 1.50, "controlled": 3.00,
        "muscle_relaxant": 1.00, "antispasmodic": 0.75, "thyroid": 0.50,
        "migraine": 3.50,
    }
    code_counters = {}

    for item in inventory:
        drug_class = item["drug_class"]
        prefix_map = {
            "penicillin": "AB", "cephalosporin": "AC", "macrolide": "AD",
            "fluoroquinolone": "AE", "tetracycline": "AF", "aminoglycoside": "AG",
            "sulfonamide": "AH", "analgesic": "RX", "nsaid": "NS",
            "antihypertensive": "CV", "antidiabetic": "DM", "statin": "ST",
            "antiplatelet": "AP", "anticoagulant": "AX", "ppi": "GI",
            "antacid": "GA", "antiemetic": "AV", "bronchodilator": "RS",
            "corticosteroid": "CS", "antifungal": "AF", "antiviral": "AV",
            "antihistamine": "AH", "antidepressant": "PS", "antiepileptic": "NE",
            "vasopressor": "VP", "sedative": "SD", "controlled": "CT",
            "muscle_relaxant": "MR", "antispasmodic": "AS", "thyroid": "TH",
            "migraine": "MG",
        }
        prefix = prefix_map.get(drug_class, "XX")
        code_counters[prefix] = code_counters.get(prefix, 0) + 1
        code = f"{prefix}-{code_counters[prefix]:03d}"

        base = base_prices.get(drug_class, 1.00)
        price = round(base * random.uniform(0.8, 1.5), 2)

        item_name = f"{item['generic_name'].lower()} {item['strength']}"
        catalog.append({
            "item_name": item_name,
            "code": code,
            "price": price,
            "drug_class": drug_class
        })

    return catalog

# =============================================================================
# 4. DISCHARGE CASES — 150 patients
# =============================================================================

DIAGNOSES = [
    "Community acquired pneumonia", "Urinary tract infection",
    "Acute viral fever", "Lower respiratory tract infection",
    "Bronchitis with fever", "Skin and soft tissue infection",
    "Diabetic foot ulcer with cellulitis", "Acute gastroenteritis",
    "Tension headache", "Post-operative pain management",
    "Mild dengue fever", "Hypertension management",
    "Acute myocardial infarction", "Severe CAP with sepsis",
    "Viral upper respiratory infection", "Musculoskeletal pain",
    "Observation only — chest pain ruled out", "Migraine with aura",
    "Type 2 diabetes mellitus", "Unstable angina",
    "Acute exacerbation of COPD", "Acute asthma",
    "Atrial fibrillation", "Deep vein thrombosis",
    "Pulmonary embolism", "Peptic ulcer disease",
    "Gastroesophageal reflux disease", "Acute pancreatitis",
    "Cholecystitis", "Appendicitis — post appendectomy",
    "Cellulitis of lower limb", "Diabetic ketoacidosis",
    "Hypothyroidism", "Hyperthyroidism",
    "Epilepsy — breakthrough seizure", "Major depressive disorder",
    "Generalized anxiety disorder", "Chronic kidney disease stage 3",
    "Acute kidney injury", "Congestive heart failure",
    "Herpes zoster", "Oral candidiasis",
    "Allergic rhinitis", "Chronic urticaria",
    "Rheumatoid arthritis flare", "Osteoarthritis knee",
    "Lumbar spondylosis", "Sciatica",
    "Nausea and vomiting — post chemotherapy", "Acute vertigo",
    "Febrile neutropenia", "Infective endocarditis",
    "Meningitis — empirical treatment", "Septic arthritis",
    "Surgical site infection", "Post-CABG recovery",
    "Post-hip replacement", "Post-caesarean section",
    "Preeclampsia — postpartum", "Neonatal sepsis",
]

ALLERGY_OPTIONS = [
    [], [], [], [], [], [], [],  # Most patients have no allergies
    ["penicillin"], ["penicillin"], ["penicillin"],
    ["sulfonamides"], ["sulfonamides"],
    ["aspirin"], ["aspirin"],
    ["nsaid"],
    ["penicillin", "sulfonamides"],
    ["penicillin", "cephalosporin"],
    ["codeine"],
    ["ibuprofen"],
    ["fluoroquinolone"],
]

FREQUENCIES = ["OD", "BD", "TDS", "QDS", "SOS", "HS", "STAT"]
DURATIONS = ["3 days", "5 days", "7 days", "10 days", "14 days", "21 days", "30 days"]

CLINICAL_NOTES_TEMPLATES = [
    "Patient responded well to treatment. Vitals stable. Discharge on oral medications.",
    "Symptoms resolved after {duration} of IV therapy. Stepping down to oral.",
    "Clinical improvement noted. Labs trending towards normal. Follow-up in 1 week.",
    "Patient tolerated treatment well. No adverse reactions. Discharge advised.",
    "Observation complete. No complications. Discharge with prescribed medications.",
    "Post-operative recovery uneventful. Wound clean. Oral antibiotics and analgesics advised.",
    "Fever resolved. CRP declining. Completing antibiotic course at home.",
    "Blood sugar levels stabilized. Adjusted oral hypoglycemics for discharge.",
    "Blood pressure controlled with current regimen. Continue medications.",
    "Seizure-free for 48 hours. Anti-epileptic levels therapeutic. Safe for discharge.",
    "Patient counseled on medication compliance. Return if symptoms recur.",
    "Pain managed with oral analgesics. Physiotherapy referral given.",
    "Infection markers improving. Culture sensitivity guided antibiotic change.",
    "Respiratory distress resolved. Nebulization weaned. Inhalers prescribed.",
    "Cardiac enzymes normalized. Dual antiplatelet started. Cardiology follow-up.",
]

def calc_quantity(frequency, duration_str):
    freq_map = {"OD": 1, "BD": 2, "TDS": 3, "QDS": 4, "SOS": 2, "HS": 1, "STAT": 1}
    days = int(duration_str.split()[0])
    return freq_map.get(frequency, 1) * days

def generate_patients():
    patients = []
    patient_csv = []
    patient_counter = 1000

    # =========================================================================
    # CATEGORY 1: HAPPY PATH — 60 patients
    # =========================================================================
    for i in range(60):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        diag = random.choice(DIAGNOSES[:18])
        num_meds = random.choice([1, 1, 2, 2, 2, 3])
        meds = []
        used_generics = set()

        for _ in range(num_meds):
            # Pick a med whose generic has stock > 0
            attempts = 0
            while attempts < 50:
                entry = random.choice(BRAND_GENERIC_MAP)
                if entry["generic"] is None:
                    attempts += 1
                    continue
                if entry["class"] in ["controlled", "vasopressor"]:
                    attempts += 1
                    continue
                if entry["generic"] in used_generics:
                    attempts += 1
                    continue
                strength = random.choice(entry["strengths"])
                used_generics.add(entry["generic"])
                freq = random.choice(["OD", "BD", "TDS"])
                dur = random.choice(["3 days", "5 days", "7 days"])
                meds.append({
                    "brand_name": entry["brand"],
                    "dose": strength,
                    "frequency": freq,
                    "duration": dur
                })
                break
            else:
                continue

        notes = random.choice(CLINICAL_NOTES_TEMPLATES).format(duration="5 days")
        patients.append({
            "_scenario": f"HAPPY PATH — Standard discharge #{i+1}",
            "_test_type": "success",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": diag,
            "allergies": [],
            "discharge_medications": meds,
            "clinical_notes": notes
        })
        patient_csv.append((pid, "success"))

    # =========================================================================
    # CATEGORY 2: OUT-OF-STOCK — 20 patients
    # =========================================================================
    oos_brands = [
        ("Augmentin", "625 mg"), ("Taxim-O", "200 mg"), ("Rantac", "150 mg"),
        ("Voveran", "50 mg"), ("Glycomet", "500 mg"), ("Amlopress", "5 mg"),
        ("Losar", "25 mg"), ("Azithral", "250 mg"), ("Omnacortil", "5 mg"),
        ("Pan", "20 mg"),
    ]
    for i in range(20):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        brand, strength = oos_brands[i % len(oos_brands)]
        diag = random.choice(DIAGNOSES)
        meds = [{"brand_name": brand, "dose": strength, "frequency": "BD", "duration": "5 days"}]
        # Add a second in-stock med sometimes
        if i % 3 == 0:
            meds.append({"brand_name": "Crocin", "dose": "500 mg", "frequency": "SOS", "duration": "3 days"})

        patients.append({
            "_scenario": f"OUT-OF-STOCK — Requires alternative suggestion #{i+1}",
            "_test_type": "success",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": diag,
            "allergies": [],
            "discharge_medications": meds,
            "clinical_notes": f"Prescribed {brand} {strength} — currently out of stock. Alternative required."
        })
        patient_csv.append((pid, "success"))

    # =========================================================================
    # CATEGORY 3: RBAC VIOLATIONS — 15 patients
    # =========================================================================
    rbac_tests = [
        ("billing", "get_clinical_notes", "ehr"),
        ("pharmacy", "get_discharge_summary", "ehr"),
        ("clinical", "create_invoice", "billing"),
        ("pharmacy", "create_invoice", "billing"),
        ("billing", "resolve_generic", "pharmacy"),
        ("billing", "check_stock", "pharmacy"),
        ("admin", "get_clinical_notes", "ehr"),
        ("admin", "create_invoice", "billing"),
        ("billing", "get_medication_list", "ehr"),  # billing not in allowed list
    ]
    for i in range(15):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        role, tool, server = rbac_tests[i % len(rbac_tests)]
        patients.append({
            "_scenario": f"RBAC VIOLATION — {role} role calls {tool} on {server} server #{i+1}",
            "_test_type": "failure",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": random.choice(DIAGNOSES),
            "allergies": [],
            "discharge_medications": [
                {"brand_name": "Crocin", "dose": "500 mg", "frequency": "TDS", "duration": "3 days"}
            ],
            "clinical_notes": f"RBAC test case. {role} role should be DENIED access to {tool}.",
            "_rbac_test": {
                "requesting_role": role,
                "tool_called": tool,
                "target_server": server,
                "expected_result": "access_denied"
            }
        })
        patient_csv.append((pid, "failure"))

    # =========================================================================
    # CATEGORY 4: PHI LEAKAGE — 10 patients
    # =========================================================================
    phi_payloads = [
        [{"item": "paracetamol 500 mg", "quantity": 9}, {"item": "Consultation", "diagnosis": "Pneumonia", "quantity": 1}],
        [{"item": "clinical_review", "quantity": 1}],
        [{"item": "amoxicillin + clavulanate 1g", "quantity": 10}, {"item": "Diagnosis: UTI", "quantity": 1}],
        [{"item": "paracetamol 500 mg", "quantity": 6, "clinical_notes": "Patient has history of liver disease"}],
        [{"item": "discharge_summary_clinical", "quantity": 1}],
    ]
    for i in range(10):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        patients.append({
            "_scenario": f"PHI LEAKAGE — Clinical data in billing payload #{i+1}",
            "_test_type": "failure",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": random.choice(DIAGNOSES),
            "allergies": [],
            "discharge_medications": [
                {"brand_name": "Crocin", "dose": "500 mg", "frequency": "TDS", "duration": "3 days"}
            ],
            "clinical_notes": "PHI leakage test. Billing payload should be rejected.",
            "_phi_leakage_test": {
                "malicious_payload": phi_payloads[i % len(phi_payloads)],
                "expected_result": "rejected",
                "expected_error": "PHI LEAKAGE DETECTED"
            }
        })
        patient_csv.append((pid, "failure"))

    # =========================================================================
    # CATEGORY 5: ALLERGY CONFLICTS — 15 patients
    # =========================================================================
    allergy_cases = [
        (["penicillin"], "Augmentin", "625 mg", "penicillin", True),
        (["penicillin"], "Mox", "500 mg", "penicillin", True),
        (["penicillin"], "Amoxil", "500 mg", "penicillin", True),
        (["penicillin"], "Ampilox", "500 mg", "penicillin", True),
        (["penicillin"], "Crocin", "500 mg", "analgesic", False),  # safe
        (["sulfonamides"], "Bactrim", "400+80 mg", "sulfonamide", True),
        (["sulfonamides"], "Septran", "400+80 mg", "sulfonamide", True),
        (["aspirin"], "Ecosprin", "75 mg", "antiplatelet", True),
        (["aspirin"], "Deplatt-A", "75+75 mg", "antiplatelet", True),
        (["nsaid"], "Brufen", "400 mg", "nsaid", True),
        (["nsaid"], "Voveran", "50 mg", "nsaid", True),
        (["penicillin", "sulfonamides"], "Augmentin", "1g", "penicillin", True),
        (["penicillin", "cephalosporin"], "Monocef", "1g", "cephalosporin", True),
        (["codeine"], "Codeine Phosphate", "30 mg", "controlled", True),
        (["ibuprofen"], "Combiflam", "400+325 mg", "nsaid", True),
    ]
    for i in range(15):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        allergies, brand, dose, drug_class, is_unsafe = allergy_cases[i % len(allergy_cases)]
        patients.append({
            "_scenario": f"ALLERGY CONFLICT — {'UNSAFE' if is_unsafe else 'SAFE'} prescription #{i+1}",
            "_test_type": "edge_case",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": random.choice(DIAGNOSES),
            "allergies": allergies,
            "discharge_medications": [
                {"brand_name": brand, "dose": dose, "frequency": "BD", "duration": "5 days"}
            ],
            "clinical_notes": f"Patient has allergies: {', '.join(allergies)}. {brand} is {'UNSAFE' if is_unsafe else 'SAFE'}.",
            "_allergy_test": {
                "allergies": allergies,
                "prescribed_brand": brand,
                "prescribed_class": drug_class,
                "is_unsafe": is_unsafe,
                "requires_doctor_review": is_unsafe
            }
        })
        patient_csv.append((pid, "edge_case"))

    # =========================================================================
    # CATEGORY 6: DUPLICATE BILLING — 10 patients
    # =========================================================================
    dup_cases = [
        ("Crocin", "Calpol", "500 mg", "paracetamol"),      # two brands same generic
        ("Tylenol", "Dolo", "650 mg", "paracetamol"),        # NOTE: mismatch strengths (500 vs 650) — tricky
        ("Crocin", None, "500 mg", "paracetamol"),           # brand + generic name
        ("Tylenol", "Metacin", "500 mg", "paracetamol"),
        ("Ciplox", "Cifran", "500 mg", "ciprofloxacin"),
        ("Azithral", "Azee", "500 mg", "azithromycin"),
        ("Atorva", "Lipitor", "20 mg", "atorvastatin"),
        ("Clopilet", "Plavix", "75 mg", "clopidogrel"),
        ("Omez", "Pantocid", "20 mg", "different_generic"),  # trap: similar class but different generics (omeprazole vs pantoprazole) — NOT a duplicate
        ("Brufen", "Ibugesic", "400 mg", "ibuprofen"),
    ]
    for i in range(10):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        brand1, brand2, dose, generic = dup_cases[i]
        meds = [{"brand_name": brand1, "dose": dose, "frequency": "TDS", "duration": "3 days"}]
        if brand2:
            meds.append({"brand_name": brand2, "dose": dose, "frequency": "TDS", "duration": "3 days"})
        else:
            meds.append({"generic_name": generic.title(), "dose": dose, "frequency": "TDS", "duration": "3 days"})

        is_true_dup = generic != "different_generic"
        patients.append({
            "_scenario": f"DUPLICATE BILLING — {'TRUE duplicate' if is_true_dup else 'FALSE POSITIVE (different generics)'} #{i+1}",
            "_test_type": "edge_case",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": random.choice(DIAGNOSES),
            "allergies": [],
            "discharge_medications": meds,
            "clinical_notes": f"{'Duplicate detected' if is_true_dup else 'NOT a duplicate'}: {brand1} and {brand2 or generic}.",
            "_duplicate_test": {
                "brand_1": brand1,
                "brand_2": brand2 or f"(generic: {generic})",
                "is_true_duplicate": is_true_dup,
                "expected_deduplicated": is_true_dup
            }
        })
        patient_csv.append((pid, "edge_case"))

    # =========================================================================
    # CATEGORY 7: SIMILAR DRUG NAMES — 5 patients (trap)
    # =========================================================================
    similar_pairs = [
        ("Dopmin", "Dobutrex", "dopamine", "dobutamine"),
        ("Losartan", "Losar-H", "losartan", "losartan + hydrochlorothiazide"),
        ("Clopilet", "Ecosprin", "clopidogrel", "aspirin"),  # not similar name but confused in practice
        ("Metoprolol", "Metformin", "metoprolol", "metformin"),  # similar prefix
        ("Prednisolone", "Methylprednisolone", "prednisolone", "methylprednisolone"),
    ]
    for i, (brand1, brand2, gen1, gen2) in enumerate(similar_pairs):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        # Find entries
        b1_entry = next((e for e in BRAND_GENERIC_MAP if e["brand"] == brand1), None)
        b2_entry = next((e for e in BRAND_GENERIC_MAP if e["brand"] == brand2), None)
        s1 = b1_entry["strengths"][0] if b1_entry else "10 mg"
        s2 = b2_entry["strengths"][0] if b2_entry else "10 mg"

        patients.append({
            "_scenario": f"SIMILAR DRUG NAMES — {gen1} vs {gen2} confusion trap #{i+1}",
            "_test_type": "edge_case",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": random.choice(DIAGNOSES),
            "allergies": [],
            "discharge_medications": [
                {"brand_name": brand1, "dose": s1, "frequency": "BD", "duration": "5 days"},
                {"brand_name": brand2, "dose": s2, "frequency": "BD", "duration": "5 days"}
            ],
            "clinical_notes": f"CAUTION: {gen1} and {gen2} are DIFFERENT drugs despite similar names. Do NOT deduplicate.",
            "_similar_name_test": {
                "drug_1": gen1,
                "drug_2": gen2,
                "are_same_drug": False,
                "should_deduplicate": False
            }
        })
        patient_csv.append((pid, "edge_case"))

    # =========================================================================
    # CATEGORY 8: CONTROLLED SUBSTANCES — 5 patients (billing trap)
    # =========================================================================
    controlled_brands = ["Morphine Sulfate", "Durogesic", "OxyContin", "Codeine Phosphate", "Buprigesic"]
    for i, brand in enumerate(controlled_brands):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        entry = next(e for e in BRAND_GENERIC_MAP if e["brand"] == brand)
        patients.append({
            "_scenario": f"CONTROLLED SUBSTANCE — Billing must NOT see full clinical details #{i+1}",
            "_test_type": "edge_case",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": "Post-operative pain management — major surgery",
            "allergies": [],
            "discharge_medications": [
                {"brand_name": brand, "dose": entry["strengths"][0], "frequency": "SOS", "duration": "3 days"},
                {"brand_name": "Crocin", "dose": "500 mg", "frequency": "TDS", "duration": "5 days"}
            ],
            "clinical_notes": f"CONTROLLED SUBSTANCE: {brand} prescribed for severe pain. Billing should only see billable item name and quantity — NO clinical notes, NO diagnosis, NO prescription justification.",
            "_controlled_substance_test": {
                "controlled_drug": brand,
                "generic": entry["generic"],
                "billing_should_see": {"item": f"{entry['generic']} {entry['strengths'][0]}", "quantity": 6},
                "billing_must_NOT_see": ["clinical_notes", "diagnosis_summary", "prescription_justification", "pain_score", "controlled_substance_schedule"]
            }
        })
        patient_csv.append((pid, "edge_case"))

    # =========================================================================
    # CATEGORY 9: MISSING / MALFORMED DATA — 5 patients
    # =========================================================================
    missing_cases = [
        {"brand_name": "Crocin", "dose": "", "frequency": "SOS", "duration": "3 days"},        # empty dose
        {"brand_name": "Augmentin", "dose": "625 mg", "frequency": "", "duration": "5 days"},  # empty frequency
        {"brand_name": "Crocin", "dose": "500 mg", "frequency": "TDS", "duration": ""},        # empty duration
        {"brand_name": "", "dose": "500 mg", "frequency": "BD", "duration": "5 days"},          # empty brand
        {"brand_name": "Crocin", "dose": "500 mg"},                                              # missing frequency+duration
    ]
    for i, med in enumerate(missing_cases):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        patients.append({
            "_scenario": f"MISSING DATA — Malformed medication record #{i+1}",
            "_test_type": "edge_case",
            "patient_id": pid,
            "discharge_status": "ready",
            "diagnosis_summary": random.choice(DIAGNOSES),
            "allergies": [],
            "discharge_medications": [med],
            "clinical_notes": f"Data quality issue: medication record has missing fields. System should flag for human review.",
            "_missing_data_test": {
                "missing_field": [k for k, v in med.items() if v == ""] + [f for f in ["frequency", "duration"] if f not in med],
                "expected_result": "validation_error",
                "requires_human_review": True
            }
        })
        patient_csv.append((pid, "edge_case"))

    # =========================================================================
    # CATEGORY 10: PATIENT NOT FOUND / NOT READY — 5 patients
    # =========================================================================
    for i in range(3):
        patient_counter += 1
        pid = f"P-{9990 + i}"
        patients.append({
            "_scenario": f"PATIENT NOT FOUND — ID does not exist in EHR #{i+1}",
            "_test_type": "failure",
            "patient_id": pid,
            "discharge_status": "unknown",
            "diagnosis_summary": "N/A",
            "allergies": [],
            "discharge_medications": [],
            "clinical_notes": "",
            "_edge_case": {
                "expected_result": "Patient not found.",
                "reason": "Patient ID does not exist in EHR_DATA."
            }
        })
        patient_csv.append((pid, "failure"))

    for i in range(2):
        patient_counter += 1
        pid = f"P-{patient_counter}"
        patients.append({
            "_scenario": f"NOT READY FOR DISCHARGE — Workflow must halt #{i+1}",
            "_test_type": "edge_case",
            "patient_id": pid,
            "discharge_status": "not_ready",
            "diagnosis_summary": random.choice(["Acute myocardial infarction", "Septic shock", "ICU — ventilator dependent"]),
            "allergies": random.choice(ALLERGY_OPTIONS),
            "discharge_medications": [],
            "clinical_notes": "Patient still under critical care. Discharge NOT appropriate. Workflow must halt.",
            "_edge_case": {
                "expected_workflow_action": "abort_discharge",
                "reason": "discharge_status is 'not_ready'."
            }
        })
        patient_csv.append((pid, "edge_case"))

    return patients, patient_csv

# =============================================================================
# 5. RBAC POLICIES — 30 entries
# =============================================================================

RBAC_POLICIES = [
    # EHR Server tools
    {"tool": "get_discharge_summary", "server": "ehr_server", "allowed_roles": ["clinical", "discharge"], "denied_roles": ["billing", "pharmacy", "admin"]},
    {"tool": "get_medication_list", "server": "ehr_server", "allowed_roles": ["clinical", "discharge", "pharmacy"], "denied_roles": ["billing", "admin"]},
    {"tool": "get_clinical_notes", "server": "ehr_server", "allowed_roles": ["clinical"], "denied_roles": ["billing", "pharmacy", "discharge", "admin"],
     "sensitivity": "HIGH — Contains PHI. Only clinical role allowed."},
    # Pharmacy Server tools
    {"tool": "resolve_generic", "server": "pharmacy_server", "allowed_roles": ["pharmacy", "discharge"], "denied_roles": ["billing", "clinical", "admin"]},
    {"tool": "check_stock", "server": "pharmacy_server", "allowed_roles": ["pharmacy", "discharge"], "denied_roles": ["billing", "clinical", "admin"]},
    {"tool": "suggest_alternative", "server": "pharmacy_server", "allowed_roles": ["pharmacy", "discharge"], "denied_roles": ["billing", "clinical", "admin"]},
    # Billing Server tools
    {"tool": "get_billing_code", "server": "billing_server", "allowed_roles": ["billing", "discharge"], "denied_roles": ["clinical", "pharmacy", "admin"]},
    {"tool": "create_invoice", "server": "billing_server", "allowed_roles": ["billing", "discharge"], "denied_roles": ["clinical", "pharmacy", "admin"],
     "phi_guard": "Rejects payloads containing 'diagnosis' or 'clinical' substrings."},
    {"tool": "validate_invoice", "server": "billing_server", "allowed_roles": ["billing", "discharge"], "denied_roles": ["clinical", "pharmacy", "admin"]},
    # Cross-boundary test cases
    {"_test": "billing_reads_clinical_notes", "role": "billing", "tool": "get_clinical_notes", "server": "ehr_server", "expected": "access_denied", "reason": "PHI boundary violation"},
    {"_test": "pharmacy_reads_diagnosis", "role": "pharmacy", "tool": "get_discharge_summary", "server": "ehr_server", "expected": "access_denied", "reason": "Role not permitted"},
    {"_test": "clinical_creates_invoice", "role": "clinical", "tool": "create_invoice", "server": "billing_server", "expected": "access_denied", "reason": "Separation of concerns"},
    {"_test": "pharmacy_creates_invoice", "role": "pharmacy", "tool": "create_invoice", "server": "billing_server", "expected": "access_denied", "reason": "Separation of concerns"},
    {"_test": "billing_resolves_generic", "role": "billing", "tool": "resolve_generic", "server": "pharmacy_server", "expected": "access_denied", "reason": "Billing has no pharmacy access"},
    {"_test": "billing_checks_stock", "role": "billing", "tool": "check_stock", "server": "pharmacy_server", "expected": "access_denied", "reason": "Billing has no pharmacy access"},
    {"_test": "admin_reads_notes", "role": "admin", "tool": "get_clinical_notes", "server": "ehr_server", "expected": "access_denied", "reason": "Admin role not implemented"},
    {"_test": "admin_creates_invoice", "role": "admin", "tool": "create_invoice", "server": "billing_server", "expected": "access_denied", "reason": "Admin role not implemented"},
    {"_test": "discharge_reads_notes", "role": "discharge", "tool": "get_clinical_notes", "server": "ehr_server", "expected": "access_denied", "reason": "Even discharge cannot read clinical notes"},
    {"_test": "discharge_full_happy_path", "role": "discharge", "tools": ["get_medication_list", "resolve_generic", "check_stock", "suggest_alternative", "create_invoice", "validate_invoice"], "expected": "all_allowed", "reason": "Discharge role is the orchestrator"},
    {"_test": "clinical_full_ehr_access", "role": "clinical", "tools": ["get_discharge_summary", "get_medication_list", "get_clinical_notes"], "expected": "all_allowed", "reason": "Clinical has full EHR read access"},
    {"_test": "billing_limited_access", "role": "billing", "tools": ["get_billing_code", "create_invoice", "validate_invoice"], "expected": "all_allowed", "reason": "Billing can only use billing tools"},
    {"_test": "pharmacy_limited_access", "role": "pharmacy", "tools": ["resolve_generic", "check_stock", "suggest_alternative", "get_medication_list"], "expected": "all_allowed", "reason": "Pharmacy can use pharmacy tools + read med list"},
    # PHI Leakage guards
    {"_test": "phi_diagnosis_in_payload", "tool": "create_invoice", "payload_contains": "diagnosis", "expected": "rejected", "reason": "PHI leakage — diagnosis keyword detected"},
    {"_test": "phi_clinical_in_payload", "tool": "create_invoice", "payload_contains": "clinical", "expected": "rejected", "reason": "PHI leakage — clinical keyword detected"},
    {"_test": "phi_clinical_notes_in_item", "tool": "create_invoice", "payload_contains": "clinical_notes", "expected": "rejected", "reason": "PHI leakage — clinical_notes substring detected"},
    {"_test": "phi_clean_payload", "tool": "create_invoice", "payload_contains": "item + quantity only", "expected": "accepted", "reason": "Clean payload — no PHI detected"},
    # Controlled substance boundaries
    {"_test": "controlled_substance_billing", "tool": "create_invoice", "constraint": "Billing must receive only item name and quantity for controlled substances", "blocked_fields": ["clinical_notes", "diagnosis_summary", "prescription_justification", "dea_number", "controlled_schedule"]},
    {"_test": "controlled_substance_pharmacy", "tool": "resolve_generic", "constraint": "Pharmacy can resolve controlled substance brands to generics", "expected": "allowed"},
    # Edge: role escalation attempt
    {"_test": "role_escalation_attempt", "role": "billing", "attempts": "Pass context_role='clinical' to bypass RBAC", "expected": "access_denied", "reason": "RBAC is enforced at tool level, not just prompt level"},
    {"_test": "empty_role", "role": "", "tool": "get_clinical_notes", "expected": "access_denied", "reason": "Empty role should be denied"},
]

# =============================================================================
# 6. GENERATE BILLING INPUTS from patients
# =============================================================================

def generate_billing_inputs(patients, brand_generic_map, inventory, billing_catalog):
    billing_inputs = []
    bg_map = {e["brand"].lower(): e for e in brand_generic_map if e["generic"]}
    cat_map = {c["item_name"]: c for c in billing_catalog}

    for patient in patients:
        if patient["_test_type"] == "failure" and "_rbac_test" in patient:
            continue  # RBAC tests don't produce billing inputs
        if patient["_test_type"] == "failure" and "_phi_leakage_test" in patient:
            # These produce the malicious payload
            billing_inputs.append({
                "_scenario": patient["_scenario"],
                "_test_type": "failure",
                "patient_id": patient["patient_id"],
                "billable_items": patient["_phi_leakage_test"]["malicious_payload"],
                "_expected_output": {"error": "PHI LEAKAGE DETECTED: Clinical data found in billing payload. Request rejected."}
            })
            continue
        if patient.get("discharge_status") != "ready":
            continue
        if not patient.get("discharge_medications"):
            billing_inputs.append({
                "_scenario": patient["_scenario"],
                "_test_type": patient["_test_type"],
                "patient_id": patient["patient_id"],
                "billable_items": [],
                "_expected_output": {"status": "created", "items": [], "total_amount": 0.0}
            })
            continue

        items = []
        for med in patient["discharge_medications"]:
            brand = med.get("brand_name", "")
            dose = med.get("dose", "")
            freq = med.get("frequency", "BD")
            dur = med.get("duration", "5 days")

            if not brand and not med.get("generic_name"):
                continue
            if not dose:
                continue

            if brand:
                entry = bg_map.get(brand.lower())
                if entry:
                    generic = entry["generic"]
                else:
                    generic = None
            else:
                generic = med.get("generic_name", "").lower()

            if generic:
                item_name = f"{generic} {dose}".lower()
                qty = calc_quantity(freq, dur) if dur and freq else 1
                items.append({"item": item_name, "quantity": qty})

        if items:
            billing_inputs.append({
                "_scenario": patient["_scenario"],
                "_test_type": patient["_test_type"],
                "patient_id": patient["patient_id"],
                "billable_items": items,
            })

    return billing_inputs


# =============================================================================
# MAIN GENERATION
# =============================================================================

def main():
    print("Generating synthetic data...")

    # Generate inventory & catalog
    inventory = generate_inventory(BRAND_GENERIC_MAP)
    billing_catalog = generate_billing_catalog(inventory)

    # Generate patients
    patients, patient_csv = generate_patients()

    # Generate billing inputs
    billing_inputs = generate_billing_inputs(patients, BRAND_GENERIC_MAP, inventory, billing_catalog)

    # =========================================================================
    # WRITE synthetic_records.json (EHR)
    # =========================================================================
    ehr_output = {
        "ehr_records": patients,
        "metadata": {
            "total_records": len(patients),
            "by_type": {
                "success": sum(1 for p in patients if p["_test_type"] == "success"),
                "failure": sum(1 for p in patients if p["_test_type"] == "failure"),
                "edge_case": sum(1 for p in patients if p["_test_type"] == "edge_case"),
            }
        }
    }
    with open(os.path.join(OUTPUT_DIR, "synthetic_records.json"), "w", encoding="utf-8") as f:
        json.dump(ehr_output, f, indent=2, ensure_ascii=False)
    print(f"  [OK] synthetic_records.json — {len(patients)} EHR records")

    # =========================================================================
    # WRITE synthetic_pharmacy_records.json
    # =========================================================================
    brand_generic_output = []
    for entry in BRAND_GENERIC_MAP:
        brand_generic_output.append({
            "brand_name": entry["brand"],
            "generic_name": entry["generic"],
            "drug_class": entry["class"],
            "strengths": entry["strengths"]
        })

    pharmacy_output = {
        "brand_to_generic": brand_generic_output,
        "inventory": inventory,
        "rbac_permissions": RBAC_POLICIES,
        "metadata": {
            "total_brand_generic_mappings": len(brand_generic_output),
            "total_inventory_records": len(inventory),
            "total_rbac_policies": len(RBAC_POLICIES),
            "out_of_stock_items": sum(1 for i in inventory if i["stock"] == 0)
        }
    }
    with open(os.path.join(OUTPUT_DIR, "synthetic_pharmacy_records.json"), "w", encoding="utf-8") as f:
        json.dump(pharmacy_output, f, indent=2, ensure_ascii=False)
    print(f"  [OK] synthetic_pharmacy_records.json — {len(brand_generic_output)} mappings, {len(inventory)} inventory, {len(RBAC_POLICIES)} RBAC")

    # =========================================================================
    # WRITE synthetic_billing_records.json
    # =========================================================================
    billing_output = {
        "billing_catalog": billing_catalog,
        "billing_inputs": billing_inputs,
        "phi_boundary_rules": {
            "blocked_keywords": ["diagnosis", "clinical"],
            "detection_method": "if 'diagnosis' in str(item).lower() or 'clinical' in str(item).lower()",
            "safe_fields": ["item", "quantity"],
            "action_on_violation": "Entire invoice rejected"
        },
        "rbac_permissions": {
            "create_invoice": {"allowed": ["billing", "discharge"], "denied": ["clinical", "pharmacy", "admin"]},
            "validate_invoice": {"allowed": ["billing", "discharge"], "denied": ["clinical", "pharmacy", "admin"]},
            "get_billing_code": {"allowed": ["billing", "discharge"], "denied": ["clinical", "pharmacy", "admin"]}
        },
        "metadata": {
            "total_catalog_items": len(billing_catalog),
            "total_billing_inputs": len(billing_inputs),
        }
    }
    with open(os.path.join(OUTPUT_DIR, "synthetic_billing_records.json"), "w", encoding="utf-8") as f:
        json.dump(billing_output, f, indent=2, ensure_ascii=False)
    print(f"  [OK] synthetic_billing_records.json — {len(billing_catalog)} catalog, {len(billing_inputs)} inputs")

    # =========================================================================
    # WRITE patient_classification.csv
    # =========================================================================
    csv_path = os.path.join(OUTPUT_DIR, "patient_classification.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Patient ID", "Classification"])
        for pid, cls in patient_csv:
            writer.writerow([pid, cls])
    print(f"  [OK] patient_classification.csv — {len(patient_csv)} rows")

    # Summary
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"EHR Records:              {len(patients)}")
    print(f"  - Success (happy path): {sum(1 for p in patients if p['_test_type'] == 'success')}")
    print(f"  - Failure:              {sum(1 for p in patients if p['_test_type'] == 'failure')}")
    print(f"  - Edge Case:            {sum(1 for p in patients if p['_test_type'] == 'edge_case')}")
    print(f"Brand-Generic Mappings:   {len(brand_generic_output)}")
    print(f"Pharmacy Inventory:       {len(inventory)}")
    print(f"Billing Catalog:          {len(billing_catalog)}")
    print(f"Billing Inputs:           {len(billing_inputs)}")
    print(f"RBAC Policies:            {len(RBAC_POLICIES)}")
    print(f"CSV Classification:       {len(patient_csv)} rows")
    print(f"{'='*60}")
    print(f"\nTraps included:")
    print(f"  [OK] Brand-generic mismatch (penicillin class brands)")
    print(f"  [OK] Out of stock (10 items with stock=0, alternatives provided)")
    print(f"  [OK] Similar drug names (dopamine vs dobutamine, metoprolol vs metformin)")
    print(f"  [OK] Controlled substances (5 cases — billing sees only item+qty)")
    print(f"  [OK] Wrong department access (15 RBAC violation cases)")
    print(f"  [OK] Missing dosage (5 malformed medication records)")
    print(f"  [OK] Allergy conflict (15 cases including multi-allergy)")
    print(f"  [OK] Duplicate billing (10 cases including false positive trap)")
    print(f"  [OK] PHI leakage (10 cases with various payload violations)")

if __name__ == "__main__":
    main()
