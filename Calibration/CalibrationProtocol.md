# The Afanasyev calibration: how good is the measuring stick?

**Frozen 2026-10-04, before any tale is listed or transcribed.** Nothing below changes after this commit; a departure is logged in `KeeperLog.md`, not made here.

## The question

Every genre result of this project rests on blind transcription by language models under one set of rules and one definitions card. This test asks whether that instrument reproduces Propp's own analysis on the tales Propp analyzed. If it cannot, the genre results are partly about the transcribers.

## The material

**The tales:** the 45 tales whose schemes Propp printed in Appendix III, as the first project holds them (`TaleTokenStreamsV4Utf8.txt`, numbers 93 to 167, the collection's modern numbering). Their texts are in the transcriber repository `Story Language/Afanasyev` (GitHub Propp-Afanasyev), in the original language, from Russian Wikisource, which follows the academic edition of 1984-85.

**Propp's answer:** each tale's scheme as `embedCorpus.py` derives it from that file: per move, the base symbols with varieties and signs dropped. Branching braces are flattened in printed order, every branch kept, since Propp uses them for repeated and parallel episodes; an embedded move is expanded where it stands. Propp's schemes print no preparatory functions (p.116), so they are left out of ours before comparing.

## The instrument, in two arms

**Arm U, the card as used:** the rules and definitions card exactly as the Aesop and tragedy tests used them, refusal problem included. This calibrates the stick we have.

**Arm C, the card corrected:** the same, with one sentence added to complicity θ: a victim who refuses or sees through a trick has not performed θ, and the act is written X. This measures the fix the trick audit called for.

**The runs:** fresh event listers on Opus list each tale's events and cast from the original text, once; both arms transcribe the same event lists. In each arm transcriber A runs on Opus and B on Sonnet, blind to each other and to the other arm. Listers and transcribers read the tales in their original language; the rules, the card and every output are in English.

**Not done: the translation pilot.** The plan once set machine translation against reading the original, in a small pilot. It is dropped: a translation adds a layer between text and function that this test exists to keep out, and the models read Russian. If arm U fails, translation becomes one of the things to try.

**Nothing in the transcriber repository says that Propp analyzed these tales.** The prompts and Readme name them as tales from Afanasyev's collection.

## What is compared

For each transcription, each tale's stream is its functions marked Y, in the order of its notes, with X entries and preparatory functions left out, symbols reduced as the tragedy scoring reduces them. Four measures:

1. **Content:** the Dice overlap of the multisets of symbols, ours against Propp's, per tale, averaged over tales.
2. **Order:** one minus the Levenshtein distance between the two sequences, divided by the longer one's length, per tale, averaged.
3. **Moves:** the share of tales where our move count equals Propp's.
4. **Acceptance:** the share of our moves that v46 as shipped accepts at `move` (Propp's own moves: 80 of 84).

**The yardstick:** measures 1 to 3 computed between transcriber A and transcriber B of the same arm: how far two transcribers agree with each other, which is the most the instrument can be expected to agree with Propp.

**The baseline:** measures 1 and 2 with each transcription paired with Propp's scheme for a different tale, over 1000 random derangements, seed 46: how much agreement is generic, coming from what all wondertales share.

## The verdict, per arm and transcriber

**CALIBRATED** if all four hold:
1. content agreement with Propp is at least 0.8 of the A-B content agreement;
2. order agreement with Propp is at least 0.8 of the A-B order agreement;
3. both content and order agreement with Propp exceed the derangement baseline, with at most 50 of 1000 derangements at or above;
4. v46 accepts at least 75% of our moves.

**PARTLY CALIBRATED** if 3 holds and any of 1, 2 and 4 fails.

**NOT CALIBRATED** if 3 fails: our transcriptions are no closer to Propp's scheme for a tale than to his scheme for another.

Arm C against arm U is reported, measure by measure, and not judged.

## The memory probe

The transcribers are models that may have read Propp's book. A transcriber recalling his schemes would look calibrated without reading the tale. So, AFTER both arms' transcriptions are committed and only then (the probe's prompts would tell a transcriber whose tales these are), fresh instances on Opus and on Sonnet are asked, from memory and without the texts, for Propp's Appendix III scheme for each tale by number and title. Their answers are scored by measures 1 and 2.

**MEMORY IMPLAUSIBLE** if, for each model, recall content agreement is at least 0.15 below that model's transcription content agreement in arm U. Otherwise **MEMORY POSSIBLE**, and the calibration verdict is reported as possibly inflated by recall.

## Order of work

1. This protocol, committed. 2. The rules and prompts of both arms, and the run file, committed to the transcriber repository. 3. The listing stage; the keeper checks the lists for form. 4. Both arms' transcription stages; checked for form. 5. The probe's prompts committed, and the probe run. 6. The comparison, by a program committed before step 4's results are read.
