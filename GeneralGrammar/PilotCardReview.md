# The two cards, for the owner to compare (CardPilotProtocol.md section 2)

**Readers in cell S see only the Code and S's definition columns, in this shuffled order.** This sheet, with the key, stays in the keeper's repository.

## The card

| Code | His symbol | His name (dropped in S) | Definition in H | Changed in S? |
|---|---|---|---|---|
| Wob | L | unfounded claims | A false hero claims what is not theirs: a deed, a reward, a quality. | same |
| Lun | E | the hero's reaction | The hero responds to that test or request: passes or fails it, helps or refuses, withstands or yields. | same |
| Nep | T | transfiguration | The hero is given a new appearance. | same |
| Zab | C | beginning counteraction | The hero decides or agrees to act against the misfortune or lack. | same |
| Sef | δ | violation | The prohibition is broken, or the order is not obeyed. | same |
| Rav | ε | reconnaissance | The villain tries to find out something about the victim: where they are, or what they have. | same |
| Bip | N | solution | The task is accomplished. | same |
| Lom | F | receipt of an agent | The hero gets something or someone that will help: given, earned, bought, found, seized, or a helper offering service. | same |
| Mur | γ | interdiction | Someone is forbidden to do something, or ordered to do something. | same |
| Vek | B | mediation | The misfortune or lack is made known to someone who might act on it; the hero is asked, ordered, allowed, or sent to act. A lament or complaint to no one who might act is X. | same |
| Mip | β | absentation | A member of a household, or the one who protects it, goes away or dies, leaving others unprotected. | same |
| Dov | θ | complicity | The victim is taken in by the deception and so unwittingly helps the villain. A victim who refuses or sees through the trick has not performed θ: write that act X. | S: The victim is taken in by the deception and so unwittingly helps the villain. A victim who refuses or sees through the trick has not performed Dov: write that act X. |
| Suv | G | guidance | The hero is led, carried, or shown the way to what is sought. | same |
| Vig | H | struggle | The hero and the villain meet in direct combat or contest. | same |
| Fub | ↓ | return | The hero returns to where they set out from. | same |
| Yul | W | wedding | The hero marries or is rewarded with rank, wealth or a throne. | same |
| Qet | o | unrecognized arrival | The hero arrives, at home or elsewhere, without being recognized. | same |
| Tiv | α | initial situation | The characters and their situation are introduced. Not a function; write it only for an event that does nothing but introduce. An event that narrates an act is never α. | S: The characters and their situation are introduced. Not an act on this card; write it only for an event that does nothing but introduce. An event that narrates an act is never Tiv. |
| Gop | Pr | pursuit | The hero is pursued. | same |
| Dek | Rs | rescue | The hero is saved from pursuit or from destruction. | same |
| Hab | a | lack | Someone lacks or desires something: food, safety, a mate, a possession, a quality they do not have. | same |
| Hux | Q | recognition | The hero is recognized. | same |
| Poz | D | first function of the donor | The hero is tested, questioned, asked for help, or attacked by someone who may then give help. | same |
| Jem | K | liquidation | The original misfortune or lack is set right: the loss restored, the want satisfied, the victim freed. | same |
| Nar | M | difficult task | A difficult task or test is set. | same |
| Kib | U | punishment | The villain or false hero is punished. | same |
| Baf | Ex | exposure | The false hero or the villain is exposed. | same |
| Sog | ζ | delivery | The villain receives that information. | same |
| Gul | I | victory | The villain is defeated: killed, beaten, outwitted, or driven off. | same |
| Zin | J | branding | The hero is marked: wounded, or given a token that can later identify them. | same |
| Pov | ↑ | departure | The hero leaves home or sets out. | same |
| Rud | η | trickery | The villain, often in disguise or with false words, tries to deceive the victim in order to get hold of them or what they have. | same |
| Dox | A | villainy | The villain does harm: kills, carries off, steals, injures, drives out, deceives to ruin, or otherwise causes loss or misfortune. | same |
| Kem | λ | preliminary misfortune | A misfortune that forces the victim to accept the villain's deceitful bargain. | same |

