import json


def main():
    with open("clinical_data/SiteC-dataset_clinical_ingest.json", "r") as f:
        node3_data = json.load(f)

    program_names = {
        "SiteC-SYNTH_01": "N3_S01",
        "SiteC-SYNTH_02": "N3_S02",
        "SiteC-SYNTH_03": "N3_S03",
        "SiteC-SYNTH_04": "N3_S04"

    }
    indices = list(range(0, 19, 1)) + list(range(199, 224, 1)) + list(range(399, 424, 1)) + list(range(599, 624, 1))
    reduced_donors = [node3_data['donors'][x] for x in indices]
    for donor in reduced_donors:
        donor['program_id'] = program_names[donor['program_id']]
        for pd in donor['primary_diagnoses']:
            if 'primary_site' in pd:
                if pd['primary_site'] == "Bronchus and Lung":
                    pd['primary_site'] = "Breast"
    node3_data['donors'] = reduced_donors
    with open("SiteC-filtered.json", "w+") as f:
        json.dump(node3_data, f)
    print("hello")



if __name__ == "__main__":
    main()
