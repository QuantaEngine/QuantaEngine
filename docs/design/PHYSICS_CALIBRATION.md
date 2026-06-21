# Physics calibration and uncertainty contract

This document makes the toy/analytic calibration surface explicit. The ranges below are
**model-uncertainty envelopes**, not experimental confidence intervals. A “physical anchor” is
measured or derived; a “literature-informed window” is a broad feasibility region; a “heuristic”
is an arena scoring choice. The code must not present the latter two as measured probabilities.

## Standard-universe anchors

| Quantity | Accepted interval | Standard result | Basis |
|---|---:|---:|---|
| Hydrogen binding energy | 13.5–13.7 eV | ≈13.60 eV | NIST Atomic Spectra Database ionization energy; reduced-mass Bohr-model check |
| Bohr radius | 5.2–5.4 × 10⁻¹¹ m | ≈5.29 × 10⁻¹¹ m | CODATA/NIST Bohr radius; reduced-mass tolerance |
| Universe age | 13.0–14.5 Gyr | ≈13.8 Gyr | Planck 2018 ΛCDM parameters, arXiv:1807.06209 |
| Analytic compiler score | 0.98–1.00 | ≈0.9997 | Regression anchor, heuristic score |
| Variational relaxer score | 0.82–0.90 | ≈0.8614 | Regression anchor, heuristic score |
| Minimal-axiom score | 0.88–0.96 | ≈0.9233 | Regression anchor, heuristic score |

## Calibrated thresholds

The identifiers below are the public `CalibrationThreshold.basis` values exposed by each engine.
Every logistic/falling window has a nominal value and an envelope. Sensitivity is computed by
`engine.threshold_sensitivity(vector)`, which changes one threshold at a time to both envelope
ends and records the score delta.

| Basis | Nominal | Envelope | Classification and rationale |
|---|---:|---:|---|
| `analytic.stellar_min_lifetime_years` | 1 Gyr | 0.5–2 Gyr | Heuristic time available for complex chemistry; not a biological probability |
| `variational.atomic_binding` (low/high) | 1 / 120 eV | 0.5–2 / 80–160 eV | Broad chemical-binding feasibility around the 13.6 eV anchor |
| `variational.relativistic_alpha` | 0.5 | 0.3–0.8 | Non-relativistic model-validity taper; α≈1 is supercritical for this model |
| `variational.nuclear_strong` (low/high) | 0.8 / 1.45 | 0.7–0.9 / 1.25–1.65 | Toy strong-scale calibration; must not be read as a QCD error band |
| `variational.ignition` | log₁₀ g=-1.4 | -2.0–-0.8 | Heuristic ignition transition informed by alternative-constant stellar models |
| `variational.lifetime` (low/high) | 1 Gyr / 10 Tyrs | 0.5–2 Gyr / 5–20 Tyrs | Lower bound heuristic; upper bound prevents unbounded “longer is always better” scoring |
| `variational.structure` (low/high) | Q=10⁻⁶ / 3×10⁻⁴ | 3×10⁻⁷–3×10⁻⁶ / 10⁻⁴–10⁻³ | Literature-informed broad structure window; Tegmark & Rees, arXiv:astro-ph/9709058 |
| `variational.age` (low/high) | 2 / 50 Gyr | 1–4 / 30–80 Gyr | Heuristic usable-time window around the 13.8 Gyr anchor |
| `minimal.alpha` (low/high) | 10⁻³ / 0.1 | 3×10⁻⁴–3×10⁻³ / 0.05–0.3 | Literature-informed/order-of-magnitude atomic and stellar feasibility |
| `minimal.stellar_number` (low/high) | 10⁴⁸ / 10⁶³ | 10⁴⁶–10⁵⁰ / 10⁶¹–10⁶⁵ | Dimensionless order-of-magnitude proxy, not a measured observable |
| `minimal.hierarchy` | 10⁻⁸ | 3×10⁻⁹–3×10⁻⁸ | Carr–Rees-style hierarchy proxy; Nature 278, 605–612 (1979), DOI 10.1038/278605a0 |
| `minimal.lambda` | scale 12 | 6–24 | Heuristic suppression scale, explicitly not the observed Λ uncertainty |
| `minimal.seeds` (low/high) | Q=10⁻⁶ / 3×10⁻⁴ | 3×10⁻⁷–3×10⁻⁶ / 10⁻⁴–10⁻³ | Same perturbation-amplitude calibration as the variational scheme |

## References and interpretation limits

- Planck Collaboration, “Planck 2018 results. VI. Cosmological parameters,”
  https://arxiv.org/abs/1807.06209.
- M. Tegmark and M. Rees, “Why is the CMB fluctuation level 10⁻⁵?”,
  https://arxiv.org/abs/astro-ph/9709058.
- F. C. Adams, “Stars In Other Universes,” https://arxiv.org/abs/0807.3697.
- B. J. Carr and M. J. Rees, “The anthropic principle and the structure of the physical world,”
  https://doi.org/10.1038/278605a0.
- NIST Atomic Spectra Database and CODATA constants, https://physics.nist.gov/asd and
  https://physics.nist.gov/cuu/Constants/.

The cited work motivates scale and ordering, not the exact logistic shape or arena weights. A
future high-fidelity solver must replace these envelopes with likelihoods or emulator-based
uncertainty propagation before scientific inference is claimed.
