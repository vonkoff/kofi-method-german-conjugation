ge_deck_id = 391834738
ge_deck_name = 'KOFI German'

tense_order = ["tag:Infinitiv", "tag:Partizip_I", "tag:Partizip_II",
               "tag:Imperativs", "tag:Präsens", "tag:Indikativ_Präteritum",
               "tag:Konjunktiv_II_Präteritum"]
person_order = ["tag:ich", "tag:du", "tag:er/sie/es",
                "tag:wir", "tag:ihr", "tag:sie/Sie", "tag:ihr/Sie"]


modal_verbs = ["können", "müssen", "wollen", "sollen", "dürfen", "mögen"]

templates = {
    "Präsens": "⊙ Jetzt gerade, ⊙<br>{2} <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> über die Vergangenheit.",
    "Ind. Präteritum": "← Zu dieser Zeit, oft, ←<br>{2} <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> gestern über die Vergangenheit",
    "Sub. Präteritum": "↫ Es war überraschend, dass ↫<br>{2} <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> gestern über die Vergangenheit",
    "Imperativs": "Bitte, Mann, <br><span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> jetzt!",
    "Partizip I": "Beim <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> denkt er an die Vergangenheit",
    "Partizip II": "Das Objekt is <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> worden",
    "Infinitiv": "Das Verb in<br><span class=\"cloze_hilite\"> er {1} </span><br>ist zu <span class=\"de_verb\">{{{{c1::{0}}}}}</span>"
}

