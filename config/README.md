# Configuration file

Configuration file should be found under the `config` folder and called `config.yaml` like the provided example. 

`configfile: "config/config.yaml"`

If desired, you can name it differently, but make sure to include the option `--configfile config/NEW_NAME.yaml` when running snakemake

Other than that, the configuration file requires only two information:

 ```
sample_info:
  "config/species_table_shorter_augustus.tsv"
project_name:
  "developing_workflow"
```
The name of the species table (`sample_info`) can be modified, just make sure the name of the actual file also matches what is listed in the configuration file. Make sure to still store in the folder `config` to keep things organized.

Choose the name of your project (`project_name)`, which is how the output subfolder in `results` will be named. 

**Note**: It is really important you have a folder in `resources` that is named the same way, which is where you will store any input file, like genome (always mandatory), transcriptome, forward and reverse files. Inside of `resources/[project_name]` is also where the data downloaded from the SRA database will be stored in the subfolder `resources/[project_name]/SRA/`

# Species information table

Modify `species_table_shorter_augustus.tsv` based on your project. If you rename the file, make sure to change the name under `sample_info:` in the configuration file.

NEVER change the names of the columns and leave no cell empty, write `None` when needed and `Yes|No` (more info below).

|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
HW06_Cratena_peregrina|Pomacea_canaliculata_GCF_003073045.1_genome.fna|None|SRR8573936_1.fastq.gz|SRR8573936_2.fastq.gz|None|mollusca_odb10|resources/Dario_custom_adapters.fa|Yes|Yes|No|None|HW06_Cratena_peregrina|
Pediculus_humanus_corporis_Genome-Guided|Pediculus_humanus_corporis_GCF_000006295.1_genome.fna|None|None|None|SRR13528755|hemiptera_odb10|TruSeq3-PE.fa|No|Yes|Yes|Pediculus_humanus|Pediculus_humanus|
Pediculus_humanus_corporis|Pediculus_humanus_corporis_GCF_000006295.1_genome.fna|Pediculus_humanus_corporis_GCF_000006295.1_transcriptome.fna|None|None|None|hemiptera_odb10|None|No|Yes|No|None|Pediculus_humanus|
Drosophila_melanogaster|Drosophila_melanogaster_GCF_000001215.4_genome.fna|Drosophila_melanogaster_GCF_000001215.4_transcriptome.fna|None|None|None|diptera_odb10|None|Yes|Yes|No|None|Drosophila_melanogaster|
Drosophila_melanogaster_no_transcriptome|Drosophila_melanogaster_GCF_000001215.4_genome.fna|None|None|None|None|None|None|No|No|Yes|fly|None|

## Mandatory parameters
- Species_name: name of your species and how output files will be labeled. This needs to be unique if you want to process the same genome and/or transcriptome file differently.
  - Example1: Pediculus_humanus_corporis_Genome-Guided X Pediculus_humanus_corporis: same genome file, but for Pediculus_humanus_corporis_Genome-Guided the transcriptome is assembled. Additionally, augustus analyses are different.
  - Example2: Drosophila_melanogaster X Drosophila_melanogaster_no_transcriptome: no transcriptome is assembled or provided for the latter, so just gene predictions ab initio can be done with Augustus.
- Genome: name of fasta file stored in folder `resources/[project_name]`. The suffix is "irrelevant", i.e. it can be .fna, .fas, .fasta, etc.

## Mandatory parameters for all but one case (where no transcriptome is assembled or provided)

- BUSCO_lineage: name of BUSCO lineage. More on available lineages [here](https://busco-data.ezlab.org/v5/data/lineages/)

## Required parameters on a case-by-case 

1. Provide both genome and transcriptome files
- Provide information on Species_name, Genome, Transcriptome, and BUSCO_lineage. Mark `None` for Forward, Reverse, SRA, and Adapter.

2. Provide a genome file and paired-end RNA-Seq files
- Provide the Species_name and Genome information, and write `None` under Transcriptome
- Provide names of Forward and Reverse files
- Write `None` under SRA
- Provide the BUSCO_lineage for you species. e.g. mollusca_odb10 if you are working with a mollusc. More on available lineages [here](https://busco-data.ezlab.org/v5/data/lineages/)
- Provide the name of your adapter file for trimming, which is done with Trimmomatic. You can give a path to a custom file, like the example found in `resources/Dario_custom_adapters.fa` or the name of a standard adapter file deployed with Trimmomatic, like `TruSeq3-PE.fa`. More info [here](http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf)

3. Provide a genome file and a [SRA accession ID](https://www.ncbi.nlm.nih.gov/sra) corresponding to paired-end RNA-Seq files
- Provide the Species_name and Genome information, and write `None` under Transcriptome, Forward, and Reverse
- Write the accession id corresponding to paired-end reads file from the SRA database
- Provide the BUSCO_lineage for you species. e.g. mollusca_odb10 if you are working with a mollusc. More on available lineages [here](https://busco-data.ezlab.org/v5/data/lineages/)
- Provide the name of your adapter file for trimming, which is done with Trimmomatic. You can give a path to a costum file, like the example found in `resources/Dario_custom_adapters.fa` or the name of a standard adapter file deployed with Trimmomaticm, like `TruSeq3-PE.fa`. More info [here](http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf)

4. Provide just the genome file
- Provide the Species_name and Genome information, and write `None` under Transcriptome, Forward, Reverse, SRA, Adapter, and BUSCO_lineage.

## Augustus processing alternatives

Generally speaking, protein-coding genes and their exon-intron structures can be found in genomic sequences using the program Augustus. There are different approaches when doing so. Whether you want to train Augustus, run it with extrinsic hints or *ab initio*, you need to write `Yes` or `No` under the columns `Augustus_training`, `Augustus_hints`, `Augustus_ab_initio`, respectively. Additionally, if you don't want to run Augustus *ab initon* or with hints, write `None` under `Augustus_ab_initio_species` or `Augustus_ab_initio_species`, repectively. For which species name to write under the two columns, see sections below.

### Ab initio

No other input file other than a genome file is required and the gene prediction is done *ab initio* with training annotation files already provided by the program. As such, the user needs to provide the name of the species according to the name of the subdirectory within [config from Augustus](https://github.com/Gaius-Augustus/Augustus/tree/master/config/species).

For example, if you want to annotate a genome file from *Drosophila melanogaster*, the name provided in the column `Augustus_ab_initio_species` should be `fly`. If you would write down something like `Drosophila_melanogaster` instead it would return an error as there are not folders named like that. So, pay attention! Additionally, you need to write `Yes` under the column `Augustus_ab_initio`.

As aforementioned, the user only needs to provide a genome file, signal with "Yes" that they want to run ab initio predictions and the name of the species to be used.
However, it is entirely possible for the user to run augustus ab initio **as well** as the training and/or predictions with hints. For example, a row from the table might look like this:

|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Octopus_bimaculoides|Octopus_bimaculoides_genome.fas|Octopus_bimaculoides_transcriptome.fas|None|None|None|mollusca_odb10|None|Yes|Yes|Yes|Argopecten_irradians|Octopus_bimaculoides|

What this will do: 

- Train the new species and generate predictions for *Octopus bimaculoides*
- Generate gene predictions using extrinsic hints from the transcriptome file with parameters trained for *Octopus bimaculoides*
- Run gene predictions *ab initio* using pre-trained parameter sets
from another mollusk, *Argopecten irradians*

Running *ab initio* prediction with a pre-trained species like *Argopecten irradians* would allow for the user to compare the predictions between the newly trained set and the existing set. For more on training, see section below. Do keep in mind that in this example *Argopecten irradians* and *Octopus bimaculoides* are mollusks from two different classes, so predictions might not be ideal. 

**Scenario 1**: If, for example, you have two different genome files for two specimens of *Octopus bimaculoides*, and just one of them with transcriptomic data, you could use the species with transcriptomic data to train Augustus, as *Octopus bimaculoides* does not yet have trained parameters, and then use these parameters to predict genes ab initio for the other specimen who has only a genome file.

|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Octopus_bimaculoides|Octopus_bimaculoides_genome.fna|Octopus_bimaculoides_transcriptome.fna|None|None|None|mollusca_odb10|None|Yes|No|No|None|None|
Octopus_bimaculoides_alternative|Octopus_bimaculoides_alternative_genome.fna|None|None|None|None|None|None|No|No|Yes|Octopus_bimaculoides|None|


Remember to name both specimens uniquely and that under the column `Augustus_ab_initio_species` for the species `Octopus_bimaculoides_alternative` you should write the name of the species used for training. In this example, it would be `Octopus_bimaculoides`.

The workflow will first finish training `Octopus_bimaculoides` and then run the *ab initio* prediction for the species `Octopus_bimaculoides_alternative` using the parameters within `$AUGUSTUS_CONFIG_PATH/species/Octopus_bimaculoides_train/`.

**Scenario 2:** You have transcriptomic and genomic data for the two *Octopus bimaculoides* specimens, but the sequencing quality is higher for `Octopus_bimaculoides_one`. You train that specimen first. Then, you use the transcritome from `Octopus_bimaculoides_two` to generate extrinsic hints and use the trained parameters from `Octopus_bimaculoides_one`.

|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Octopus_bimaculoides_one|Octopus_bimaculoides_one_genome.fna|Octopus_bimaculoides_one_transcriptome.fna|None|None|None|mollusca_odb10|None|Yes|No|No|None|None|
Octopus_bimaculoides_two|Octopus_bimaculoides_two_genome.fna|Octopus_bimaculoides_two_transcriptome.fna|None|None|None|mollusca_odb10|None|No|Yes|No|None|Octopus_bimaculoides_one|

### Extrinsic hints

Transcriptome is used to generate "hints" by providing evidence about the location of introns and exons. To do so, user has to provide genome and transcriptome files, BUSCO_lineage to quality check transcriptome file, mark `Yes` under `Augustus_hints` and the name of the species under `Augustus_hints_species`. 

If you want to use pre-trained parameters from Augustus (standard and recommended, when applicable), check the available species [here](https://github.com/Gaius-Augustus/Augustus/tree/master/config/species) and provide the name of the subdirectory in the cell corresponding to `Augustus_hints_species`.

If you want to train a new species and use the trained paremeters to predict genes with extrinsic hints for another one, provide the name of that first species under `Augustus_hints_species` for the second one.

|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Octopus_bimaculoides_one|Octopus_bimaculoides_one_genome.fna|Octopus_bimaculoides_one_transcriptome.fna|None|None|None|mollusca_odb10|None|Yes|No|No|None|None|
Octopus_bimaculoides_two|Octopus_bimaculoides_two_genome.fna|Octopus_bimaculoides_two_transcriptome.fna|None|None|None|mollusca_odb10|None|No|Yes|No|None|Octopus_bimaculoides_one|

### Train new species

First and foremost, it is important to know that training Augustus is meant to be a "supervised" process, as it needs RELIABLE information on gene structures, as well as the flanking, non-coding regions. However, it is possible to automate this process to some extant, but not without caveats. There are some checking steps built into the rules to warn the user with messages in the log files, as well as stopping the pipeline if something is not as it should be.

If the quality of the transcriptome is low and/or the genome used for mapping is from a species too distantly related from the subject species, [PASApipeline](https://github.com/PASApipeline/PASApipeline/wiki/PASA_RNAseq) **WILL FAIL**. PASA is used by AugusMake to generate the training gene structures, also called bona fide reference gene structures or training set, to train Augustus. If there isn't enough information, what usually happens is that `TransDecoder.Predict`, built into the PASApipeline to identify ORFs with homology to known proteins. This is first flagged as an error by TransDecoder.predict although the first program from TransDecoder pipeline, `TransDecoder.LongOrfs`, likely only found a small number of ORFs. If that is the case, within the log file `results/{project}/{species}/logs/pasa_{species}.log` the user will see the following message:

```
ERROR in PASApipeline; {species} probably doesn't have enough information to run TransDecoder; 

One quick way to check the quality of the transcriptome is to see how many complete, single-copy orthologs were found for {species}: results/{project}/{species}/busco_figure_{species}.png;

If there are MANY missing orthologs, it could be that the transcriptome assembly is not good and/or the genome from a species too distant to the target species was used for mapping;

TRAINING {species} IS NOT POSSIBLE AT THE MOMENT
```

**If that is the case, it is NOT possible to continue training this species.** If so, the user should remove the species from the input table as a training species and re-run the workflow. As an alternative, one could run predictions with extrinsic hints and/or **ab initio** using one of the available species [here](https://github.com/Gaius-Augustus/Augustus/tree/master/config/species), while still keeping in mind the results might not be ideal if the genome file is from a distant relative from the target species. 

If the PASApipeline finished adequately, there is a high change that no other errors will be thrown up until the actual Augustus training step. During said step, if there are less than 200 gene structures, which is the absolute minimum for acceptable performance, the analysis will also fail. Like before, a message will be given flagging this in `results/{project}/{species}/logs/augustus_training_{species}.log`:

```
ERROR: There are fewer than 200 gene structures in results/{project}/{species}/augustus_training_{species}/main_results/{species}_noerror_genes_refiltered_bonafide.gbff;
TRAINING {species} IS NOT POSSIBLE AT THE MOMENT
```

Or, if there are exactly 200 genes and nothing left to be used for training, this will be seen:

```
ERROR: there are exactly 200 genes in test set: results/{project}/{species}/augustus_training_{species}/main_results/{species}_noerror_genes_refiltered_bonafide.gbff.test;
training set empty: results/{project}/{species}/augustus_training_{species}/main_results/{species}_noerror_genes_refiltered_bonafide.gbff.train;
TRAINING {species} IS NOT POSSIBLE AT THE MOMENT
```

If training is finished successfully and the user has other species listed in the input table for which predictions **ab initio** and/or with hints will be done using the trained parameters, the predictions will continue as expected.

However, as aforemetioned, training augustus is meant to be a supervised process. It could very well be that `Species_one` was trained seemingly successfuly and subsequent steps for `Species_two` are done as expected using the new parameters. However, it could be that upon closer inspection of the report accuracy values listed at the end of `results/{project}/{species}/augustus_training_{species}/main_results/{species}_augustus_training.out` for `Species_one`, the user finds out training results were not as good. If so, **meta parameters optimization** would need to be done manually by the user and augustus run again. This is because there is yet no automated check built into the workflow to modify this. 

All in all, results for training augustus should be inspected closely and used carefully.

With all of that being said, to train augustus, the user needs to provide genome and transcriptome files (or paired-end reads - local or to be downloaded from the SRA database) and to flag this under `Augustus_training` with `Yes`.


|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Octopus_bimaculoides|Octopus_bimaculoides_genome.fna|Octopus_bimaculoides_transcriptome.fna|None|None|None|mollusca_odb10|None|Yes|No|No|None|None|

Remember: you CAN NOT use a name under the column "Species_name" that would crash with a species subdirectory from [here](https://github.com/Gaius-Augustus/Augustus/tree/master/config/species). So, if you want to train a new *Drosophila melanogaster* sample, do not name it `fly`, name it `Drosophila_melanogaster`. Then, let's say you want to use the newly trained parameters to predict genes for another specimen of `D. melanogaster`, fill the information in the cells like this:


|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Drosophila_melanogaster_spp1|Drosophila_melanogaster_spp1_genome.fna|Drosophila_melanogaster_spp1_transcriptome.fna|None|None|None|mollusca_odb10|None|Yes|No|No|None|None|
Drosophila_melanogaster_spp2|Drosophila_melanogaster_spp2_genome.fna|Drosophila_melanogaster_spp2_transcriptome.fna|None|None|None|mollusca_odb10|None|No|Yes|No|None|Drosophila_melanogaster_spp1|

You could also mark `Yes` under `Augustus_ab_initio` and use just the genome from spp2 to run **ab initio** predictions using parameters already provided by Augustus for `fly`. With these settings, one can compare the results from training against the results from existing paremeters. 

|Species_name|Genome|Transcriptome|Forward|Reverse|SRA|BUSCO_lineage|Adapter|Augustus_training|Augustus_hints|Augustus_ab_initio|Augustus_ab_initio_species|Augustus_hints_species|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
Drosophila_melanogaster_spp2|Drosophila_melanogaster_spp2_genome.fna|Drosophila_melanogaster_spp2_transcriptome.fna|None|None|None|mollusca_odb10|None|No|Yes|Yes|fly|Drosophila_melanogaster_spp1|
