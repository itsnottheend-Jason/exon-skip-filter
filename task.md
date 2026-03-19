# Software engineer Technical Interview Task

## Background

Note: you do not need to understand the bioinformatical concepts
mentioned here, this is not the goal of the task.

A common pattern in a lot of our projects revolves around filtering out
elements that does not help with the task at hand. In this case, we want
to filter the [exon skip](https://en.wikipedia.org/wiki/Exon_skipping)
events when we are going through each of the [gene
splicing](https://en.wikipedia.org/wiki/RNA_splicing) events.

Processes such as these are then used in a larger orchestrated system to
produce the results we need.

## Task

This task contains two steps, filtering exon skip events and
containerize

### Filtering exon skip events

Each entry in the provided `events.txt` should be processed given the
following criteria:

1. All entries where `event_id` does not start with `exon_skip*` event
   should be filtered out
2. All entries with any `*_conf` value <10 must be filtered out
3. All entries with `psi` <0.1 or >0.9 must be filtered out

The remaining elements should then be written to a `json` file, with the
additional information: `GENE-NAME`, such as: `TASOR2`

The gene name can be obtained through this command:
```
GENE_ID=ENSG00000108021
curl -s "https://rest.ensembl.org/lookup/id/$GENE_ID?content-type=application/json" | jq -r '.display_name'
```

Feel free to make assumptions as you see fit.

### Containerize

The script above should ideally be run in an easy-to-use, encapsulated
environment, so create a container image that can be used to run the
program from the previous section.

### Delivery

As mentioned in the `Background` section, the resulting container image
will be used in a larger system so using this functionality should be
easily called as a command line tool.

The functionality implemented in this task should also easily be used as
part of a larger workflow orchestrator system, so maintainability is
paramount.
