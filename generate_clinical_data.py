from git import Repo
import shutil
from clinical_etl.schema import ValidationError
import os
import sys
import subprocess
import json
import pandas as pd


def main():
    ingest_repo_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_path = "tmp-data"
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    print(f"Cloning mohccn-synthetic-data repo into {tmp_path}")
    synth_repo = Repo.clone_from("https://github.com/CanDIG/mohccn-synthetic-data.git", tmp_path)
    dataset_prefixes = ["SiteA", "SiteB", "SiteC"]

    # make some edits to the synthetic data
    samples = pd.read_csv("tmp-data/medium_dataset_csv/raw_data/SampleRegistration.csv")
    samples['sample_type'] = 'Total DNA'
    samples['tumour_normal_designation'] = 'Normal'
    samples['specimen_tissue_source'] = 'Whole blood'
    samples['specimen_type'] = 'Normal'
    samples.to_csv("tmp-data/medium_dataset_csv/raw_data/SampleRegistration.csv", index=False)

    for prefix in dataset_prefixes:
        try:
            process = subprocess.run([f'python {tmp_path}/src/csv_to_ingest.py --size m --prefix {prefix}'],
                                     shell=True, check=True, capture_output=True)
            output_dir = f"{tmp_path}/custom_dataset_csv-{prefix}"

            with open(f'{output_dir}/raw_data_validation_results.json') as f:
                validation_results = json.load(f)
                if len(validation_results['validation_errors']) > 0:
                    raise ValidationError("Clinical etl conversion failed to create an ingestable json file, "
                                          "please check the errors in tests/clinical_data_validation_results.json and "
                                          "try again.")

        except ValidationError as e:
            print(e)
            print(f"Moving validation results file to clinical_data.")
            shutil.move(f"{output_dir}/raw_data_validation_results.json",
                        f"clinical_data/{prefix}-dataset_clinical_ingest_validation_results.json")
            print("Removing repo.")
            shutil.rmtree(tmp_path)
            sys.exit(0)

        print("Ingestable JSON successfully created, moving output json files to tests directory")
        shutil.move(f"{output_dir}/raw_data_map.json",
                    f"clinical_data/{prefix}-dataset_clinical_ingest.json")

    print("Removing repo.")
    shutil.rmtree(tmp_path)


if __name__ == "__main__":
    main()