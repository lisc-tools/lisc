---
title: 'LISC: A Python Package for Scientific Literature Collection and Analysis'
tags:
  - python
  - literature analysis
  - text mining
  - web scraping
  - meta science
  - knowledge discovery
  - hypothesis generation
  - automated meta analysis
  - literature based discovery
authors:
  - name: Thomas Donoghue
    orcid: 0000-0001-5911-0472
    affiliation: "1"
affiliations:
  - name: Department of Cognitive Science, University of California, San Diego
    index: 1
date: 16th August, 2019
bibliography: paper.bib
---

# Summary

The scientific literature is vast, and ever expanding. As a single example, the Pubmed database,
a curated database of literature from the bio-medical sciences, holds more than 30 million
published scientific articles, and is continuously growing. Given the scale of the literature,
work across informatics, information sciences, and bibliometrics has explored automated methods
for the curation of and inference from the existing literature. This work is sometimes referred
to as knowledge discovery, literature-based discovery, or hypothesis generation
[@stegmann_hypothesis_2003; @voytek_automated_2012; @spangler_automated_2014].

Here, we introduce 'Literature Scanner', or 'LISC', an open-source Python module for performing
automated meta-analyses of scientific articles by collecting and analyzing data from the
scientific literature. LISC seeks to provide an easily accessible interface that connects to
external resources that make data available through application programming interfaces (APIs).
For example, LISC connects to the Pubmed database, providing access to collect and analyze bio-medical
literature, and to the OpenCitations database [@heibi_coci_2019] providing access to citation data.
LISC is designed with an extendable approach that can be used to integrate additional APIs.
LISC also includes support and utilities for analyzing the collected literature data.

For data collection, LISC currently offers the following types of literature data collection:

- Counts: tools to collect and analyze data on the co-occurence of specified search terms
- Words: tools to collect and analyze text and meta-data from scientific articles
- Citations: tools to collect and analyze citation and reference data

To support use cases for collection and analyzing literature data, LISC includes:

- URL management and requesting for interacting with integrated APIs
- custom data objects for managing collected data
- a database structure, as well as save and load utilties for storing collected data
- functions and utilities to analyze collected data
- data visualization functions for plotting collected data and analysis outputs

LISC is organized as an object-oriented tool, and aims to be a general utility that can
be expanded to included new databases, APIs and analyses as new resources and tools are integrated.

# Statement of Need

The size and increasing scale of the scientific literature is prohibitively large for
individual scientists to be able to keep up with. Common methods for literature summarization,
including meta-analyses and systematic reviews, require time-intensive manual work, and are often
limited in scope and lag behind the literature. As a way to complement such approaches, multiple
lines of investigation have shown how automated analyses of scientific literature can be applied
to summarize and make inference from the existing literature [@stegmann_hypothesis_2003;
@voytek_automated_2012; @spangler_automated_2014].

Despite these established methods for analyzing the continuously growing literature, there is
currently a relative lack of openly available tools to collect and analyze scientific literature.
Although databases such as Pubmed have APIs, it still takes considerable work to implement and
apply even relatively simple analyses of the literature. LISC seeks to help fill this gap, by
providing user-friendly access to methods to programmatically search for and collect literature
of interest and apply analyses of interest to it.

LISC aims to serve as a complement to other relevant tools, for example Moliere,
a more sophisticated and also more computationally complex tool for hypothesis
generation [@sybrandt_moliere_2017], or Meta, a recently developed service for probing
a pre-built knowledge network inferred from the literature
(https://chanzuckerberg.com/science/programs-resources/meta/).
LISC, in contrast to these more complex systems, aims to offer a lightweight and customizable
approach for finding and collecting literature of interest, and offers tools for efficiently
performing analyses on this data. It aims to do so in particular by offering a connective
interface between available APIs and natural language processing (NLP) analyses
available through other tools. The goal is to allow for simple and rapid literature analyses.
LISC may not be appopriate for more complex analyses and hypothesis generation projects
that would be best served by tools like Moliere.

# Related Projects

LISC is inspired by and based on the BRAIN-SCANR project, a project that collected literature
data and analyzed co-occurences of terms in the neuroscientific literature [@voytek_automated_2012].

LISC, or it's precursors, has enabled a series of recent studies, including meta-analytic / descriptive
work and hypothesis driven investigations, including:

- ERPSCANR: an automated meta-analysis of the field of event-related potential (ERP) work,
in the domain of cognitive neuroscience (https://github.com/TomDonoghue/ERP_SCANR).
- Conveyed Confidence in Scientific Literature and Press Releases: an analysis of
conveyed confidence in primary scienfific literature, as compared to press releases [@fox_confidence_2018]
- Cognitive Ontology Mapping: an analysis of ontologies of cognitive and neuroscientific terms and
their use in journal articles and conference proceedings [@gao_automated_2017]

# Acknowledgements

Thank you to Jessica and Bradley Voytek for the inspiration from the BRAINSCANR project,
and to Lakshmi Menon, Will Fox and Richard Gao for helpful insights and feedback.

# References
