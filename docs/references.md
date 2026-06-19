# References and Inspiration

This project is inspired by the architecture and discipline of established scientific simulation toolkits, especially Geant4, while targeting a different goal: configurable universe generation across scales.

## Geant4 references

- Geant4 website: https://geant4.web.cern.ch/
- Geant4 documentation index: https://geant4.web.cern.ch/docs/
- Geant4 Book for Application Developers: https://geant4.web.cern.ch/documentation/pipelines/master/bfad_html/ForApplicationDevelopers/
- Geant4 Physics Reference Manual: https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/
- Geant4 GitHub repository: https://github.com/Geant4/geant4

## Architectural lessons adopted by QuantaEngine

- Separate run management, process selection, state representation, observation, and validation.
- Make physics modules replaceable.
- Make configuration and reproducibility first-class.
- Treat validation as part of the framework, not an afterthought.
- Avoid hard-coding physical assumptions inside numerical kernels.

## Scientific caution

QuantaEngine is not a replacement for Geant4, CLASS, CAMB, Gadget, Enzo, Athena++, lattice-QFT codes, chemistry packages, evolutionary simulators, or social simulators. Early QuantaEngine modules are toy/effective models unless explicitly validated otherwise.