## Every other line changed: wonder

- **H:** # Transcriber rules: Afanasyev's tales in Propp's notation
- **S:** # Coding rules: a collection of tales
- **H:** These rules turn tales from Aleksandr Afanasyev's collection of Russian folktales, read in their original language, into strings of the function symbols Vladimir Propp defined for the folktale.
- **S:** These rules turn tales from a collection of Russian folktales, read in their original language, into strings of the symbols on the card below.
- **H:** Do not open other files, do not search the web, and do not use any published analysis of these tales in Propp's terms.
- **S:** Do not open other files, do not search the web, and do not use any published analysis of these tales.
- **H:** Transcribe from the text and from the definitions card alone.
- **S:** Code from the text and from the card alone.
- **H:** `Events.txt` has one line per event: tale identifier, event number, and a short plain paraphrase without Propp's terms.
- **S:** `Events.txt` has one line per event: tale identifier, event number, and a short plain paraphrase.
- **H:** **Each act in an event gets one entry: a function symbol, or X.**
- **S:** **Each act in an event gets one entry: a symbol from the card, or X.**
- **H:** Propp defines a function as "an act of a character, defined from the point of view of its significance for the course of the action" (p.21).
- **S:** A symbol on the card stands for an act of a character, defined from the point of view of its significance for the course of the action.
- **H:** Where an event's words narrate two or more distinct acts, give each act that fulfills a function its own entry, in the order the text narrates them.
- **S:** Where an event's words narrate two or more distinct acts, give each act that fits a symbol its own entry, in the order the text narrates them.
- **H:** A single act gets a single entry; where it could be read two ways, choose by what it causes in the tale, as Propp does (p.67).
- **S:** A single act gets a single entry; where it could be read two ways, choose by what it causes in the tale.
- **H:** An event none of whose acts fulfills a function gets one X.
- **S:** An event none of whose acts fits a symbol gets one X.
- **H:** A closing speech, a retort, a lament or a verdict, that the tale's point turns on matters, even when no function names it.
- **S:** A closing speech, a retort, a lament or a verdict, that the tale's point turns on matters, even when no symbol names it.
- **H:** Mark every entry, X included: an X that matters is an act the tale needs that no function names.
- **S:** Mark every entry, X included: an X that matters is an act the tale needs that no symbol names.
- **H:** **Assign the function whoever performs it.**
- **S:** **Assign the symbol whoever performs it.**
- **H:** Propp: "Functions of characters serve as stable, constant elements in a tale, independent of how and by whom they are fulfilled" (p.21).
- **S:** The acts on the card are stable, constant elements in a tale, independent of how and by whom they are fulfilled.
- **H:** Do not write X because a function's usual partner is absent.
- **S:** Do not write X because a symbol's usual partner is absent.
- **H:** Do not assign a function because the surrounding entries seem to call for one.
- **S:** Do not assign a symbol because the surrounding entries seem to call for one.
- **H:** When in doubt between a function and X, write X, with the nearest candidate in the note; a notation stretched to fit anything will let anything pass, and a high share of X is a finding, not a failure.
- **S:** When in doubt between a symbol and X, write X, with the nearest candidate in the note; a notation stretched to fit anything will let anything pass, and a high share of X is a finding, not a failure.
- **H:** Until something harmful is actually done, a request or demand is the asker's lack (a) when it is where that want is first stated, and X when the want was stated before.
- **S:** Until something harmful is actually done, a request or demand is the asker's lack (Hab) when it is where that want is first stated, and X when the want was stated before.
- **H:** **The hero asking another for help is not the donor's function.**
- **S:** **The hero asking another for help is not Poz.**
- **H:** The hero's request is a when it is where the hero's want is first stated, and X otherwise; the answer to it is F when help is given and F− when it is refused.
- **S:** The hero's request is Hab when it is where the hero's want is first stated, and X otherwise; the answer to it is Lom when help is given and Lom− when it is refused.
- **H:** Propp: "Each new act of villainy, each new lack creates a new move" (p.92).
- **S:** Each new act of villainy, each new lack creates a new move.
- **H:** Only a new villainy or lack opens a move: the same demand, want or harm repeated toward the same end is written with its function in the move already begun.
- **S:** Only a new villainy or lack opens a move: the same demand, want or harm repeated toward the same end is written with its symbol in the move already begun.
- **H:** **Write the bare letter; do not write variety numbers.**
- **S:** **Write each symbol as the card gives it.**
- **H:** A minus marks a negative result: E− for a test the hero fails, F− where nothing is given, I− where the hero loses the fight, and likewise on any function whose outcome is negative.
- **S:** A minus marks a negative result: Lun− for a test the hero fails, Lom− where nothing is given, Gul− where the hero loses the fight, and likewise on any symbol whose outcome is negative.
- **H:** A000 | I | 3 | ev 3 | D | <performer> | <undergoer> | Y | ev 7 |   | "<the key words of the clause, quoted>"; <note>
- **S:** A000 | I | 3 | ev 3 | Poz | <performer> | <undergoer> | Y | ev 7 |   | "<the key words of the clause, quoted>"; <note>
- **H:** A000 | I | 4 | ev 4 | X | <performer> | <undergoer> | N | - | ? | "<quoted words>"; X, perhaps E
- **S:** A000 | I | 4 | ev 4 | X | <performer> | <undergoer> | N | - | ? | "<quoted words>"; X, perhaps Lun
- **H:** Do not summarize the results or comment on how well Propp fits.
- **S:** Do not summarize the results or comment on how well the card fits.

