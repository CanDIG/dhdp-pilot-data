import json


def make_experiment(sample_name, program_name, sample_number, site_name):
    experiment_json = {
        "program_id": program_name,
        "experiment_id": f"{site_name}-SAMPLE_{sample_number}-EXP",
        "submitter_sample_id": sample_name,
        "metadata": {
            "library_strategy": "WGS",
            "library_description": "1000Genomes data, variants from chromosome 17, see their documentation for full details",
            "instrument": "Illumina HiSeq 2500",
            "library_selection": "size fractionation",
            "protocol": "https://www.internationalgenome.org/",
            "library_source": "genomic",
            "library_layout": "paired"
        }
    }
    return experiment_json


def make_analysis(sample_name, s3_dir, program_name, sample_number, site_name):
    analysis_json = {
        "program_id": program_name,
        "analysis_id": f"{sample_name}-chr17-vcf",
        "metadata": {
            "analysis_type": "sequence_variation",
            "analysis_attribute": {
                "subtype": "mutation"
            },
            "reference": "hg38",
            "reference_sequence_type": "Whole genome sequencing",
            "analysis_centre": "1000Genomes"
        },
        "main": {
            "access_method": f"{s3_dir}ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz",
            "name": f"ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz"
        },
        "index": {
            "access_method": f"{s3_dir}ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz.tbi",
            "name": f"ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz.tbi"
        },
        "samples": {
            "experiment_id": f"{site_name}-SAMPLE_{sample_number}-EXP",
            "analysis_sample_id": sample_name
        }
    }
    return analysis_json


def get_file_list(linking_json):
    vcf_files = [x['main']['name'] for x in linking_json["analyses"]]
    tbi_files = [x['index']['name'] for x in linking_json["analyses"]]
    vcf_files.extend(tbi_files)
    return vcf_files


def main():
    with open("1000G-samples-list.txt", "r") as f:
        samples = f.read()
        sample_list = samples.split("\n")
    with open("s3_addresses.json", "r") as f:
        s3_addresses = json.load(f)
    synth_size = 600
    site_a_genomic_json = {"experiments": [], "analyses": []}
    site_b_genomic_json = {"experiments": [], "analyses": []}
    site_c_genomic_json = {"experiments": [], "analyses": []}

    for j in range(0, 4):
        # print(f"j is: {j}")
        for i in range(0, synth_size, 3):
            # print(f"i is: {i}")
            s1_sample = sample_list.pop()
            # print(f"s1_sample is: {s1_sample}")
            sample_number = str((i + 1) + (j * synth_size)).zfill(4)
            # print(f"sample_number: {sample_number}")
            site_a_genomic_json["experiments"].append(make_experiment(s1_sample,
                                                                      f"SiteA-SYNTH_0{j + 1}", sample_number,
                                                                      "SiteA"))
            site_a_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteA"],
                                                                 f"SiteA-SYNTH_0{j + 1}", sample_number,
                                                                 "SiteA"))

            s1_sample = sample_list.pop()
            site_b_genomic_json["experiments"].append(make_experiment(s1_sample,
                                                                      f"SiteB-SYNTH_0{j + 1}", sample_number,
                                                                      "SiteB"))
            site_b_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteB"],
                                                                 f"SiteB-SYNTH_0{j + 1}", sample_number,
                                                                 "SiteB"))
            s1_sample = sample_list.pop()
            site_c_genomic_json["experiments"].append(make_experiment(s1_sample,
                                                                      f"SiteC-SYNTH_0{j + 1}", sample_number,
                                                                      "SiteC"))
            site_c_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteC"],
                                                                 f"SiteC-SYNTH_0{j + 1}", sample_number,
                                                                 "SiteC"))

    for i in range(1, 6, 3):
        s1_sample = sample_list.pop()
        sample_number = str(i).zfill(4)
        site_a_genomic_json["experiments"].append(make_experiment(s1_sample,f"SiteA-SYNTH_01",
                                                   f"ALL_{sample_number}","SiteA"))
        site_a_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteA"],
                                                     f"SiteA-SYNTH_01", f"ALL_{sample_number}",
                                                     "SiteA"))
        s1_sample = sample_list.pop()
        site_a_genomic_json["experiments"].append(make_experiment(s1_sample, f"SiteA-SYNTH_01",
                                                                  f"NULL_{sample_number}", "SiteA"))
        site_a_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteA"],
                                                                 f"SiteA-SYNTH_01", f"NULL_{sample_number}",
                                                                 "SiteA"))
        s1_sample = sample_list.pop()
        sample_number = str(i).zfill(4)
        site_b_genomic_json["experiments"].append(make_experiment(s1_sample, f"SiteB-SYNTH_01",
                                                                  f"ALL_{sample_number}", "SiteB"))
        site_b_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteB"],
                                                                 f"SiteB-SYNTH_01", f"ALL_{sample_number}",
                                                                 "SiteB"))
        s1_sample = sample_list.pop()
        site_b_genomic_json["experiments"].append(make_experiment(s1_sample, f"SiteB-SYNTH_01",
                                                                  f"NULL_{sample_number}", "SiteB"))
        site_b_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteB"],
                                                                 f"SiteB-SYNTH_01", f"NULL_{sample_number}",
                                                                 "SiteB"))

        s1_sample = sample_list.pop()
        sample_number = str(i).zfill(4)
        site_c_genomic_json["experiments"].append(make_experiment(s1_sample, f"SiteC-SYNTH_01",
                                                                  f"ALL_{sample_number}", "SiteC"))
        site_c_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteC"],
                                                                 f"SiteC-SYNTH_01", f"ALL_{sample_number}",
                                                                 "SiteC"))
        s1_sample = sample_list.pop()
        site_c_genomic_json["experiments"].append(make_experiment(s1_sample, f"SiteC-SYNTH_01",
                                                                  f"NULL_{sample_number}", "SiteC"))
        site_c_genomic_json["analyses"].append(make_analysis(s1_sample, s3_addresses["SiteC"],
                                                                 f"SiteC-SYNTH_01", f"NULL_{sample_number}",
                                                                 "SiteC"))

    site_a_files = get_file_list(site_a_genomic_json)
    with open("genomic_data/SiteA_files.txt", "w") as f:
        f.writelines("\n".join(site_a_files))
    site_b_files = get_file_list(site_b_genomic_json)
    with open("genomic_data/SiteB_files.txt", "w") as f:
        f.writelines("\n".join(site_b_files))
    site_c_files = get_file_list(site_c_genomic_json)
    with open("genomic_data/SiteC_files.txt", "w") as f:
        f.writelines("\n".join(site_c_files))

    with open("genomic_data/SiteA_genomic.json", "w") as f:
        json.dump(site_a_genomic_json, f)
    with open("genomic_data/SiteB_genomic.json", "w") as f:
        json.dump(site_b_genomic_json, f)
    with open("genomic_data/SiteC_genomic.json", "w") as f:
        json.dump(site_c_genomic_json, f)


if __name__ == "__main__":
    main()
