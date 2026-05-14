---
name: de-ai
description: Strip AI voice from text — humanize while preserving meaning. Combines glebis's RU/EN/DE/ES/FR/PT/JP/IT diagnostic pipeline with the author's Humanizer Prompt + the Buddha-at-2-AM shipped-manuscript reverse-engineering + the (redacted) Russian-original voice analysis. Use for KDP books, the publication series, marketing copy, or any text that needs to read like a real person wrote it. Pairs with locked voice voice spec.
---

# De-AI / Humanizer — canonical text humanization

The ONE place for text humanization. Combines four lineages:

- **glebis/de-ai diagnostic pipeline** — 6-level AI-tell scan, multi-language
- **the author's Humanizer Prompt** — forbidden words + voice rules (post-2026-04-27 KDP termination response)
- **an exemplar manuscript reverse-engineering** — counted from the only shipped KDP-approved manuscript
- **Source-voice reference audit** — anchor the locked voice register to a real ancestor text (PDF, transcript, or published book in the target voice).

The standalone `humanizer_prompt.md` memory entry is superseded by this skill. Don't run two passes — this skill IS the canonical pass.

**Full operational reference:** `C:\Users\A\Desktop\Books\_new_concepts\_shared\HUMANIZER_STYLE_GUIDE.md` (461-line deep reference; this skill is the operational entry point).

**Companion voice spec:** `C:\Users\A\Desktop\Books\_new_concepts\_shared\VEGAN_BADASS_VOICE.md` — the writing rules. This skill is the detection / scrubbing rules. Use both together.

---

## When to use

- KDP non-fiction (the publication series, an exemplar manuscript, an exemplar manuscript, business-book digests, the inspirational 5-book batch)
- Bible + AI book (queued) — entire manuscript humanized through this pipeline
- Marketing copy (Amazon listings, BookTok captions, landing page hero copy)
- Final polish pass on Mother Simulator narrator voice
- Russian-language sites (the marketplace project) — strips RU-specific AI patterns
- the project manual / wellness copy where authenticity matters

## When NOT to use

- Literary fiction character voices that are intentionally stylized (ELEOS in Compassion Algorithm — clinical is the point)
- Translations where matching source register matters
- Code, JSON, technical specs — humanization breaks them

---

## The two-pass pipeline

Run BOTH passes in order. Don't skip Pass 2 — that's where soul gets added back.

### PASS 1 — Strip AI tells

**Content sins (cut or rewrite):**
- Significance inflation: "marking a pivotal moment", "testament to", "underscores"
- Promotional fluff: "nestled", "breathtaking", "vibrant", "groundbreaking", "cutting-edge"
- Superficial -ing analyses: "symbolizing...", "reflecting...", "showcasing..."
- Vague attributions: "Experts believe", "Industry reports suggest"
- Formulaic challenges: "Despite X... continues to thrive"
- Generic conclusions: "The future looks bright", "Exciting times ahead"

**Banned vocabulary (replace or delete every instance):**
`additionally`, `furthermore`, `moreover`, `delve`, `landscape`, `tapestry`, `multifaceted`, `nuanced`, `pivotal`, `intricate`, `interplay`, `underscore`, `testament`, `leverage`, `paradigm`, `foster`, `comprehensive`, `robust`, `keen`, `arguably`, `notably`, `realm`, `embark`, `holistic`, `synergy`, `encompass`, `shed light`, `serve as`, `at its core`, `it is worth noting`, `navigate` (metaphorical), `journey` (metaphorical), `embrace`, `profound`, `optimize`, `framework`, `mindset`, `intentional`, `authentic`, `lean into`, `showing up`, `actionable`, `takeaway`, `utilize`, `at the end of the day`, `respectful`, `honor the process`, `ultimately`, `in many ways`, `key insight`, `step-by-step`.

**Structure sins:**
- Copula avoidance: "serves as", "functions as", "boasts" → use `is` or `has`
- Rule of three: forcing everything into triple lists — break to 2 or 4
- Synonym cycling: protagonist → main character → central figure → hero. Repeat the key noun instead.
- "Not just X, it's Y" parallelisms — banned outright
- "From X to Y" false ranges — pick the specific case
- Em-dash overuse — see Buddha-baseline rule below (≤1 per 5 chapters for KDP-bound text)
- Boldface on every term
- Inline-header lists
- Title Case On Every Heading Word
- Decorative emojis in headings — zero anywhere in body

**Tone sins:**
- Chatbot artifacts: "I hope this helps!", "Let me know if you'd like me to expand"
- Sycophancy: "Great question!", "You're absolutely right", "You're right to flag this"
- Knowledge disclaimers: "As of my last update..."
- Excessive hedging: "could potentially possibly"
- Filler: "In order to" → "To"
- Signposting: "Let's dive in"
- Persuasive authority: "At its core", "What really matters is"

### PASS 2 — Add soul (vibe + 7 numeric gates)

**Vibe bullets (the qualitative):**
- **Have opinions.** React, don't just report.
- **Vary rhythm.** Short punchy sentence. Then a longer one that winds and finds its point three commas in.
- **Show uncertainty.** "I think", "probably", "I'm not sure but".
- **Be specific.** Not "concerning" — "the kind of thing that keeps you up at 2 AM."
- **Let some mess in.** A tangent. A half-formed thought.
- **Use "I"** when it fits.
- **Clean but not sterile.**

