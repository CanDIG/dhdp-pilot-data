#!/bin/bash

while read file;
do
  aws s3 cp _local/1000G/$file s3://dhdp-site-a/ --profile dhdp-site-a;
done < genomic_data/SiteA_files.txt

while read file;
do
  aws s3 cp _local/1000G/$file s3://dhdp-site-b/ --profile dhdp-site-b;
done < genomic_data/SiteB_files.txt

while read file;
do
  aws s3 cp _local/1000G/$file s3://dhdp-site-c/ --profile dhdp-site-c;
done < genomic_data/SiteC_files.txt
