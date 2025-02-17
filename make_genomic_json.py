import json


def make_linking_json(sample_name, s3_dir, program_name, sample_number, site_name):
    linking_json = {
            "program_id": f"{program_name}",  # The name of the program
            "genomic_file_id": f"{sample_name}-chr17-vcf",
            # The identifier used to identify the genomic file, usually the filename, minus extensions
            "main": {  # location and name of the main genomic file, bam/cram/vcf
                "access_method": f"{s3_dir}ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz",
                "name": f"ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz"
            },
            "index": {  # location and name of the index for the main genomic file, bai/crai/
                "access_method": f"{s3_dir}ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz.tbi",
                "name": f"ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.{sample_name}.vcf.gz.tbi"
            },
            "metadata": {  # Metadata about the file
                "sequence_type": "wgs",
                # type of data sequenced (whole genome or whole transcriptome), allowed values: [wgs, wts]
                "data_type": "variant",  # type of data represented, allowed values: [variant, read]
                "reference": "hg38"  # which reference genome was used for alignment, allowed values: [hg37, hg38]
            },
            "samples": [  # Linkage to one or more samples that the genomic file was derived from
                {
                    "genomic_file_sample_id": sample_name,  # The name of the sample in the genomic file
                    "submitter_sample_id": f"{site_name}-SAMPLE_{sample_number}"  # The submitter_sample_id to link to
                }
            ]
        }
    return linking_json


def get_file_list(linking_json):
    vcf_files = [x['main']['name'] for x in linking_json]
    tbi_files = [x['index']['name'] for x in linking_json]
    vcf_files.extend(tbi_files)
    return vcf_files


def main():
    with open("1000G-samples-list.txt", "r") as f:
        samples = f.read()
        sample_list = samples.split("\n")
    with open("s3_addresses.json", "r") as f:
        s3_addresses = json.load(f)
    synth_size = 600
    site_a_genomic_json = []
    site_b_genomic_json = []
    site_c_genomic_json = []

    for j in range(0, 4):
        #print(f"j is: {j}")
        for i in range(0, synth_size, 3):
            #print(f"i is: {i}")
            s1_sample = sample_list.pop()
            #print(f"s1_sample is: {s1_sample}")
            sample_number = str((i + 1) + (j * synth_size)).zfill(4)
            #print(f"sample_number: {sample_number}")
            site_a_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteA"],
                                                         f"SiteA-SYNTH_0{j+1}", sample_number,
                                                         "SiteA"))

            s1_sample = sample_list.pop()
            site_b_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteB"],
                                                         f"SiteB-SYNTH_0{j+1}", sample_number,
                                                         "SiteB"))

            s1_sample = sample_list.pop()
            site_c_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteC"],
                                                         f"SiteC-SYNTH_0{j+1}", sample_number,
                                                         "SiteC"))


    for i in range(1, 6, 3):
        s1_sample = sample_list.pop()
        sample_number = str(i).zfill(4)
        site_a_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteA"],
                                                     f"SiteA-SYNTH_01", f"ALL_{sample_number}",
                                                     "SiteA"))
        s1_sample = sample_list.pop()
        site_a_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteA"],
                                                     f"SiteA-SYNTH_01", f"NULL_{sample_number}",
                                                     "SiteA"))

        s1_sample = sample_list.pop()
        sample_number = str(i).zfill(4)
        site_b_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteB"],
                                                     f"SiteB-SYNTH_01", f"ALL_{sample_number}",
                                                     "SiteB"))
        s1_sample = sample_list.pop()
        site_b_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteB"],
                                                     f"SiteB-SYNTH_01", f"NULL_{sample_number}",
                                                     "SiteB"))

        s1_sample = sample_list.pop()
        sample_number = str(i).zfill(4)
        site_c_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteC"],
                                                     f"SiteC-SYNTH_01", f"ALL_{sample_number}",
                                                     "SiteC"))
        s1_sample = sample_list.pop()
        site_c_genomic_json.append(make_linking_json(s1_sample, s3_addresses["SiteC"],
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
