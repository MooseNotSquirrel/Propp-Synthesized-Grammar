# Rules for describing what each act means for the story

**You are adding a third layer to an existing description of some stories.**
Another reader has already listed, event by event, the acts in each story: what is done, who does it, to whom, and how the two stand to each other.
Your task is to say, for each of those acts, what it means for the course of the story: whom it helps or harms, what part it plays in the story's problems, and which other act it answers or makes possible.
You do not change the acts, and you do not judge whether they were listed well.

## What you are given

**Your input file** holds your stories, one after another.
Each story opens with a line naming its identifier, its title and its hero:

```
story: A093 | Witch and Sun's Sister | hero: Ivan-tsarevich
```

Then come its events in order, each followed by the acts listed for it, one per line, each with an identifier:

```
  ev 1 | The groom tells Ivan of the witch sister to come
    e0001 | reveal-information | конюх | Иван-царевич | below | "<quoted words>"; the groom tells Ivan
```

The fields of an act line are: its identifier, the act, the one who does it, the one it is done to (or `-`), their relation, and the other reader's note.
Names may be written in the story's own language while the hero line is in English; they are the same people.
Where the hero line says the story divides between two characters, count either of them as the hero.

**The story's text** is also yours to read, in the file your task names.

## Read the whole story first

**Whether an act helps or harms, opens or repairs, depends on what comes after it.**
Read the whole story, and the whole list of acts, before you write anything for it.

## What you write for each act

**One line per act, in the order of your input file, with every act given a line.**

```
e0001 | undergoes | harms | serves | p1 | enables | e0004 |   | the warning sets Ivan's flight going
```

The fields are: the act's identifier, the hero's part, its value for the hero, its place in a problem, the problem's label, the kind of link, the act it links to, a question mark if you are unsure, and one short sentence saying why.

### The hero's part

| Part | Meaning |
|---|---|
| does | The hero does the act. |
| undergoes | The act is done to the hero. |
| both | The hero does it to themselves, or is on both sides of it. |
| neither | The hero neither does it nor undergoes it. |

### Its value for the hero

| Value | Meaning |
|---|---|
| helps | The act brings the hero closer to what the hero needs, or protects the hero, or turns out in the hero's favor. |
| harms | The act hurts the hero, or those the hero is bound to, or puts them in danger, or turns out against the hero. |
| neither | Neither, as far as the story shows. |

Judge the value by what the act leads to in the story, not by what the one who does it intends.
A warning the hero ignores still helps; a gift that later ruins the hero harms.

### Its place in a problem

**A problem is a harm done or a lack felt that the story then works on, whether or not it is ever solved.**
A story may have one problem or several, one after another or overlapping.

| Place | Meaning |
|---|---|
| opens | A problem begins with this act: the harm is done, or the lack is first felt. |
| worsens | A problem already open gets worse: a new harm is added to it, or its solution moves further away. |
| serves | The act prepares a problem's opening, or moves toward its solution, without itself opening, worsening or solving it: a warning, a trick that leads to the harm, a request for help, a test, a gift that will help later, a journey toward the solution. |
| repairs | The problem is solved or undone, wholly or in part: the captive freed, the lost thing recovered, the enemy defeated, the want met. |
| rewards | Someone is rewarded for their part in a problem, once it is over or in passing. |
| punishes | Someone is punished for their part in a problem. |
| none | The act has no place in any problem of the story. |

### The problem's label

**Label the story's problems p1, p2, p3, in the order in which they open.**
Give each act the label of the problem it belongs to; an act that serves a problem before it opens takes the label of the problem it leads to.
Write `-` where the place is none.
The first time a label is used, add one line for it, just before the act that first uses it, naming it in a few words:

```
A093 | problem | p1 | the witch sister threatens to eat the household
```

### The link

| Link | Meaning |
|---|---|
| answers | This act responds to an earlier act: an answer to a request, a test or a threat; a breach of a prohibition; a counterattack; a reward or punishment for a deed. |
| enables | This act makes a later act possible: information that lets a harm be done, a gift that lets the hero win, a journey that brings the hero where the task is. |
| none | Neither. |

Give the identifier of the act it answers or enables, or `-` with none.
Where an act both answers one act and enables another, give the link that matters more to the story.

## What you do not do

**Do not name any other system of analysis.**
Describe each act in the terms above only.
Do not change, add or remove any act, even one you think was listed wrongly; describe it as listed, and say so in your sentence if it puzzles you.

## Your report

**End with a short report.**
List every place where these rules left you unsure what to write, with the story and the act's identifier.
Do not summarize the stories.