# Borrowed from Lisardo https://www.asiteaboutnothing.net/w_ultimate_spanish_conjugation.html#tags
kofi_css = """
.night_mode {
/*
disable the color inverter to display colors how I intended them
See:
https://github.com/ankidroid/Anki-Android/wiki/Advanced-formatting#customize-night-mode-colors
https://github.com/ankidroid/Anki-Android/issues/6921
*/
}

.card {
 font-family: Arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.front, .back { /* not quite as bright as white */
 color: rgb(203, 209, 209);
}

.back {
  text-align: left;
}

.tag_SECTION {
  font-size: 0.8em;
  color: #999;
}

.tags {
  font-style: italic;
}

.orientation_hint {
  font-style: italic;
  color: #999;
}

.orientation_pop_back {
   color: rgb(113, 171, 194);
}

.orientation_inf { /*  spelling change, e.g c => z */
  color: rgb(209, 199, 158);
}


.have_fun {
   color: rgb(113, 171, 194);
   font-size: 2em;
}


orientation_examples, .orientation_examples {
 color: rgb(203, 209, 209);
  text-align: left;
}


.info_cloze {  /*  the [...OK...] */
  color: rgb(210, 142, 2);
}


.hint {  /*  hints on the front, e.g. (tú/vos) or (Haber) */
  color: #999;
}

.en_verb {  /*  the English verb on the front card */
  color: rgb(210, 142, 2);
}

.de_verb {  /* the German verb on the back card */
  color: rgb(210, 142, 2);
}

.de_hint {  /* on the back card, additional text with the answer, e.g. */ (gestern über die Vergangenheit)
  text-align: left;
  color: #999;
}

.de_prn { /* the pronoun on the Germ side. Since it's optional, it can be greyed out */
  color: #999;
}

.alt_conj, .alt_to_inf { /* The conjugated form of a similar verb, or the infinitive */
  color: rgb(209, 199, 158);
}

.alt_to_inf a:link, .alt_to_inf a:visited, .alt_to_inf a:active, .alt_to_inf a:hover {
  color: rgb(209, 199, 158);
  border-bottom: 1px dashed rgb(88, 157, 246);
  text-decoration: none;
}

.alt_inf { /* the infinitive of alternate verbs in parentheses, as in (atañer) */
  font-style: italic;
}

.alt_inf a:link, .alt_inf a:visited, .alt_inf a:active, .alt_inf a:hover {
  color: rgb(203, 209, 209);
  border-bottom: 1px dashed rgb(88, 157, 246);
  text-decoration: none;
}

.alt_tu_vos { /* in alternates that have tú and vos, the respective tú and vos headers */
  color: rgb(98, 151, 85);
}
.en_hilite { /* special words on front card, e.g. 'was' in 'It was' */
  text-align: left;
 color: rgb(113, 171, 194);
}

.tu_vos_hint { /* how (tú/vos) should appear on the front of cards that do have a vos */
  color: rgb(98, 151, 85);
  font-style: italic;
}


.note_feature { /* A feature of a verb that we want to highlight in the notes, e.g. Unique, Impersonal */
  color: rgb(136, 136, 198);
}

.note_pop { /* A misc feature to highlight in the notes, e.g. podrí */
   color: rgb(255, 0, 128);
}

.note_numb { /* a number in the notes */
  color: rgb(31, 139, 210);
}

.note_spell { /*  spelling change, e.g c => z */
  color: rgb(209, 199, 158);
}

.note_de_word  { /* A German word used in the notes, e.g. 'me' */
  font-style: italic;
}

.note_english_highlight  { /* Let's Go */
  font-style: italic;
  color: rgb(209, 199, 158);
}


.notes_de_form {  /* One of the answer's conjugated forms, when mentioned in the notes */
  color: rgb(210, 142, 2);
}

.notes_de_inf { /*  the German infinitive of the current verb, when mentioned in the notes*/
  font-style: italic;
  color: rgb(209, 199, 158);
}

.notes_usage { /* something specific, like sea lo que fuere*/
  color: rgb(113, 171, 194);
  font-style: italic;
}

.notes_usage a:link, .notes_usage a:visited, .notes_usage a:active, .notes_usage a:hover {
  color: rgb(113, 171, 194);
  border-bottom: 1px dashed rgb(88, 157, 246);
  text-decoration: none;
}

.notes_usage_english { /* translation of something specific, like sea lo que fuere*/
  font-style: italic;
}

.dle_conj a:link, .dle_conj a:visited, .dle_conj a:active {
  color: rgb(209, 199, 158);
  border-bottom: 1px dashed rgb(88, 157, 246);
  text-decoration: none;
  font-style: italic;
}

.dle_conj a:hover {
  color: rgb(88, 157, 246);
  text-decoration: none;
  font-style: italic;
}

.wrong_conj {  /* wrong theoretical conjugation */
  color: rgb(205, 92, 92);
  font-style: italic;
}

.verb_numbers { /* number of verbs in this family */
  color: rgb(209, 199, 158);
}

.cloze_hilite { /* special words on front card */
 color: rgb(113, 171, 194);
  font-style: italic;
}

.cloze_pronoun {  /*  the pronoun on the front */

}

.manual {
  font-size: 0.8em;
  color: #999;
}

.manual a:link, .manual a:visited, .manual a:active {
  color: rgb(255, 128, 64);
  border-bottom: 1px dashed rgb(255, 128, 64);
  text-decoration: none;
  font-style: italic;
}

.manual a:hover {
  color: rgb(255, 0, 128);
  border-bottom: 1px dashed rgb(255, 0, 128);
  text-decoration: none;
  font-style: italic;
}

/* UNUSED COLORS
The following classes are not used in the deck.
They are included here for convenience: they are colors I find eye-pleasing and consistent with the current palette. Having them here makes it easy to copy the color codes to different classes whose styles I might want to change around.

Snippets:
  color: rgb();
*/
.whitish { /* several options */
  color: rgb(203, 209, 209);
  color: rgb(209, 199, 158);
  color: rgb(255, 216, 183);
}
.blue { /* several options */
  color: rgb(113, 171, 194);
  color: rgb(88, 157, 246);
  color: rgb(31, 139, 210);
  color: rgb(104, 151, 187);
}
.brown {
  color: rgb(210, 142, 2);
}
.pink {
  color: rgb(255, 0, 128);
  color: rgb(255, 170, 170);
}
.yellow { /* several options */
  color: rgb(255, 198, 109);
  color: rgb(251, 188, 66);
  color: rgb(230, 219, 116);
}
.green { /* several options */
  color: rgb(98, 151, 85);
  color: rgb(127, 159, 127);
  color: rgb(67, 134, 0);
  color: rgb(142, 192, 116);
}

.purple {  /* several options */
  color: rgb(128, 128, 255);
  color: rgb(136, 136, 198);
  color: rgb(151, 118, 170);
}

.orange {
  color: rgb(255, 128, 64);"
}
"""