**Numeric gates (PASS/FAIL):**
1. **First-10-words rule.** Opening sentence contains a first-person verb, a question, OR a named human/place/year. NEVER an abstract noun-phrase opener.
2. **Burstiness target.** Every 200-word block has at least one sentence ≤6 words AND at least one ≥25 words. Sentence-length stdev ≥7 across the chapter.
3. **Hard-cut transitions.** At least one paragraph per page starts with a single-word transition: But. Still. Anyway. Look. Here's the thing.
4. **Concrete-noun density.** Every paragraph contains at least one of: proper noun, year, body part, household object, food, weather, brand name. If a paragraph could survive without one concrete noun, rewrite.
5. **Italics/caps prosody.** At least one mid-sentence italicized OR ALL-CAPS word per ~500 words, used for TONE (not for defining a term).
6. **Self-interruption.** At least one parenthetical or aside per 400 words that adds personality, not information.
7. **Ending beat.** Final sentence of every section is a question, a one-line image, a direct address, OR a fragment. Never starts with: Ultimately, In essence, At the end of the day, In conclusion.

**The 10 moves an exemplar manuscript actually does (promote to REQUIRED):**
1. Open inside a concrete physical scene, no thesis statement.
2. Repeat the key noun instead of synonym-cycling ("the app does not know" 5× in 3 lines).
3. Anchor each chapter with one named teacher + book + year (Trungpa 1973, Joko Beck *Everyday Zen*).
4. Specific years on claims — average 3+ per chapter (77 instances across 25 chapters).
5. Brand names in the open (Calm, Headspace, Instagram, Black Friday — not "a meditation app"). 37 named brands across the book.
6. Anaphoric noun stacks ("The body. The chair. The feet on the floor.").
7. One italicized concept per chapter (*spiritual materialism*, *don't refresh*) — surgical, not decorative.
8. Body-locating self-correction ("for about two weeks… and then I picked up the phone").
9. End the chapter on a flat physical detail, not a feeling ("Stand up. Go to bed.").
10. Single-word paragraphs. "Good." "No." "Stop."

**Personal-experience stamp** (Russian and English): At least once per chapter, drop a "personal receipt" right after the hardest claim. Variants: "I checked." / "I tested it." / "I lived this one." / "I have the receipt." / "I burned a year on this." / "I did the math." / "I tracked it for ninety days." Russian: `Я проверил.` / `Я попробовал.` / `Я лично прошёл.` / `Сам испытал.` / `На своей шкуре прочувствовал.` / `Я тестировал на себе.` AI rarely produces these naturally; their presence is a near-deterministic human signal.

**Mock-clinical → vernacular punchline structure** (≥1 per chapter): Set up a sentence in clinical/anatomical/physiological register, land the punchline in vernacular. The contrast IS the punch. Russian: *"Контринсулярные гормоны... это ТЫ БЛОКИРУЕШЬ десятой пиццей."* English: "Your insulin does not block fat oxidation. *You* are the bug, with the tenth slice of pizza."

**Source-traced debunking** (every cited scientist): Name the actual scientist + actual paper + actual mismatch. Not "research suggests" — "Ohsumi studied autophagy in yeast cells, not diets; he personally refuted the IF connection." Name-only without trace is the AI pattern.

---

## PASS 3 — Manuscript-level audit (book-length only)

Pass 1 + 2 are paragraph-local. Books fail at the document level. Run once when chapters are stitched, before KDP upload.

**Five mechanical checks (each is ~5 lines of Python):**
1. **Per-chapter sentence-length variance.** AI hovers at the same 15-25 word mean across all chapters; humans vary. Target: variance of chapter means ≥1.5 words.
2. **Opening-move distribution.** Tag each chapter's first move (anecdote / question / scene / direct claim / quote / data / second-person command / fragment). Fail if >60% of chapters share one move. Quota: max 5 chapters per move-type across 25.
3. **N-gram phrase frequency across the whole manuscript.** Any 3+ word phrase appearing >8× is a fingerprint. Top 10 over-frequent phrases get a rewrite pass.
4. **Last-paragraph cosine similarity** (TF-IDF). If all chapter closers cluster too tightly, flatten. Even Buddha's "Three things" closer was deliberately broken in 1 of 25 chapters.
5. **Per-chapter sentiment + certainty-marker variance.** AI is emotionally stationary; humans get tired / mad / unsure mid-draft. Variance near zero = fingerprint.

**Ugly chapter quota:** out of N chapters, plan 2-3 deliberately rough — one short and clipped (≤700 words like Buddha Ch 25), one long and winding, one with a real unresolved grudge.

**Release cadence rule:** never upload two books of the same series within 7-10 days. Amazon weights submission velocity.

---

## Quantitative gates (numbers, not vibes)

Run before declaring done. Convert "this feels human" into PASS/FAIL.

| Gate | Human range | AI range | Action |
|---|---|---|---|
| Perplexity (GPTZero) | ≥85 | 20–30 | Reject if <60 on any 3-paragraph sample |
| Burstiness (GPTZero) | 0.6–1.2 | 0.2–0.4 | Reject if <0.5 manuscript-level |
| Sentence-length stdev | ≥7 words | 2–4 words | Reject if <5 chapter-level |
| ADJ+NOUN bigram ratio | 4–7% | 8–14% | Reject if >8% |
| Passive-voice ratio | 8–15% | 18–30% | Reject if >12% |
| Hapax legomena rate | 40–55% | 25–40% | Reject if <42% |
| Punctuation entropy (Shannon) | ≥1.8 bits | <1.4 | Reject if <1.6 |
| Comma:period ratio | 1.2–2.5 | 1.4–1.8 uniform | Reject if >2.2 or semicolons >1/500 words |
| Originality.ai score | <20% AI | ≥40% AI | Reject if >25% |
| gzip compression delta | -2% to +5% vs source | +5% to +20% better | Reject if humanized text compresses BETTER than original |

Sources: GPTZero published methodology; StyloAI (arxiv 2405.10129); DependencyAI (arxiv 2602.15514).

---

## an exemplar manuscript baseline (overrides earlier rules where they conflict)

Counted from the only shipped, KDP-approved manuscript. These supersede generic rules elsewhere in this file.

- **Em dashes: 5 total across 25 chapters.** Cap is **1 per ~5 chapters**, NOT "max 2 per chapter" and NOT "use commas or periods when they work." Treat em-dashes as nearly banned for KDP-bound text.
- **Profanity rule REMOVED.** Buddha shipped with **0 fucks, 1 "ass".** The off-register signal is brand names, Russianisms, technical jargon — NOT profanity. Use profanity only when the register is already loose (Havrilesky-class, anti-work titles).
- **24 of 25 chapters use the "Three things... and not a fourth" closer; one chapter (25) deliberately breaks it.** The discipline is the joke. Always plan one chapter that breaks the template.

---

## Per-model fingerprints

Each major LLM leaves a distinct signature that survives generic vocabulary scrubs.

### Claude 4.x / 4.5 / 4.7 (the author's primary — highest priority)
- **Em-dash density 1.0–1.3 per 100 words** (vs <0.1 human). Drop to ≤0.2 per 100 words.
- **Hard-banned phrases:** "Let me X", "I'd be happy to help with that", "You're absolutely right", "It's worth noting that", "While this may vary", "That said", "To be fair", "I should note", "Generally speaking".
- **Sycophancy reflex** — search and destroy: "You're right to flag this", "Great point", "Excellent question".
- **Markdown over-structuring** — no bold-term-colon-explanation lists in prose.
- **Long flowing sentences with multiple subordinate clauses** — Claude's signature shape.

### GPT-4o / GPT-5 / GPT-5.1
- **Triadic rule-of-three** lists — kill or break to 2 / 4.
- **"Not just X — it's Y"** parallelism — banned outright.
- **2025-26 era vocabulary:** align with, enhance, fostering, highlighting, showcasing (replacing the dead delve/tapestry cluster).
- **GPT-5.1 has actively suppressed em-dashes** — em-dash density is now a Claude-vs-GPT discriminator.
- **Business-email openers:** "I hope this message finds you well", "leverage", "streamline", "ensure".

### Gemini 2/3
- **Numbered lists + uniform declarative sentences.**
- **Heavier colon/semicolon use; shorter, more direct sentences.**
- **SynthID watermark** embedded server-side — token-distribution bias survives paraphrase. For high-stakes work, retype the final sentence-by-sentence.
- **Hardest to detect by 2026 tools** — if the user ever needs cross-model laundering (short marketing copy only), launder THROUGH Gemini, NEVER through GPT.

### Detection mode
Tag input with `[CLAUDE]` / `[GPT]` / `[GEMINI]` at top to enable per-model overrides.

### GPT-locked voice drift signatures (the specific failures when LLMs try this voice)
From audit of three GPT-drafted English manuscripts at `C:\Users\A\Desktop\locked voice-Originals\`. Hard ban in any chapter, marketing copy, or social post claiming this voice:
1. **Three-strand "It's not X. It's Y." poetry triples.** Cap: zero per chapter. GPT averages 6-12.
2. **"Welcome to the [movement / rebellion / tribe / new you]" closer.** Hard ban.
3. **Emoji bullets at section headers** (🔥📕⚡🧱💀⚔️🎯👉). Hard ban anywhere.
4. **"Mantra: Say this every morning..."** Hard ban. The voice does not give mantras.
5. **"Spoiler:" / "Plot twist:" / "HAHAHAHA. That's adorable." / "Mic drop. 🎤"** Hard ban.
6. **Cooked metaphor parade** — 2-3 metaphors in one paragraph. Cap: 1 metaphor per paragraph, must earn the punch.
7. **Bullet-list as default mode.** Cap: 1 bullet block per chapter.
8. **Identity-flattering reader-naming** ("magnificent humans", "fellow warriors", "future plant-powered beasts"). Hard ban. Use affectionate-mocking nicknames instead.
9. **Cheerful-coach baseline.** The voice baseline is cynical-deadpan. If a paragraph reads cheerful, rewrite.
10. **Source-citation without trace** — naming Ohsumi or Kahneman or Sapolsky without naming the actual paper + the mismatch. Hard ban.

---

## Language-specific rules

### Russian (the deepest section — Russian is the author's native and the voice ancestor's source)

**Idiom density target: ≥3 native idioms per 1000 words.** AI Russian is grammatically correct but idiom-empty. The Brin (redacted) original has 8-12 untranslatable idioms per page. Without them the text reads as translated-from-English even when written in Russian.

High-yield idiom bank (use, don't translate literally):

| Idiom | Literal | Real meaning |
|---|---|---|
| `поздно пить Боржоми` | too late to drink Borjomi | the damage is done |
| `хрен там плавал` | a dick floated there | hard luck, no way |
| `лохматить бабушку` / `лохматить метод` | mess up Grandma / mess up the method | argue uselessly / try variants |
| `одно-хуйственная` (vulgar) | one-fuckstone (effective) | equally crappy / equally good |
| `на хрена` (mild) | for what dick | what the hell for |
| `съебывать` (vulgar) | (slang for) running away | bailing on commitments |
| `пизданулся` (vulgar) | (slang for) lost the plot | went insane |
| `дешево и сердито` | cheap and angry | cheap and effective |
| `мы тут все умные` | we are all clever here | sarcastic acknowledgment |
| `как два пальца обоссать` | like pissing on two fingers | extremely easy |
| `по три раза в день` | three times a day | habitually, addictively |
| `куда ни плюнь` | wherever you spit | everywhere you look |
| `на пальцах объяснить` | explain on fingers | dumb it down |
| `катетер реальности` | catheter of reality | a hard wake-up call (Brin's coinage, reusable) |

**Profanity creative-typography.** Humans censor with `@`, `*`, or partial omission. AI cleans profanity OR uses the full word — both signals. Examples from the Brin original: `съебыв@емся`, `пизд@нулся`, `х*йственная`, `хуйнюшечка` (diminutive — kept in full because the diminutive softens). The censoring choice IS the human signal. (For Buddha-at-2-AM-clean tier: zero profanity even softened. Russian editions of looser-register books can use it.)

**Banned phrases (cap ≤3 per 1000 words):**

| Phrase | Why ban |
|---|---|
| `является` (as connector verb) | Wikipedia construction; humans use `–` or active verb |
| `представляет собой` | textbook AI Russian |
| `при этом` | discourse marker AI overuses 5-10× |
| `более того` | same |
| `стоит отметить` | direct ChatGPT signature |
| `важно понимать` | same |
| `в современном мире` | translated from "in today's world" |
| `в первую очередь` (as opener) | bureaucratic; humans drop or invert |
| `на сегодняшний день` | translated; humans say `сегодня` |
| `необходимо учитывать` | textbook |
| `с одной стороны... с другой стороны` | three-part-balance AI tell |
| `достаточно эффективный` (hedge) | AI hedges; humans commit |
| `тем не менее` | overused by AI 4×; humans use `но` |
| `в связи с этим` | textbook |
| `способствует` | AI verb; use `помогает` or active verb |
| `функционирует` | AI verb; use `работает` |
| `данный, указанный, вышеуказанный, настоящий, подобный` (канцелярит демонстративы) | use `этот / тот / такой` or delete |
| `важно отметить, что` / `важно понимать, что` / `стоит подчеркнуть` / `следует учитывать` / `нельзя не заметить` / `не секрет, что` | hedge-stack openers — delete wrapper, keep claim |
| `осуществление, реализация, внедрение, оптимизация, функционирование, обеспечение` (nominalization stack) | convert to verbs |
| `не просто X, а Y` / `не только X, но и Y` / `это не X — это Y` (negative parallelism) | state directly |
| `ключевой, важнейший, комплексный, инновационный, эффективный, уникальный, всесторонний` (inflator adjectives) | cut |
| `давайте рассмотрим, давайте разберёмся, перейдём к, обратимся к, подводя итог, таким образом` (meta-signposting) | delete |
| `рад помочь, отличный вопрос, надеюсь, это будет полезно, если у вас остались вопросы` (chatbot pleasantries) | delete |

**Participle phrases (причастные обороты): ≤1 per sentence, ≤2 per paragraph.** Beyond that = AI Wikipedia voice. AI Russian example: *"Исследование, проведённое в 2024 году учёными из Стэнфордского университета, изучавшими..."*. Human rewrite: *"Стэнфордское исследование 2024 года изучало интервальное голодание. Показатели глюкозы упали."* Russian humans break sentences; AI builds them.

**Named Russian brands: ≥5 per chapter.** Ашан / Перекрёсток / Магнит / Пятёрочка / Дикси / Лента / ВкусВилл / HH.ru / Telegram / Яндекс.Такси / Тинькофф / ЛитРес / Боржоми. The Ашан rule: specific brand > generic noun, every time.

Cross-reference for translating English brand mentions to Russian editions:
- Costco → Ашан / Метро / Перекрёсток
- Trader Joe's → ВкусВилл
- Whole Foods → Азбука Вкуса
- Walmart → Магнит / Пятёрочка
- Starbucks → Шоколадница / Кофемания
- Slack → Telegram (default)
- LinkedIn → HH.ru
- Instagram → ВКонтакте / Telegram-канал
- Tinder → Mamba / Badoo
- Uber → Яндекс.Такси
- Audible → ЛитРес.Аудио / MyBook

**Em-dash also flags in RU** (Text.ru and Etxt both detect it) — same rule as EN: ≤1 per 5 chapters for KDP-bound text.

**Russian KDP humanization runs BEFORE final TTS** — F5-TTS Misha24-10 amplifies канцелярит rhythm. Scrub before voicing.

**Colloquial markers when register allows:** "ну", "короче", "да и в общем" — useful, not banned.

### English

- **US/UK/International — pick one and hold the line.** Mixing is an AI tell.
- **Contract aggressively:** don't, can't, isn't. AI overuses full forms.
- **Cut `in order to`, `due to the fact that`, `with regard to`.**

**English banned phrases (in addition to the universal banned vocabulary above):**

| Phrase | Why ban |
|---|---|
| "in today's [fast-paced / digital / increasingly] world" | textbook AI |
| "let's get one thing straight" | GPT motivational opener |
| "here's the thing" | overused by AI 5-8× vs. humans |
| "the truth is" (without committing to next-sentence truth) | hedging without follow-through |
| "spoiler:" / "plot twist:" | Reddit-trained AI register |
| "PSA:" / "TL;DR:" | not in this voice register |
| "let me explain" / "let me break this down" | LLM chatbot opener |
| "(though, hey, [aside])" | cheerleading aside, characteristic of GPT |
| "but here's the kicker" | clickbait drift |
| "the bottom line is" | wrap-up tell |
| "stay tuned" | newsletter-bro voice |
| "without further ado" | textbook |
| "in conclusion" / "in summary" / "to wrap up" | school essay |
| "circle back" / "level up" / "unlock" (metaphorical) | corporate-LinkedIn drift |
| "absolutely crushing it" | influencer |
| "literally [adjective]" (as intensifier, when not literally meant) | GPT-tic |
| "I cannot stress enough" | textbook hedge |
| "in my honest opinion" / "to be completely honest" | AI politeness ritual |
| "this is huge" / "this is massive" / "this is everything" | hyperbole AI overuses |

**English asymmetric-rhythm rule.** AI English writes in even cadence (12-18 words per sentence, monotonously). Human locked voice writes in heavily variable rhythm. Target per paragraph: at least one sentence under 8 words AND one over 25 words. At least one sentence fragment per chapter. At least one one-line paragraph as punctuation per page. AI text: mean ≈ 15, stdev ≈ 4. Human locked voice: mean ≈ 14, stdev ≥ 10.

**English self-correction signals: ≥1 per chapter.** Humans correct themselves mid-paragraph; AI does not unless prompted. Patterns to inject: "Actually, that's not quite right." / "Wait — I want to be careful here." / "Let me restate that." / "I'm overstating. The real version is..." / "That's the cleanest version of it. The messy version is..." / "I almost wrote [X]. The truer thing is [Y]."

**Affectionate-mocking reader nicknames (the user canon): ≥1 per chapter.** Never punch down at named real individuals; always punch at the pattern the reader fits. Identity-flattering reader-naming ("magnificent humans", "fellow warriors") is the GPT anti-pattern — hard ban. The clean canon:
- "the average Slack-warrior"
- "the recovering 5 AM Club graduate"
- "the LinkedIn-philosopher"
- "the part of you that bought the third planner"
- "the version of you reading this at 11:47 PM in the kitchen"
- "you with seven productivity-app subscriptions"
- "the gym-bro with three protein subscriptions"
- "the partner who got too good at the morning routine"
- "the 41-year-old who Googled their high-school name at 11:47"

**Named brands + cultural anchors: ≥4 per page.** LinkedIn, Slack, Notion, Whoop, Oura, Costco, Audible, Substack, Spotify, Apple Watch, MyFitnessPal, AirPods, Headspace, Calm, Tinder, the named coffee shop, the named gym, the named cathedral. AI English defaults to generic ("a coffee shop," "in the morning," "a few years ago"). Specificity is the cheapest human signal.

**Specific time-stamps: ≥3 per chapter, ≥1 in the chapter opener.** 11:47 PM / 4:47 AM Tuesday / October 7:43 AM. AI defaults to "in the morning."

### German

- **Banned vocab:** Landschaft, eintauchen, Reise (metaphorical), nahtlos, robust, gewährleisten, Wandteppich, facettenreich, darüber hinaus, letztendlich.
- **Banned phrases:** "Es ist wichtig zu beachten, dass…", "In der heutigen schnelllebigen Welt…", "lassen Sie uns eintauchen", "ein tieferes Verständnis erlangen".
- **Compound words OK if natural; flag invented compounds (AI-built).**
- **Subjunctive II (würde + infinitive) overuse = AI tell.**
- **Nominalstil overdose** is the dominant tell — AI stacks noun chains ("die Durchführung der Implementierung der Optimierung"). Native German alternates verb/noun.
- **Translation calques to fix:** "tief eintauchen" → `sich eingehend befassen`. "Spielveränderer" → `Wendepunkt`. "erreichen Sie uns" → `melden Sie sich`.

### Spanish (covers .es + .com.mx + LATAM)

- **Banned vocab:** sumergirse, panorama, tapiz, desbloquear, aprovechar, robusto, fluido, fomentar, garantizar, fundamental, crucial.
- **Banned phrases:** "Es importante destacar que…", "En el mundo actual…", "hoy en día", "un mundo de posibilidades".
- **Gerund cycling** ("explorando, analizando, desarrollando…") — Plagius flags >3 per 200 words.
- **Pick ONE register:** Castilian (vosotros) or LATAM (ustedes) — declare per market.
- **Calques:** "Let's dive in" → `vamos al grano`. "Game-changer" → `punto de inflexión`.

### French

- **Banned vocab:** plonger, paysage, tapisserie, naviguer, exploiter, robuste, fluide, crucial, primordial, davantage, notamment.
- **Banned phrases:** "Il est important de noter que…", "Il convient de souligner que…", "à l'ère du numérique", "force est de constater".
- **`il est` + adj + `de` + infinitive** stacked is the structural tell — native French prefers active subject.
- **Smart quotes:** French uses `« guillemets »` with nbsp — AI ships ASCII `"`.

### Portuguese-BR

- **Banned vocab:** mergulhar, panorama, tapeçaria, desbloquear, aproveitar, robusto, contínuo, crucial, fundamental, abrangente.
- **Banned phrases:** "É importante ressaltar que…", "No mundo de hoje…", "um leque de possibilidades".
- **Gerundismo** ("vou estar enviando, vou estar fazendo") — call-center Portuguese, hated in published prose.
- **PT-BR vs PT-PT discipline:** declare explicitly.

### Japanese

- **Banned grammar:** 〜について excess, 〜に関して, 重要である (use 大切), 〜化 noun-suffix abuse (最適化 etc cycled), さらに, 一方で, つまり, 結論として, 〜を行う.
- **Banned phrases:** 〜することが重要です, 今日の急速に変化する世界では, 〜の世界に飛び込んでみましょう.
- **〜である調 / 〜です・ます調 mixing** within one document = AI tell.
- **Sentence-length variance must be ≥15%** — AI clusters at 30-40 chars; natives vary 8-60.
- **Calques:** "Let's dive in" → 早速見ていきましょう. "Game-changer" → 転換点.

### Italian

- **Banned vocab:** immergersi, panorama, arazzo, sbloccare, sfruttare, robusto, senza soluzione di continuità, cruciale, fondamentale, in definitiva, inoltre, altresì.
- **Banned phrases:** "È importante sottolineare che…", "immergiamoci in…", "al giorno d'oggi", "un'ampia gamma di".
- **Subjunctive overuse + `che` chains** — 3+ che-clauses stacked = AI; natives break with periods.
- **Accent direction:** `perchè` vs correct `perché` — AI mixes both.

---

## Voice anchors — operationalized

Each locked voice voice anchor has measurable, prompt-injectable patterns.

### Mary Karr (memoir)
- Body-part / object as first noun in ~60% of openings — never a feeling word.
- Code-switch within 3 sentences — literate diction + Texan vernacular in the same paragraph.
- Fragment-as-punchline ending ~1 in 4 paragraphs.
- **Uses:** hollering, fixing-to, the dark wad of something, sumbitch.
- **Never uses:** navigate, journey, profound, embrace, ultimately, leverage, complexity.

### Anne Lamott (essay)
- First-person catastrophe → universal "you" pivot within 2 sentences.
- Triads with one absurd member ("prayer, coffee, and one good Pop-Tart").
- Sacred/profane collision in one sentence.
- **Uses:** shitty first draft, KFKD radio, butt in chair, gnarly, the broccoli.
- **Never uses:** optimize, framework, mindset, intentional, holistic, authentic, lean into.

### Heather Havrilesky (advice column)
- And-anaphora climbing — 4-7 consecutive sentences starting with "And" in the final third.
- Italicized single words mid-paragraph (*this*, *that*, *now*) — never whole phrases.
- Endearment-caps salutation ("DARLING DROWNING", "SWEET PEA") — structurally non-negotiable for the column form.
- **Uses:** glitter-encrusted, your one wild life, demonic, dumb animal joy.
- **Never uses:** actionable, takeaway, key insight, at the end of the day.

### Caitlin Doughty (death-positive)
- Technical-term in cozy register — clinical morgue vocabulary inside warm domestic sentence.
- Gruesome-detail → 6-9 word deadpan landing.
- First-person idiot-narrator pose — never the authority.
- **Uses:** corpse (never "deceased"), shaved the old man, slop, goo.
- **Never uses:** passed away, loved one, celebrate the life, transition (verb).

**Operational rule:** when a paragraph reads off, open Karr or Havrilesky at random for 2 minutes before continuing.

---

## Genre-specific rules

Five distinct genres in the author's catalog need genre-specific rules beyond the generic register categories.

### the publication series (argumentative critique)
- **Banned:** fake-balanced concession pivot ("To be fair, X does have a point. However…"); closing-the-loop sentences ("And that's why X's framework deserves scrutiny").
- **Required:** one personal financial/time/credibility loss per chapter (amount + year + what it cost); one paragraph where the writer admits the subject was right about something without walking it back; direct first-name address ("Tony, this is where you lose me").
- **Exemplar:** Cory Doctorow, *Chokepoint Capitalism*.

### Spirituality / philosophy (an exemplar manuscript, an exemplar manuscript)
- **Banned:** "wisdom traditions" framing; sage-character omniscience; universal-translation flattening (dukkha → "stress").
- **Required:** one untranslated term per chapter, used in context (don't gloss); the teacher does something embodied and unflattering; one specific 2 AM detail dating the writing.
- **Exemplar:** Anne Lamott, *Traveling Mercies*.

### Anti-work / lifestyle critique (Enlightened Don't…)
- **Banned:** hustle-culture quote-Frankenstein; solution-shaped paragraph; "in our always-on culture" / "in today's fast-paced world".
- **Required:** refuse to end any chapter with an action list; name a specific company / founder / product (not "Big Tech"); admit complicity once per chapter.
- **Exemplar:** Jenny Odell, *How to Do Nothing*.

### Epistolary memoir (In The Drawer)
- **Banned:** calendar-perfect date headers; reflection-to-incident ratio inverted; universal salutations ("Dear reader").
- **Required:** irregular date intervals with at least 2 acknowledged gaps; 60/40 incident-to-reflection ratio; named recipient with shifting relationship across letters.
- **Exemplar:** Mary-Louise Parker, *Dear Mr. You*.

### Argument-driven nonfiction (948 Business Books, Six Hours)
- **Banned:** round-number sample sizes ("over 1000 books"); meta-commentary opener ("What I learned from reading 948…"); synonym cycling of the genre name.
- **Required:** odd-numbered specificity (948, not 1000); cite 5+ books by exact title + year per chapter; one book the writer agrees with, named, with the specific page.
- **Exemplar:** Will Storr, *The Status Game*.

---

## Marketing copy by format

Each format has different scanners and audience.

### Amazon KDP book description (≤4000 chars)
- **Banned in headline position:** Unlock / Unleash / Discover / "Whether you're [X], [Y], or [Z]" / "In this groundbreaking guide".
- **Open with:** one concrete sentence (number + noun) or one specific scene. Never a rhetorical question.

### Vella / BookBub hook (200-char + 100-word blurb)
- **Banned:** "must confront", "world-shattering", ellipsis cliffhangers.

### Print paperback back cover (~200 words)
- **Banned:** "masterful", "tour de force", "unputdownable", magazine-blurb voice.

### Author Central "About"
- **Banned:** third-person CV stack, "passionate about", "transforming lives".
- **Use:** first person. Reedsy 2025 A/B data: 18% higher follow-rate.

### Email newsletter
- **Banned subjects:** "Quick question", "Hope this finds you well".
- **Banned openers:** "Hope you're well!", "Quick one for you today".

### Cold outreach DM (the Tatiana Becker failure mode)
- **Banned:** em dashes anywhere, "I came across your profile", "would love to connect", "without losing the human feel", "the kind of X I gravitate toward".
- **Rule:** max 1 comma, zero em-dashes, one specific feed-detail, no "let me know if interested" closer.
- **No recovery move:** if rejected as AI on read 1, do NOT explain. Honest recovery still fails.

### Tweet / BookTok caption (≤280 chars or ~30s)
- **Banned:** "POV:", "Nobody talks about this", "This changed my life", hashtag stacks.
- **Use:** lowercase opener, zero hashtags, one off-rhythm specific.

### Landing page hero + CTA
- **Banned:** "Ultimate", "All-in-one", "Get Started" (CTA).
- **Use:** one verifiable fact (number + noun), zero adjectives, button uses the product verb.

---

## Editor "trained-eye" verification checklist

Before submitting any manuscript, confirm it HAS (boxes empty = reads as AI to a trained editor regardless of algorithm score):

- [ ] One character / narrator who is wrong about themselves for the first 60% — and the text knows it.
- [ ] At least 3 lived-in specifics per chapter that only the user could write (place name, brand, date, smell, dead relative's phrase).
- [ ] One joke that doesn't quite work — and is kept anyway.
- [ ] One paragraph that breaks shape — a one-liner, or a 200-word run-on — every ~1500 words.
- [ ] One subtextual exchange where the narrator discusses A while clearly meaning B.
- [ ] One asymmetric chapter — shorter, angrier, or quieter than its neighbors (Buddha Ch 25).
- [ ] One factual aside revealing what the writer was *doing* while writing.
- [ ] One unresolved grudge — a person, a job, a city the narrator can't be fair about.
- [ ] One punctuation quirk consistent enough to be a fingerprint.
- [ ] At least one "almost-right" metaphor that betrays the narrator's bias rather than describes accurately.

---

## Pre-KDP submission protocol

Amazon's 2026 stack reads metadata + velocity + cross-book uniformity, not just text.

**Metadata fingerprint sanitization:**
- KDP reads `.docx` / `.epub` XML edit-history. A 100K-word manuscript with 14 minutes of editing time = instant flag.
- **Required:** open final manuscript in Word, do a real ≥30-minute revision pass with track-changes so the XML shows organic edit time. OR strip metadata before upload.
- Verify all factual citations exist (Google Scholar each one). A made-up Stanford study = fastest termination path.

**Velocity rules (the user is in one-strike state since 2026-04-27):**
- One book per 14 days minimum.
- Never batch-upload 5 the series titles same week. Space 7-10 days minimum.
- Long-form (≥10,000 words) at <1/month is the safe envelope.

**Anti-paraphraser-tool rule:**
Pangram-class detectors (Amazon's likely vendor) specifically train against QuillBot / Undetectable.ai / StealthGPT / Phrasly. Tool-laundered text scores WORSE than raw GPT against these. **Do not use commercial humanizer tools.** Use this skill + manual rewrite + optional EN→RU→EN round-trip.

**Self-screening before upload:**
1. Originality.ai → target <20% AI.
2. GPTZero → target >85 perplexity, >0.7 burstiness.
3. Paste 3 random paragraphs into GPTZero. If any scores <40, rewrite.
4. Verify every cited fact.

---

## Cross-language audit pipeline (greppable patterns)

Run these greps before accepting any draft.

### Russian audit

```bash
# AI tells (cap: ≤3 per 1000 words)
grep -E "является|представляет собой|при этом|более того|стоит отметить|важно понимать|в современном мире|в первую очередь|на сегодняшний день|необходимо учитывать|тем не менее|способствует|функционирует" file.txt | wc -l

# Idiom density (floor: ≥3 per 1000 words)
grep -E "поздно пить|хрен там|на хрена|дешево и сердито|катетер реальности|на пальцах|куда ни плюнь" file.txt | wc -l

# "I checked" stamps (floor: ≥1 per chapter)
grep -E "Я проверил|Я попробовал|Я лично|Сам испытал|На своей шкуре|Я тестировал" file.txt | wc -l

# Named-brand density (floor: ≥5 per chapter)
grep -E "Ашан|Перекрёсток|Магнит|Пятёрочка|Дикси|Лента|ВкусВилл|Боржоми|Telegram|HH\.ru|ЛитРес|Яндекс|Тинькофф" file.txt | wc -l
```

### English audit

```bash
# Three-strand poetry triples (cap: 0)
grep -E "It's not [A-Za-z]+\. It's [A-Za-z]+\. It's not" file.txt | wc -l

# Emoji presence (cap: 0)
grep -P "[\x{1F300}-\x{1F9FF}]|[\x{2600}-\x{27BF}]" file.txt | wc -l

# Banned phrases (cap: 0)
grep -Ei "in today's (fast-paced|digital) world|let's get one thing straight|here's the thing|here's the kicker|the bottom line|stay tuned|at the end of the day|in conclusion|circle back|level up|unlock" file.txt | wc -l

# "I checked" stamps (floor: ≥1 per chapter)
grep -Ei "I checked\.|I tested it\.|I lived this|I have the receipt|I tracked it|I burned a year" file.txt | wc -l

# Named-brand density (floor: ≥5 per chapter)
grep -Ei "LinkedIn|Slack|Notion|Whoop|Oura|Audible|Substack|Costco|Trader Joe's|Apple Watch|MyFitnessPal|AirPods|Spotify|Headspace|Calm|Tinder" file.txt | wc -l

# Time-stamp anchors (floor: ≥3 per chapter)
grep -E "\b[0-9]{1,2}:[0-9]{2} ?(AM|PM|am|pm)?\b" file.txt | wc -l
```

A chapter that fails any FLOOR or exceeds any CAP needs a humanizer pass before KDP submission.

---

## Drafting-agent prompt fragment (use verbatim in any agent prompt)

> The voice is calm-burnt-out, never cheerful-coach. Every chapter: ≥1 mock-clinical-to-vernacular contrast sentence; ≥1 "I checked / Я проверил" personal-experience stamp after the hardest claim; ≥1 source-traced citation (scientist + actual paper + actual mismatch); ≥1 affectionate-mocking reader nickname (never identity-flattery); ≥1 self-correction phrase; ≥1 sentence fragment; ≥1 one-line paragraph. Named brands ≥5, specific years ≥3, time-stamps ≥1. Em-dashes ≤1 per 5 chapters. Zero emoji. Zero three-strand "not X but Y" triples. Zero "Welcome to the [movement]" closers. Zero "Spoiler:" / "Plot twist:" / "Mic drop." Zero mantras. Anatomical specificity over abstract energy-talk. One bullet block per chapter max; otherwise prose. The reader is not stupid — the reader is tired. The narrator is one of them, not above them.
>
> **Russian-only:** drop ≥3 native idioms per page. Use `@`/`*` censoring for any profanity. Participle phrases ≤1 per sentence. Brand names from RU list (Ашан/Перекрёсток/HH.ru/Telegram/Яндекс/ВкусВилл), never generic nouns. Banned phrases ≤3 per 1000w (является/представляет собой/стоит отметить/при этом).
>
> **English-only:** specific brand names from EN list (LinkedIn/Slack/Whoop/Costco/Audible/Substack). Asymmetric rhythm: ≥1 sentence under 8 words AND ≥1 over 25 words per paragraph. Source-trace required for every named scientist. Buddha-at-2-AM clean tier: zero profanity even softened.

---

## Optional: humanize_pass2.py (adversarial loop, local)

For high-stakes KDP marketing copy ≤500 words — not book-length. Located at `humanize_pass2.py` in this skill folder.

Workflow: paraphrase → score with local Binoculars/Ghostbuster + the 10-gate stylometric table above → if any 2+ gates fail, re-prompt with the failing metric's numeric target injected. Uses Qwen3-4B + LoRA as the paraphraser (runs on RTX 5080).

**Explicitly rejected techniques (do not use):**
- Homoglyph / zero-width character injection — modern detectors pre-filter, KDP flags, breaks audiobook TTS.
- Pure laundering through GPT-5 — its triadic register is the most-detected by 2026 tools.

---

## Output format

Return ONLY the rewritten text. No preamble. No "Here's the humanized version:". No commentary. No before/after diff unless explicitly asked.

If asked to explain changes, return diff format:
```
- "leveraged the comprehensive landscape"
+ "used everything available"
[reason: banned vocab × 3]
```

---

## Pairs with

- **locked voice voice spec:** `~/Desktop/Books/_new_concepts/_shared/VEGAN_BADASS_VOICE.md` — the writing rules (this skill is the detection / scrubbing rules). Run de-ai first, then enforce locked voice voice rules.
- **HUMANIZER_STYLE_GUIDE.md:** `~/Desktop/Books/_new_concepts/_shared/HUMANIZER_STYLE_GUIDE.md` — the 461-line deep operational reference.
- **book-creation skill:** Phase 6 (humanization) calls this skill.
- **the publication series prompt:** feed each chapter through de-ai before publishing.

## Files in this skill

- `SKILL.md` (this file) — canonical workflow
- `humanize_pass2.py` — optional adversarial loop for short-form marketing copy
- `humanize_pass2_README.md` — install + usage docs
- `system.md` — original glebis pipeline reference (deeper diagnostic categories)
- `skill.sh` — runnable helper script
- `skill.yaml` — original glebis metadata
- `SKILL_history_2026_05_13.md` — frozen snapshot of the pre-consolidation 859-line version (v1+v2+v3 dated blocks) for reference

Sources: https://github.com/glebis/claude-skills/tree/main/de-ai (technique) + the author's Humanizer Prompt (voice rules, 2026-04-23) + Buddha-at-2-AM shipped-manuscript audit (2026-05-09) + (redacted) Russian-original voice analysis (2026-05-13).