## Every other line changed: east

- **H:** # Transcriber rules: the East Asian tales in Propp's notation
- **S:** # Coding rules: a collection of tales
- **H:** These rules turn tales from two collections of East Asian tales, Chinese (told at Swatow) and Japanese, in the English of their collectors, into strings of the function symbols Vladimir Propp defined for the folktale.
- **S:** These rules turn tales from two collections of East Asian tales, Chinese (told at Swatow) and Japanese, in the English of their collectors, into strings of the symbols on the card below.
- **H:** Do not open other files, do not search the web, and do not use any published analysis of these tales in Propp's terms.
- **S:** Do not open other files, do not search the web, and do not use any published analysis of these tales.
- **H:** Transcribe from the text and from the definitions card alone.
- **S:** Code from the text and from the card alone.
- **H:** In the Chinese tales (identifiers beginning C), the collector tells the tales inside a story of her own, about a group of children and their teacher, in which the tales are told. Passages of that story stand between the tales and may fall at the end of a tale's file. They are not part of the tale: list only the tale itself, from its title to its end.
- **S:** In the Chinese tales, the collector tells the tales inside a story of her own, about a group of children and their teacher, in which the tales are told. Passages of that story stand between the tales and may fall at the end of a tale's file. They are not part of the tale: list only the tale itself, from its title to its end.
- **H:** `Events.txt` has one line per event: tale identifier, event number, and a short plain paraphrase without Propp's terms.
- **S:** `Events.txt` has one line per event: tale identifier, event number, and a short plain paraphrase.
- **H:** **Each act in an event gets one entry: a function symbol, or X.**
- **S:** **Each act in an event gets one entry: a symbol from the card, or X.**
- **H:** Propp defines a function as "an act of a character, defined from the point of view of its significance for the course of the action" (p.21).
- **S:** A symbol on the card stands for an act of a character, defined from the point of view of its significance for the course of the action.
- **H:** Where an event's words narrate two or more distinct acts, give each act that fulfills a function its own entry, in the order the text narrates them.
- **S:** Where an event's words narrate two or more distinct acts, give each act that fits a symbol its own entry, in the order the text narrates them.
- **H:** A single act gets a single entry; where it could be read two ways, choose by what it causes in the tale, as Propp does (p.67).
- **S:** A single act gets a single entry; where it could be read two ways, choose by what it causes in the tale.
- **H:** An event none of whose acts fulfills a function gets one X.
- **S:** An event none of whose acts fits a symbol gets one X.
- **H:** A closing speech, a retort, a lament or a verdict, that the tale's point turns on matters, even when no function names it.
- **S:** A closing speech, a retort, a lament or a verdict, that the tale's point turns on matters, even when no symbol names it.
- **H:** Mark every entry, X included: an X that matters is an act the tale needs that no function names.
- **S:** Mark every entry, X included: an X that matters is an act the tale needs that no symbol names.
- **H:** **Assign the function whoever performs it.**
- **S:** **Assign the symbol whoever performs it.**
- **H:** Propp: "Functions of characters serve as stable, constant elements in a tale, independent of how and by whom they are fulfilled" (p.21).
- **S:** The acts on the card are stable, constant elements in a tale, independent of how and by whom they are fulfilled.
- **H:** Do not write X because a function's usual partner is absent.
- **S:** Do not write X because a symbol's usual partner is absent.
- **H:** Do not assign a function because the surrounding entries seem to call for one.
- **S:** Do not assign a symbol because the surrounding entries seem to call for one.
- **H:** When in doubt between a function and X, write X, with the nearest candidate in the note; a notation stretched to fit anything will let anything pass, and a high share of X is a finding, not a failure.
- **S:** When in doubt between a symbol and X, write X, with the nearest candidate in the note; a notation stretched to fit anything will let anything pass, and a high share of X is a finding, not a failure.
- **H:** Until something harmful is actually done, a request or demand is the asker's lack (a) when it is where that want is first stated, and X when the want was stated before.
- **S:** Until something harmful is actually done, a request or demand is the asker's lack (Hab) when it is where that want is first stated, and X when the want was stated before.
- **H:** **The hero asking another for help is not the donor's function.**
- **S:** **The hero asking another for help is not Poz.**
- **H:** The hero's request is a when it is where the hero's want is first stated, and X otherwise; the answer to it is F when help is given and F− when it is refused.
- **S:** The hero's request is Hab when it is where the hero's want is first stated, and X otherwise; the answer to it is Lom when help is given and Lom− when it is refused.
- **H:** Propp: "Each new act of villainy, each new lack creates a new move" (p.92).
- **S:** Each new act of villainy, each new lack creates a new move.
- **H:** Only a new villainy or lack opens a move: the same demand, want or harm repeated toward the same end is written with its function in the move already begun.
- **S:** Only a new villainy or lack opens a move: the same demand, want or harm repeated toward the same end is written with its symbol in the move already begun.
- **H:** **Write the bare letter; do not write variety numbers.**
- **S:** **Write each symbol as the card gives it.**
- **H:** A minus marks a negative result: E− for a test the hero fails, F− where nothing is given, I− where the hero loses the fight, and likewise on any function whose outcome is negative.
- **S:** A minus marks a negative result: Lun− for a test the hero fails, Lom− where nothing is given, Gul− where the hero loses the fight, and likewise on any symbol whose outcome is negative.
- **H:** A000 | I | 3 | ev 3 | D | <performer> | <undergoer> | Y | ev 7 |   | "<the key words of the clause, quoted>"; <note>
- **S:** A000 | I | 3 | ev 3 | Poz | <performer> | <undergoer> | Y | ev 7 |   | "<the key words of the clause, quoted>"; <note>
- **H:** A000 | I | 4 | ev 4 | X | <performer> | <undergoer> | N | - | ? | "<quoted words>"; X, perhaps E
- **S:** A000 | I | 4 | ev 4 | X | <performer> | <undergoer> | N | - | ? | "<quoted words>"; X, perhaps Lun
- **H:** Do not summarize the results or comment on how well Propp fits.
- **S:** Do not summarize the results or comment on how well the card fits.
