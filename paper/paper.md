---
title: 'LISC: A Python Package for Scientific Literature Scraping and Analysis'
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
date: XX MONTH 2019
bibliography: paper.bib
---

# Summary

The scientific literature is vast, and ever expanding. As a single example, the Pubmed database, a curated
database of literature within the bio-medical sciences, holds approximately XX published scientific articles,
with about XX new ones a year. Given the scale of the literature, work across informatics, information sciences, and
bibliometrics has explored automated methods for the curation of and inference from the existing literature. This
work is sometimes referred to as knowledge discovery, literature based discovery,
or hypothesis generation (@stegmann_hypothesis_2003; @voytek_automated_2012; @spangler_automated_2014).

Here we introduce 'Literature Scanner', or 'LISC', an open-source Python module
for performing automated meta-analyses of scientific papers, by collecting and analyzing
data from the scientific literature. LISC seeks to provide an easily accessible interface that
connects to the APIs from available databases, such as Pubmed, to collect literature data
of interest. LISC includes support and utilities for analyzing the collected literature data.

LISC currently offers two data collection & analysis approaches:
- Counts: tools to collect and analyze data on the co-occurence of specified search terms.
- Words: tools to collect and analyze text and meta-data for papers identified from a set of search terms.

To support use cases for collection and analyzing literature data, LISC includes:
- URL management and requesting for interacting witht integrated APIs
- custom objects for data management
- save and load capabilities and simple database management
- integrated analysis and plotting functionality

LISC provides these utilities in an object-oriented organization, and aims to be a general tool
that can be expanded to included new databases, APIs and analyses as new dataset and tools are
added.

# Statement of Need

The size and increasing scale of the scientific literature is prohibitively large for
individual scientists to be able to keep up with. The most common methods for literature summarization,
including meta-analyses and systematic reviews are time-demanding, lag behind the literature,
and are often limited in scope. As a possible solution to this, multiple lines of investigation have
shown how automated analyses of scientific literature can be applied to summarize and make inference from the
existing literature (@stegmann_hypothesis_2003; @voytek_automated_2012; @spangler_automated_2014).

Despite these established methods for analyzing the continuiously growing literature, there is
currently a relative lack of openly available tools to collect and analyze scientific literature.
Although databases such as Pubmed have application programming interfaces (API), it still takes considerable
work to implement and apply even relatively simple analyses of the literature. LISC seeks to help fill this gap,
by providing user-friendly access to methods to programmatically search and collect literature of interest and apply analyses of interest to it.

LISC aims to serve as a complement to other relevant tools, for example Moliere,
a more sophisticated and also more computationally complex tool for hypothesis
generation (@sybrandt_moliere_2017), or Meta, a recently developed service for probing
a pre-built knowledge network inferred from the literature (META Link / Ref / Url ?).
LISC, in contrast to these more complex systems, aims to offer a lightweight and customizable
approach for finding and collecting literature of interest, and offering tools for efficiently
applying analyses on this data. It aims to do so in particular by offering a connective
interface between available APIs and natural language processing (NLP) analyses
available through other tools. The goal is to allow for simple and rapid literature analyses,
though it may not be appopriate for more complex analyses and hypothesis generation projects
that would be best served by tools like Moliere.

# Related Projects

LISC is inspired by and based on the BRAIN-SCANR project, that collected literature data and analyzed
co-occurences of terms in the neuroscientific literature [@voytek_automated_2012].

LISC, or it's precursors, has enabled a series of recent studies, including meta-analytic / descriptive
work and hypothesis driven investigations, including:
- ERPSCANR: An automated meta-analysis of the field of event-related potential (ERP) work,
in the domain of cognitive neuroscience [REF/LINK].
- Conveyed Confidence in Scientific Literature and Press Releases: an analysis of
conveyed confidence in primary scienfific literature, as compared to press releases [@fox_confidence_2018]
- Cognitive Ontology Mapping: An analysis of ontologies of cognitive and neuroscientific terms and
their use and co-occurences in primary scientific literature and conference proceedings [@gao_automated_2017]

# Acknowledgements

Thank you to Jessica and Bradley Voytek for the inspiration for this codebase from the BRAINSCANR project,
and to Lakshmi Menon, Will Fox and Richard Gao for helpful and feedback from testing and using the codebase.

# References
