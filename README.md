# Scripts for preparing dhdp pilot synthetic data

## Description

The output data is:
* A 1000G vcf file that has been split into individual sample VCFs
* Clinical datasets for 3 sites name SiteA, SiteB, SiteC as separate ingestable jsons
* Genomic jsons linking the split vcf files to the clinical data at each site

## 1000G VCFs

VCF files are from the 1000 Genomes project: https://www.internationalgenome.org/

There are 2548 samples in the 1000G file, it takes a long time to split so hopefully you already have been given access to those split files. If you haven't, or want to know how it is done you will need to:

* Download and install bcftools
* Download the chromosome 17 1000g vcf and tbi files from:
  * ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz.tbi
  * ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz

* Run the split_vcf script that splits the file into individual samples and indexes all vcfs (this may take days depending on how much resource you give it)

## Clinical data

The clinical data at all three sites is exactly the same and slightly modified from the `medium` dataset in the [mohccn synthetic data repo](https://github.com/CanDIG/mohccn-synthetic-data). If you need to generate the data for the three sites:
* Run the `generate_clinical_data.py` script. 
* Data is output to the `clinical_data` directory.

## Genomic linking genomic data files

Assuming you have access to the split vcf files outlined above and have uploaded them into 3 s3 buckets somewhere, edit the `s3_addresses.json` with the s3 address of the bucket for each site.

Then run `make_genomic_json.py`. This will output a genomic linking json and file list for each site. Then simply upload the specified files to the correct s3 bucket.

