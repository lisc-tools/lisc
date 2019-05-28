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
  - name: Department of Cognitive Science, UC San Diego
    index: 1
date: 26 May 2019
bibliography: paper.bib
---

# Summary

The scientific literature is vast, and ever expanding. The Pubmed database, for example,
holds approximately XX published scientific articles, with about XX new ones a year.
Given the scale of the literature, work across informatics, information sciences, and
bibliometrics, has explored methods for automated methods for curation of and inference
from the existing literature, work sometimes called knowledge discovery, literature based discovery,
or hypothesis generation (@stegmann_hypothesis_2003; @voytek_automated_2012; @spangler_automated_2014).

Despite the continuing growth of the literature, there is a lack of openly available tools
for custom analysis of the literature, that allows users to programmatically search
areas of the literature of interest, and apply methods and ideas from this prior work in
information sciences. To address this, we introduce 'Literature Scanner', or 'LISC', an open-source
Python module for performing automated meta-analyses of scientific papers, by collecting and
analyzing data from the scientific literature.

LISC serves as a wrapper and connector for available database application programming
interfaces (API) to collect literature data, as well as implementing analyses that can
performed on the collected data. It's current core integration is to serve as a wrapper
of the Pubmed E-Utilities API, that provides programmatic access to the Pubmed database,
a database of scientific literature in the biomedical sciences.

LISC currently offers two data collection & analysis approaches:
- Counts: collects data on the co-occurence of specified search terms.
- Words: collects text and meta-data for papers identified from a set of search terms.

As well as the functionality to collect data, LISC includes support for analyzing
collected literature data. LISC also includes custom objects for data management,
save and load utilties, and plotting functions. LISC provides an object-oriented API
for collecting and analyzing data, though all the underlying functions are also publicly
callable, allowing for non-object-oriented use of the module.

# Statement of Need

The size and increasing scale of the scientific literature is prohibitively large for
individual scientists to be able to read all of their literature in their area, nor to
explore ideas from other areas. Existing mechanisms of literature summarization,
including meta-analyses and systematic reviews are time-demanding, lag behind the literature,
and are often limited in scope.

Though there is a body of work demonstrating how automated analyses of scientific
literature can a productive strategy for summarizing and making inferences from the
existing literature, there is, to the authors knowledge, a relative lack of openly
available tools allowing casual users to explore such analyses. LISC seeks to fill this
gap, but providing user-friendly access to available database APIs with out of the both
methods for analyzing collected data.

LISC aims to serve as a complement to other relevant tools, for example Moliere,
a much more sophisticated but also more computationally complex tool for hypothesis
generation (@sybrandt_moliere_2017), or Meta, a recently developed service for probing
a pre-built knowledge network inferred from the literature (META Link / Ref / Url ?).
It aims to do so by offering a lightweight tool that prioritizes making simple analyses
and literature summarization techniques more easily available to users, in a way that
allows users flexibility to specify areas of interest and efficiently run simple analyses
on the literature, though it may not be appopriate for more complex analyses and
hypothesis generation projects that would be best served by tools like Moliere.

# Related Projects

The current module is based on project that analyzed co-occurence mapping
of the neuroscientific literature [@voytek_automated_2012].

LISC, or it's precursors, has has allowed for a series of recent studies,
including both meta-analytic and descriptive work and hypothesis driven investigations,
including:
- ERPSCANR: An automated meta-analysis of the field of event-related potential (ERP) work,
in the domain of cognitive neuroscience [REF/LINK].
- Conveyed Confidence in Scientific Literature and Press Releases: an analysis of
conveyed confidence in primary scienfific literature, as compared to press releases [@fox_confidence_2018]
- Cognitive Ontology Mapping: An analysis of ontologies of cognitive and neuroscientific terms and
their use and co-occurences in primary scientific literature and conference proceedings [@gao_automated_2017]

# Acknowledgements

Thank you to Will Fox and Richard Gao for helpful comments and feedback
while testing and using the codebase.

# References
