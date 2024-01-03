# Kofi Method German Conjugation Anki

<img src="logo/kofi-logo.png" width="200" height="200">

🤖: AI-made image

Inspired by [Lisardo's Kofi Method](https://www.asiteaboutnothing.net/w_ultimate_italian_conjugation.html#:~:text=What%20is%20the%20KOFI%20Method,to%20formally%20study%20the%20language)

## Conjugation Forms Included

- Präsens (Present Tense): "Du sprichst" (You speak)
- Indikativ Präteritum (Simple Past Tense): "Du sprachst" (You spoke)
- Konjunktiv II Präteritum (Subjunctive Past Tense): "Du sprächest" (You spoke)
- Imperativ (Imperative Mood): "Sprich!" (Speak!)
- Partizip I (Present Participle): "sprechend" (speaking)
- Partizip II (Past Participle): "gesprochen" (spoken)
- Infinitiv mit zu (Infinitive with "zu"): "zu sprechen" (to speak)

These forms are the building blocks of German verb conjugation.

### Filtering out Konjunktiv II Präteritum

The Konjunktiv II Präteritum is not commonly used in everyday German. But, it is still included in this deck for those who would like to use it.
I on the other hand will choose to remove it, BUT, not for modal verbs where it is used in everyday German.

If you would like to do the same follow these instructions:
1. From the main Anki screen click on top button "Browse"
2. You should see a search field with placeholder text saying "Search cards/notes..."
3. Type in the text within the parentheses -> ("deck:KOFI German" tag:tense:Konjunktiv_II_Präteritum -tag:modal_verb)
4. Click on the first field and then scroll all the way to bottom. Shift + Left Click on the last field.
5. Right click and the menu should show "Cards" at the bottom. Hover over that and click  a

1. Go to "Tools" menu and select "Create Filtered Deck"

2.
1. In the "Search" field of the Create Filtered Deck dialog, you will enter a search string using Anki's search syntax to include and exclude tags.
2. To include cards that have a specific tag, but exclude cards with another tag, use a search query like this: (tag:include-tag) -(tag:exclude-tag -tag:include-tag).
3. Replace include-tag with " " and exclude-tag with " "
Your search query would be: (tag:science) -(tag:difficult -tag:science).


Mastery of these elements allows learners to construct and understand a variety of complex tenses with minimal memorization of additional forms.

## Why Not the Rest of the Forms?

While other tenses and forms exist in German, they can often be formed using the key forms included in this deck:

- Perfekt (Present Perfect): haben/sein (in Präsens form) + Partizip II
  "Du hast gesprochen" (You have spoken)

- Plusquamperfekt (Past Perfect): haben/sein (in Präteritum form) + Partizip II
  "Du hattest gesprochen" (You had spoken)

- Futur I (Future I): werden (in Präsens form) + Infinitiv
  "Du wirst sprechen" (You will speak)

- Futur II (Future Perfect): werden (in Präsens form) + Partizip II + haben/sein (Infinitiv)
  "Du wirst gesprochen haben" (You will have spoken)

- Konjunktiv I and II (Subjunctive I and II): Based on Präsens or Präteritum forms
  Konjunktiv I: "Du sprechest" (You speak, indirect speech)


You should still give a glance at the other forms and can do so through [Duden.de](https://www.duden.de/konjugation/sprechen).

References for irregular verbs:
https://jakubmarian.com/list-of-irregular-strong-german-verbs/

## Steps to setup

Steps:

1. Setup Azure Ai Services account https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python

- Explain the amount created should not cost them anything since 500,000 use of characters is free
