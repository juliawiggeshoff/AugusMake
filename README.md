# AugusMake - Augustus-based gene prediction with Snakemake

Guided by a genome file, a transcriptome is *de novo* assembled with Trinity. It does so using RNA-Seq data provided by the user or automatically downloads paired-end (PE) reads following an accession number from NCBI'S SRA database. Trimming of PE reads is done with Trimmomatic and their quality is assed pre- and post-trimming with FastQC. Alternatively, the user can also provide an already-assembled transcriptome. The completeness of the transcriptome is checked using BUSCO. Gene predictions can be done *ab initio* using just a genome file, i.e. no transcriptome is required, and/or with extrinsic hints using transcriptomic data. Both can be done with pre-trained parameters from Augustus or the user can choose to train the program for a new species. The results from training should be used with caution and carefully checked by the user after the analyzes are completed.

The rules for Augustus were developed after the protocol from [Hoff & Stanke (2018)](https://www.researchgate.net/publication/329132272_Predicting_Genes_in_Single_Genomes_with_AUGUSTUS), the developers from Augustus. 

# System requirements
## Local machine

I recommend running the workflow on a HPC system, as the analyses are resource and time consuming.

- If you don't have it yet, it is necessary to have conda or miniconda in your machine.
Follow [there](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html) instructions.
	- After you are all set with conda, I highly (**highly!**) recommend installing a much much faster package manager to replace conda, [mamba](https://github.com/mamba-org/mamba)
		- First activate your conda base:

		`conda activate base`
		- Then, type:
		
		`conda install -n base -c conda-forge mamba` 

- Likewise, follow [this](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) tutorial to install Git if you don't have it.

## HPC system

Follow the instructions from your cluster administrator regarding loading of  modules, such as loading a root distribution from Conda.
For example, modules might be used to set up environmental variables, which have to first be loaded within the jobscripts. 

e.g.:
`module load anaconda3/2022.05`

Normally, the user doesn't have have sudo rights to install anything to the root of the cluster. For example, you might want to work with a more updated distribution of conda as your "new", local base, and (ideally) install and use mamba to replace conda as a package manager. To do son, one needs to first load the anaconda module and then create a new environment, here called `localconda` 
1. `module load anaconda3/2022.05`
2. `conda create -n localconda -c conda-forge conda=22.9.0`
3. `conda install -n localconda -c conda-forge mamba`
4. `conda activate localconda`

If you run `conda env list` you'll probably see something like this:
`/home/myusername/.conda/envs/localconda/`

# Installation 

1. Clone this repository

`git clone https://github.com/juliawiggeshoff/AugusMake.git`

2. Activate your conda base

`conda activate base`

- If you are working on a cluster or have your own "local", isolated environment you want to activate instead, use its name to activate it

`conda activate localconda`

3. Install **AugusMake** into an isolated software environment by navigating to the directory where this repo is and run:

`conda env create --file environment.yaml`

If you followed what was recommended in the [System requirements](https://github.com/juliawiggeshoff/AugusMake#local-machine), run this intead:

`mamba env create --file environment.yaml`

The environment from **AugusMake** is created

4. **Always** activate the environment before running the workflow

On a local machine:

`conda activate AugusMake`

If you are on a cluster and/or created the environment "within" another environment, you want to run this first:

`conda env list`

You will probably see something like this among your enviornments:

`home/myusername/.conda/envs/localconda/envs/AugusMake`

From no own, you have to give this full path when activating the environment prior to running the workflow

`conda activate /home/myusername/.conda/envs/localconda/envs/AugusMake`

# Input data requirements

1. Configuration file `config/config.yaml`
2. Species Information table `config/species_table.tsv"

Detailed information on the required input files, including all three augustus processing alternatives found in [`config/README.md`](https://github.com/juliawiggeshoff/AugusMake/tree/main/config#readme)

# Run AugusMake

Remember to always activate the environment first

`conda activate AugusMake`

or

`conda activate /home/myusername/.conda/envs/localconda/envs/AugusMake`

Before running the workflow locally or in a HPC system, make sure to do a "dry run" (`--dry-run` or `-n`) to see how many jobs will be run and if any errors are being flagged. Use `--printshellcmds` or `-p`` for a full description of the rules or `--quiet` or `-q` to just print a summary of the jobs:

`snakemake --use-conda --cores 51 -q -n`

```
Building DAG of jobs...

Job stats:
job                      count    min threads    max threads
---------------------  -------  -------------  -------------
aa2nonred                    2             20             20
all                          1              1              1
all_busco_flag               1              1              1
all_fasterq_dump_done        1              1              1
augustus_ab_initio           1              1              1
augustus_hints               4              1              1
augustus_training            2              1              1
blat2hints                   4              1              1
blat_pslCDnaFilter           4              1              1
bonafide_gtf                 2              1              1
busco                        4             10             10
busco_report_all             1              1              1
busco_report_single          4              1              1
computeflankingregion        2              1              1
cp_busco_flag                4              1              1
download_busco               3              1              1
fasterq_dump                 1              6              6
filtergenesin                2              1              1
flag_fasterq_dump            1              1              1
genome_guided_trinity        2             20             20
gff2gbsmalldna               2              1              1
gmap_build                   2              1              1
gsnap                        2             20             20
pasa                         2             20             20
prefetch                     1              1              1
raw_fastqc                   2              2              2
samtools                     2              5              5
trimmed_fastqc               8              2              2
trimmomatic                  2             15             15
total                       69              1             20
```

You can use the information from the **total*** numbers of jobs to "guide" the value for `--jobs`, while keeping in mind not to "allow" too many jobs at one. So, a value of 25 to 30 jobs might be the safest choice. See [cluster execution](https://github.com/juliawiggeshoff/AugusMake#cluster-execution).

## Local machine execution

**Not recommended** if you don't have a lot of storage and CPUs available (and time to wait...). Nevertheless, you can simply run like this:

`nohup snakemake --keep-going --use-conda --verbose --printshellcmds --reason --nolock --cores 31 --max-threads 25 --rerun-incomplete > nohup_AugusMake_$(date +"%F_%H_%M_%S").out &`

Modify number of cores accordingly.

## Cluster execution

Tailored to work with a SGE job scheduler. Modify as needed. See [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/executing/cluster.html) for help.

Before the first execution of workflow, you need to create the environments, otherwise Snakemake fails:

`snakemake --cores 8 --use-conda --conda-create-envs-only`

To run the workflow:

`nohup snakemake --keep-going --use-conda --verbose --printshellcmds --reason --nolock --jobs 15 --cores 51 --local-cores 15 --max-threads 25 --rerun-incomplete --cluster "qsub -terse -V -b y -j y -o snakejob_logs/ -cwd -pe smp {threads} -q small.q,medium.q,large.q -M user.email@gmail.com -m be" > nohup_AugusMake_$(date +"%F_%H_%M_%S").out &`

Remember to:
1. Create snakejob_logs in the working directory
2. Modify user.email@gmail.com
3. Change values for --jobs, --cores, --local-cores, and --max-threads accordingly 

Make sure you set a low value for `--local-cores` to not take up too much resources from your host node. Likewise, it is not recommended to let a lot of `--jobs` to run in parallel, for similar reasons. Lastly, I personally like to set a `--max-threads` limit to ensure no rule "hogs" too many threads. This is often necessary because the number of thread use per rule are set as a percentage of the total of resources provided by the user. e.g.: If you can and want to use 110 threads, a rule like genome_guided_trinity will "take" 40% of these, 44 threads, and that is often an overkill. So, by limiting the maximum number of threads to 25, other jobs can run simultaneously, while making sure trinity still has a "decent" number of threads to use. 

If you named your configuration file differently, e.g. NEW_NAME, include the option `--configfile config/NEW_NAME.yaml`

# Main results

## report.zip

A report.zip file is automatically generated upon the sucessfully finished workflow. ALWAYS include `--no-lock` when running snakemake, otherwise it is not automatically created and it returns an error. If that happens, the user can just manually generate the report with `snakemake --report report.zip` afterwards, but the automatic generation is obviously prefered.

Charts to visually represent the BUSCO results are output in the report.zip. Each species has their own, individual chart. One chart combining all species is also available. This is done to compare the results between the assemblies. Similarly, the FastQC report files are also included for each species pre and post-trimming.

**To be included: Augustus results**
