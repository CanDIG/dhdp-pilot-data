#!/bin/bash

vcf_file=_local/1000G/ALL.chr17.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz
for sample in `bcftools query -l $vcf_file`; do
  bcftools view --threads 2 -c1 -Oz -s $sample -o ${vcf_file/.vcf*/.$sample.vcf.gz} $vcf_file
  bcftools index --tbi --threads 2 ${vcf_file/.vcf*/.$sample.vcf.gz}
done
