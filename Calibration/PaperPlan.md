# Paper plan: Propp's analyses against blind transcription

**A working plan, begun 2026-10-05 at the owner's instruction. It fixes what the paper will report and where each figure comes from; the prose is written once the improvement test and the human benchmark are in.**

## Working title

Measuring the measurer: blind machine transcription against Propp's own analyses of the 45 tales of his Appendix III.

## The claim, as it stands

Language models, reading the Russian tales without access to Propp's schemes, find most of the functions he found (74% to 77%; 80% to 84% counted once per tale), far beyond chance, and agree with him less than with each other, chiefly because they record repetitions he folds into one, and because his schemes write functions the text leaves implicit. Propp's schemes are themselves a compressed and partly inferred record, so agreement with them has a ceiling below one that no transcriber, human or machine, can be expected to pass.

## Sections

1. **Introduction.** Propp's schemes have served as an answer key for nearly a century of applications and, lately, for computational work; how reproducible they are has been tested only on a handful of tales.
2. **Prior work.** Bod, Fisseni, Kurji and Löwe (2012) and Fisseni et al. (2014); Finlayson (2015/2017, 2016); Gervás and Méndez (2024). See `PreliminaryFindings.md`, section 9. Their tales overlap ours (93, 104, 127, 131, 133, 139, 145, 151, 155), which allows a tale-by-tale comparison.
3. **Material.** The 45 tales, Russian Wikisource (1984-85 edition), extraction; Propp's schemes as `embedCorpus.derive()` reads them.
4. **Method.** Event listing, then blind transcription by two models under fixed rules and card, two arms; the memory probe; the frozen protocol; measures and the derangement baseline.
5. **Results.** The calibration (`CompareRun.txt`); chance-corrected figures; recall and precision; symbol by symbol over- and under-marking.
6. **Where the disagreements come from.** Repetition (trebling), implicit functions (C), move division, order and the braces. Each a measured diagnostic, with examples from tales.
7. **Can the instrument be brought closer?** The improvement test (`ImproveProtocol.md`), development and held-out results, whatever they are.
8. **The human benchmark.** The owner's transcription of a few tales from the English event lists, against Propp and against the models.
9. **Discussion.** What a reproducibility ceiling means for Propp's schemes as an answer key, and for this project's genre tests (acceptance and coverage withdrawn as genre evidence).
10. **Data and code.** The repositories, the commits, the frozen files.

## Still to obtain

- The improvement test, on the test tales.
- The human benchmark: the owner's choice of tales and time.
- A tale-by-tale comparison with the published figures of the prior studies, where their tales overlap ours.
- Every prior-work citation checked against the source before it is quoted.

## Open for the owner

- **Positioning.** The calibration is the largest blind test against Propp's own analyses found so far, but not the first comparison with them. The paper should say so.
- **Venue.** Digital humanities (*Digital Scholarship in the Humanities*, where Finlayson published), folklore (*Journal of American Folklore*, *Western Folklore*), or computational narrative (the CMN workshop, Text2Story).
- **Authorship and the role of the models.** How the paper describes the models as instruments, and the keeper's part.
