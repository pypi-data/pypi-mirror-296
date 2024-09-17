# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
import gzip

from rdflib import Namespace, Graph, Literal

from probs_runner import probs_validate_data



def test_cycles1(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obj1> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj2> .
<http://w3id.org/probs-lab/data/Obj2> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj3> .
<http://w3id.org/probs-lab/data/Obj3> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj1> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )

    assert not valid



def test_cycles2(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obj1> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj2> .
<http://w3id.org/probs-lab/data/Obj2> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj3> .
<http://w3id.org/probs-lab/data/Obj3> <http://w3id.org/probs-lab/ontology#objectEquivalentTo> <http://w3id.org/probs-lab/data/Obj1> .
<http://w3id.org/probs-lab/data/Obj4> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj5> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )

    assert not valid



def test_process_or_object_defined(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#measurement> "8551330"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2018> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#measurement> "9721460"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2019> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
<http://w3id.org/probs-lab/data/unfccc/N2O_equiv> <http://w3id.org/probs-lab/ontology#objectEquivalentTo> <http://w3id.org/probs-lab/data/unfccc/N2O> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )

    assert not valid 



def test_missing_role(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#measurement> "8551330"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2018> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#measurement> "9721460"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2019> .
<http://w3id.org/probs-lab/data/Obs2> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
<http://w3id.org/probs-lab/data/unfccc/N2O_equiv> <http://w3id.org/probs-lab/ontology#objectEquivalentTo> <http://w3id.org/probs-lab/data/unfccc/N2O> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )
    
    assert not valid



def test_missing_time(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#measurement> "8551330"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )
    
    assert not valid 



def test_missing_region(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#measurement> "8551330"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2018> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )
    
    assert not valid 



def test_missing_metric(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#measurement> "8551330"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2018> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )
 
    assert not valid 



def test_no_errors(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.nt.gz"
    with gzip.open(original_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#measurement> "8551330"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#DirectObservation> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Entity> .
<http://w3id.org/probs-lab/data/Obs1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://w3id.org/probs-lab/ontology#Observation> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasMetric> <http://qudt.org/vocab/quantitykind/Mass> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasBound> <http://w3id.org/probs-lab/ontology#ExactBound> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#partOfDataset> <http://w3id.org/probs-lab/data/unfccc/UNFCCCData> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#objectDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/N2O> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#processDirectlyDefinedBy> <http://w3id.org/probs-lab/data/unfccc/1.> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRole> <http://w3id.org/probs-lab/ontology#ProcessOutput> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasTime> <http://w3id.org/probs-lab/ontology#TimePeriod_YearOf2018> .
<http://w3id.org/probs-lab/data/Obs1> <http://w3id.org/probs-lab/ontology#hasRegion> <http://w3id.org/probs-lab/ontology#RegionGBR> .
<http://w3id.org/probs-lab/data/Obj1> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj2> .
<http://w3id.org/probs-lab/data/Obj2> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj3> .
<http://w3id.org/probs-lab/data/Obj3> <http://w3id.org/probs-lab/ontology#objectComposedOf> <http://w3id.org/probs-lab/data/Obj4> .
        """
        )

    valid = probs_validate_data(
        original_filename,
        tmp_path / "working",
        script_source_dir,
    )

    assert valid
