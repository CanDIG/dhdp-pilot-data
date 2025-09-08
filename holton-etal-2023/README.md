
Data was retreived, subsetted and transformed from https://zenodo.org/records/7625517.

Dates in the aggregated csv are made up using a fake diagnosis date of 01/01/2025 and using ages and survival days to calculate matching reference dates.

### Citations:
Mark Holton, Monica Arniella, Arvind Ravi, & Gad Getz. (2023). Genomic and Transcriptomic Analysis of Checkpoint Blockade Response in Advanced Non-Small Cell Lung Cancer (1.0.0). Zenodo. https://doi.org/10.5281/zenodo.7625517

Ravi, A., Hellmann, M.D., Arniella, M.B. et al. Genomic and transcriptomic analysis of checkpoint blockade response in advanced non-small cell lung cancer. Nat Genet 55, 807–819 (2023). https://doi.org/10.1038/s41588-023-01355-5

## Acknowledgements

Farnoosh Abbas Aghababazadeh from the [BHK lab](https://bhklab.ca/) for retreiving, subsetting and providing guidance and advice about the data.

### To convert agg csv to candig json

install requirements

```bash
pip install -r requirements.txt
```

Run CSVConvert

```bash
CSVConvert --input holton-etal-2023/agg_csv --manifest holton-etal-2023/manifest.yml
```

The output file `agg_csv_map.json` can then be ingested into CanDIG.
