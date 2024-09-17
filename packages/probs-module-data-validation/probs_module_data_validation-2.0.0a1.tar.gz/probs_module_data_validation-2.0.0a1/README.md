# PRObs data validation module

This module contains scripts and rules for the validation of RDF data against the rules and ontology defined by PRObs.

These scripts are compatible with [RDFox](https://www.oxfordsemantic.tech) version 7.

## Running the RDFox scripts

Files defining the PRObs ontology (`probs_ontology_data.nt.gz` and `probs_ontology_rules.dlog`) should be placed in the `data` folder. The file to validate (`probs_original_data.nt.gz`) should also be located in this folder. The file `scripts/data-validation/load_data.rdfox` can be edited if the file to be validated has a different name. 

To run the validation use:

```sh
RDFox sandbox <root> scripts/data-validation/master
```

where `<root>` is the path to this folder.

A file `valid.log` will be created in the `data` folder which will indicate whether validation has passed or failed. For example if validation has failed the file will have the following content:

```
?valid
false
```

A file `test_status.csv` (space delimited) will be also be created, indicating which tests have failed. For example, if only the check for cycles has failed the file will have content:

```
?test	?status
ufu:observationsDefined	true
ufu:propertiesDefined	true
ufu:noCycles	false
```

A debug mode can be used to produce extra log files indicating potential problems with the data:

`test_cycles.log` will list objects having a cyclic definition (i.e. they are defined in terms of themselves).

`test_missing_properties_for_observation.log` will list objects of type `:Observation` which have missing properties (region, role, time period or metric).

`test_object_or_process_not_defined_for_observation.log` will list objects of type `:Observation` which do not have `:objectDefinedBy` or `:processDefinedBy` properties. 

The debugging mode can be selected by using ```debug on``` or ```debug off``` parameters. If these parameters are omitted then the default mode is for debugging to be turned off.
For example, to run the validation scripts in debug mode use:

```sh
RDFox sandbox <root> "scripts/data-validation/master debug on"
```

## Using probs-runner

Using [probs-runner](https://github.com/probs-lab/probs-runner), this module can be run using the `probs_validate_data` function.
