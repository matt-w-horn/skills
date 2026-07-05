# AI Writing Tropes to Avoid

Reference catalog for the writing skill. Source: [tropes.fyi](https://tropes.fyi) by [ossama.is](https://ossama.is).

How to use this catalog: when drafting, steer around these patterns from the start. When editing, hunt for clusters. One instance of any trope might be fine; several different tropes in one piece, or one trope repeated, is the giveaway. Each entry shows the pattern, real examples of it, and the fix. The "Quick hunt list" at the end gives searchable strings for an editing pass.

---

## Word Choice

### "Quietly" and Other Magic Adverbs

Overuse of "quietly" and similar adverbs to convey subtle importance or understated power. AI reaches for these adverbs to make mundane descriptions feel significant. Also includes: "deeply", "fundamentally", "remarkably", "arguably".

**Avoid patterns like:**
- "quietly orchestrating workflows, decisions, and interactions"
- "the one that quietly suffocates everything else"
- "a quiet intelligence behind it"

**Write instead:** Delete the adverb and state what the thing does: "it schedules the workflows and files the results." If the sentence feels flat without the adverb, the problem is the content, not the missing intensifier.

### "Delve" and Friends

Used to be the most infamous AI tell. "Delve" went from an uncommon English word to appearing in a staggering percentage of AI-generated text. Part of a family of overused AI vocabulary including "certainly", "utilize", "leverage" (as a verb), "robust", "streamline", and "harness".

**Avoid patterns like:**
- "Let's delve into the details..."
- "Delving deeper into this topic..."
- "We certainly need to leverage these robust frameworks..."

**Write instead:** Skip the lead-in and start with the first detail: "The retry logic has two bugs." Prefer the plain verb every time: "use" not "utilize", "make X faster" not "streamline X".

### "Tapestry" and "Landscape"

Overuse of ornate or grandiose nouns where simpler words would do. "Tapestry" is used to describe anything interconnected. "Landscape" is used to describe any field or domain. Other offenders: "paradigm", "synergy", "ecosystem", "framework".

**Avoid patterns like:**
- "The rich tapestry of human experience..."
- "Navigating the complex landscape of modern AI..."
- "The ever-evolving landscape of technology..."

**Write instead:** Name the actual domain: "choosing an AI vendor in 2026" instead of "navigating the complex landscape of modern AI."

### The "Serves As" Dodge

Replacing simple "is" or "are" with pompous alternatives like "serves as", "stands as", "marks", or "represents". AI avoids basic copulas because its repetition penalty pushes it toward fancier constructions (I've studied this!).

**Avoid patterns like:**
- "The building serves as a reminder of the city's heritage."
- "Gallery 825 serves as LAAA's exhibition space for contemporary art."
- "The station marks a pivotal moment in the evolution of regional transit."

**Write instead:** "The building is a reminder of the city's heritage." Or say the concrete reason it matters: "The building survived the 1906 fire; the city kept it."

---

## Sentence Structure

### Negative Parallelism

The "It's not X -- it's Y" pattern, often with an em dash. The single most commonly identified AI writing tell. Man I f*cking hate it. AI uses this to create false profundity by framing everything as a surprising reframe. One in a piece can be effective; ten in a blog post is a genuine insult to the reader. Before LLMs, people simply did not write like this at scale. Includes the causal variant "not because X, but because Y" where every explanation is framed as a surprise reveal, the em-dash dismissal "X -- not Y", and the cross-sentence reframe where the same noun is negated then repositioned: "The question isn't X. The question is Y."

**Avoid patterns like:**
- "It's not bold. It's backwards."
- "Feeding isn't nutrition. It's dialysis."
- "Half the bugs you chase aren't in your code. They're in your head."

**Write instead:** State Y directly and let it stand: "It's backwards." If the contrast genuinely matters, name who holds the X view and show why they're wrong, which is an argument rather than a pose.

### "Not X. Not Y. Just Z."

The dramatic countdown pattern. AI builds tension by negating two or more things before revealing the actual point. Creates a false sense of narrowing down to the truth.

**Avoid patterns like:**
- "Not a bug. Not a feature. A fundamental design flaw."
- "Not ten. Not fifty. Five hundred and twenty-three lint violations across 67 files."
- "not recklessly, not completely, but enough"

**Write instead:** "It's a fundamental design flaw." For the numbers case: "523 lint violations across 67 files." A specific count carries its own drama; the countdown only dilutes it.

### "The X? A Y."

Self-posed rhetorical questions answered immediately in the next sentence or clause. The model asks a question nobody was asking, then answers it for dramatic effect. Thinks this is the epitome of great writing.

**Avoid patterns like:**
- "The result? Devastating."
- "The worst part? Nobody saw it coming."
- "The scary part? This attack vector is perfect for developers."

**Write instead:** "The result was devastating." Better, show it: "Revenue fell 40% the next quarter."

### Anaphora Abuse

Repeating the same sentence opening multiple times in quick succession.

**Avoid patterns like:**
- "They assume that users will pay... They assume that developers will build... They assume that ecosystems will emerge... They assume that..."
- "They could expose... They could offer... They could provide... They could create... They could let... They could unlock..."
- "They have built engines, but not vehicles. They have built power, but not leverage. They have built walls, but not doors."

**Write instead:** Merge truly parallel points into one sentence: "They assume users will pay, developers will build, and ecosystems will emerge, and none of it has happened." Otherwise vary the openings so each sentence earns its own shape.

### Tricolon Abuse

Overuse of the rule-of-three pattern, often extended to four or five. A single tricolon is elegant; three back-to-back tricolons are a pattern recognition failure.

**Avoid patterns like:**
- "Products impress people; platforms empower them. Products solve problems; platforms create worlds. Products scale linearly; platforms scale exponentially."
- "identity, payments, compute, distribution"
- "workflows, decisions, and interactions"

**Write instead:** Keep the strongest one and cut the rest. "Products solve problems; platforms create worlds" lands harder alone than stacked with two echoes of itself.

### "It's Worth Noting"

Filler transitions that signal nothing. AI uses these phrases to introduce new points without actually connecting them to the previous argument. Also includes: "It bears mentioning", "Importantly", "Interestingly", "Notably".

**Avoid patterns like:**
- "It's worth noting that this approach has limitations."
- "Importantly, we must consider the broader implications."
- "Interestingly, this pattern repeats across industries."

**Write instead:** Delete the phrase; the sentence almost always survives: "This approach can't handle concurrent writes." If the point wasn't worth stating without the preamble, cut the whole sentence.

### Superficial Analyses

Tacking a present participle ("-ing") phrase onto the end of a sentence to inject shallow analysis that says nothing. The model attaches significance, legacy, or broader meaning to mundane facts using phrases like "highlighting its importance", "reflecting broader trends", or "contributing to the development of...".

**Avoid patterns like:**
- "contributing to the region's rich cultural heritage"
- "This etymology highlights the enduring legacy of the community's resistance and the transformative power of unity in shaping its identity."
- "underscoring its role as a dynamic hub of activity and culture"

**Write instead:** End the sentence at the fact: "The festival dates to 1932." If the significance is real, give it its own sentence with actual content in it.

### False Ranges

Using "from X to Y" constructions where X and Y aren't on any real scale. In legitimate use, "from X to Y" implies a spectrum with a meaningful middle. AI uses it as a fancy way to list two loosely related things. "From innovation to cultural transformation" -- what's in between???? Nothing!

**Avoid patterns like:**
- "From innovation to implementation to cultural transformation."
- "From the singularity of the Big Bang to the grand cosmic web."
- "From problem-solving and tool-making to scientific discovery, artistic expression, and technological innovation."

**Write instead:** Use a plain list: "it handles PDFs, spreadsheets, and images." Save "from X to Y" for real scales with a real middle: "latency ranges from 3 ms to 90 seconds."

---

## Paragraph Structure

### Short Punchy Fragments

Excessive use of very short sentences or sentence fragments as standalone paragraphs for manufactured emphasis. RLHF training has pushed models toward "writing for readability" aimed at the lowest common denominator: one thought per sentence, no mental state-keeping required. It's an inhuman style. No real person writes first drafts this way because it doesn't match how humans think or speak.

**Avoid patterns like:**
- "He published this. Openly. In a book. As a priest."
- "These weren't just products. And the software side matched. Then it professionalised. But I adapted."
- "Platforms do."

**Write instead:** Recombine into a sentence that holds the relationships: "He published this openly, in a book, while he was a priest." Save the standalone fragment for the one moment in the piece that has earned it.

### Listicle in a Trench Coat

Numbered or labeled points dressed up as continuous prose. The model writes what is essentially a listicle but wraps each point in a paragraph that starts with "The first... The second... The third..." to disguise the format. Perhaps you told it to stop generating lists and it decided to do this instead... still very common.

**Avoid patterns like:**
- "The first wall is the absence of a free, scoped API... The second wall is the lack of delegated access... The third wall is the absence of scoped permissions..."
- "The second takeaway is that... The third takeaway is that... The fourth takeaway is that..."

**Write instead:** Either own the list and use actual bullets, or write prose where each point follows from the previous one and the connective tissue does real work. The numbering scaffold is the tell; remove the scaffold or admit it's a list.

---

## Tone

### "Here's the Kicker"

False suspense transitions that promise a revelation but deliver a point that did NOT need the buildup. The model uses these phrases to manufacture drama before an otherwise unremarkable observation LOL. Also includes: "Here's the thing", "Here's where it gets interesting", "Here's what most people miss", "Here's the starting point", "Here's the deal".

**Avoid patterns like:**
- "Here's the kicker."
- "Here's the thing about AI adoption."
- "Here's where it gets interesting."

**Write instead:** Lead with the fact itself. If it's genuinely surprising, the reader will notice without a drumroll; if it isn't, the drumroll makes it worse.

### "Think of It As..."

The patronizing analogy. AI constantly reaches for "Think of it as..." or "It's like a..." to simplify concepts. The model defaults to teacher mode and assumes the reader needs a metaphor to understand anything. Often produces analogies that are less clear than the original concept.

**Avoid patterns like:**
- "Think of it like a highway system for data."
- "Think of it as a Swiss Army knife for your workflow."
- "It's like asking someone to buy a car they're only allowed to sit in while it's parked."

**Write instead:** State the mechanism plainly: "the broker holds each message until the consumer acknowledges it." Reach for an analogy only when the plain mechanism genuinely won't land, and then use it without the "think of it as" frame.

### "Imagine a World Where..."

The classic AI invitation to futurism. To sell the argument usually begins with "Imagine" followed by a list of wonderful things that will happen if the reader agrees with the premise.

**Avoid patterns like:**
- "Imagine a world where every tool you use -- your calendar, your inbox, your documents, your CRM, your code editor -- has a quiet intelligence behind it..."
- "In that world, workflows stop being collections of manual steps and start becoming orchestrations."

**Write instead:** Make the checkable claim: "with scoped API access, your calendar client could draft replies to invitations." A concrete conditional beats an invited dream.

### False Vulnerability

Simulated self-awareness or honesty that reads as performative. The model pretends to break the fourth wall or admit a bias, creating a false sense of authenticity. Real vulnerability is specific and uncomfortable; AI vulnerability is polished and risk-free!!!!

**Avoid patterns like:**
- "And yes, I'm openly in love with the platform model"
- "And yes, since we're being honest: I'm looking at you, OpenAI, Google, Anthropic, Meta"
- "This is not a rant; it's a diagnosis"

**Write instead:** Real specifics or nothing: "I shipped this exact bug twice before I understood it" works because it's checkable and costs something to admit. If an admission costs nothing, cut it.

### "The Truth Is Simple"

Asserting that something is obvious, clear or simple instead of actually proving it. If you have to tell the reader your point is clear, it very likely isn't. Also includes the dramatic reveal variant: "but none of them is the real story. The real story is..." -- claiming privileged insight while waving away everything before it.

**Avoid patterns like:**
- "The reality is simpler and less flattering"
- "History is unambiguous on this point"
- "History is clear, the metrics are clear, the examples are clear"

**Write instead:** Show the evidence and let the reader conclude it's simple. If the case really is unambiguous, two strong examples will demonstrate that better than any assertion of clarity.

### Grandiose Stakes Inflation

Everything is the most important thing ever. AI inflates the stakes of every argument to world-historical significance. A blog post about API pricing becomes a meditation on the fate of civilization.

**Avoid patterns like:**
- "This will fundamentally reshape how we think about everything."
- "will define the next era of computing"
- "something entirely new"

**Write instead:** Size the claim to the evidence: "this saves our team about an hour a week." Small true claims build more trust than large unprovable ones.

### "Let's Break This Down"

The pedagogical voice that assumes the reader needs hand-holding. AI defaults to a teacher-student dynamic even when writing for expert audiences. Also includes: "Let's unpack this", "Let's explore", "Let's dive in".

**Avoid patterns like:**
- "Let's break this down step by step."
- "Let's unpack what this really means."
- "Let's explore this idea further."

**Write instead:** Break it down without saying so: delete the announcement and start with the first piece. Structure the reader can see needs no narration.

### Vague Attributions

Attributing claims to unnamed authorities instead of being specific. AI loves to invoke "experts", "observers", "industry reports", and "several publications" without naming anyone. It also inflates the quantity of sources -- presenting what one person said as a widely held view, or writing "several publications have cited" when it means two. If you can't name the expert, you don't have a source.

**Avoid patterns like:**
- "Experts argue that this approach has significant drawbacks."
- "Industry reports suggest that adoption is accelerating."
- "Observers have cited the initiative as a turning point."

**Write instead:** Name the person and the venue: "curl's maintainer Daniel Stenberg wrote that AI-generated security reports are a denial-of-service on his time." If you can't name anyone, make the claim in your own voice or drop it.

### Invented Concept Labels

AI clusters invented compound labels that sound analytical without being grounded. It appends abstract problem-nouns (paradox, trap, creep, divide, vacuum, inversion) to domain words — "supervision paradox", "acceleration trap", "workload creep" — and uses them as if they're established, rigorously defined terms. They function as rhetorical shorthand: name a thing, skip the argument. Multiple such labels in the same piece is a strong signal of AI slop.

**Avoid patterns like:**
- "the supervision paradox"
- "the acceleration trap"
- "workload creep"

**Write instead:** Make the argument the label was standing in for: "reviewers approve more code per hour than they can actually read" instead of "the supervision paradox." Coin a term only if you define it on first use and the piece genuinely needs the shorthand.

---

## Formatting

### Em-Dash Addiction

Compulsive overuse of em dashes for dramatic pauses, parenthetical asides and pivot points. A human writer might use 2-3 per piece (and naturally); AI will use 20+.

**Avoid patterns like:**
- "The problem -- and this is the part nobody talks about -- is systemic."
- "The tinkerer spirit didn't die of natural causes -- it was bought out."
- "Not recklessly, not completely -- but enough -- enough to matter."

**Write instead:** "The problem, and nobody talks about this part, is systemic." Commas, parentheses, colons, and full stops cover nearly every case; keep the em dash for the one or two places per piece where the interruption is the point.

### Bold-First Bullets

Every bullet point or list item starts with a bolded phrase or sentence. Extremely common in Claude and ChatGPT markdown output. Almost nobody formats lists this way when writing by hand. It's a telltale sign of AI-generated documentation and blog posts AND README files (especially with emojis).

**Avoid patterns like:**
- "Every single bullet point begins with a bold keyword."
- "**Security**: Environment-based configuration with..."
- "**Performance**: Lazy loading of expensive resources..."

**Write instead:** Plain bullets that read as sentences: "configuration comes from the environment, so secrets stay out of the image." If every item really needs a label, that's a table, not a list.

### Unicode Decoration

Use of unicode arrows (->), smart/curly quotes, and other special characters that can't be easily typed on a standard keyboard. Real writers typing in a text editor produce straight quotes and -> or =>. Claude in particular loves the -> arrow.

**Avoid patterns like:**
- "Input → Processing → Output"
- "This leads to better outcomes → which means higher engagement"
- "“Smart quotes” instead of straight "quotes" that you’d actually type"

**Write instead:** Type what a keyboard produces: "input -> processing -> output", straight quotes throughout.

---

## Composition

### Fractal Summaries

"What I'm going to tell you; what I'm telling you; what I just told you" -- applied at every level of the document. Every subsection gets a summary. Every section gets a summary. The document itself gets a summary.

**Avoid patterns like:**
- "In this section, we'll explore... [3000 words later] ...as we've seen in this section."
- "A conclusion that restates every point already made in the previous 3000 words"
- "And so we return to where we began."

**Write instead:** Say each thing once, where it lands hardest, and trust the reader to remember what they read two paragraphs ago. If a document is long enough to genuinely need a summary, write exactly one, at the top, and make it earn its place.

### The Dead Metaphor

Latching onto a single metaphor and beating it into the ground across the entire thing. A human writer would introduce a metaphor, use it then move on. AI will repeat the same metaphor 5-10 times.

**Avoid patterns like:**
- "The ecosystem needs ecosystems to build ecosystem value."
- "Walls and doors used 30+ times in the same article"
- "Every paragraph finds a way to say "primitives" again"

**Write instead:** Spend a metaphor once, then return to plain terms. If a metaphor is load-bearing enough to come back, develop it further on each return instead of repeating it unchanged.

### Historical Analogy Stacking

ESPECIALLY COMMON IN TECHNICAL WRITING: Rapid-fire listing of historical companies or tech revolutions to build false authority.

**Avoid patterns like:**
- "Apple didn't build Uber. Facebook didn't build Spotify. Stripe didn't build Shopify. AWS didn't build Airbnb."
- "Every major technological shift -- the web, mobile, social, cloud -- followed the same pattern."
- "Take Spotify... Or consider Uber... Airbnb followed a similar path... Shopify is another example... Even Discord..."

**Write instead:** One example, developed: what Shopify actually did, in which year, with what result. A single analogy the reader can verify beats five they have to take on faith.

### One-Point Dilution

Making a single argument and restating it in 10 different ways across thousands of words. The model pads a simple thesis to feel "comprehensive" by rephrasing the same idea with different metaphors, examples, and framings. An 800-word argument becomes 4000 words of circular repetition.

**Avoid patterns like:**
- "The same point, restated eight ways across 4000 words."
- "Each section rephrases the thesis with a different metaphor but adds nothing new"

**Write instead:** Make the point, support it with your two best pieces of evidence, and stop. If the piece feels thin at 800 words, the fix is a second idea, not a third restatement of the first.

### Content Duplication

Repeating entire sections or paragraphs verbatim within the same piece. This happens when the model loses track of what it has already written, especially in longer pieces. A dead giveaway of unedited AI output. Less common nowadays.

**Avoid patterns like:**
- "The same section appeared twice, word-for-word identical."
- "Paragraph 3 and paragraph 17 are the same sentence reworded"

**Write instead:** Reread the whole draft before shipping. If a paragraph feels familiar as you write it, search the draft for its key phrase; you probably already wrote it.

### The Signposted Conclusion

Explicitly announcing the conclusion with "In conclusion", "To sum up", or "In summary". Competent writing doesn't need to tell you it's concluding. The reader can feel it. AI signals its structural moves because it's following a template, not writing organically.

**Avoid patterns like:**
- "In conclusion, the future of AI depends on..."
- "To sum up, we've explored three key themes..."
- "In summary, the evidence suggests..."

**Write instead:** End on substance: a consequence, a recommendation, an open question. "The migration starts Monday" is a stronger last line than any summary of the preceding argument.

### "Despite Its Challenges..."

The rigid formula where AI acknowledges problems only to immediately dismiss them. Always follows the same beat: "Despite its [positive words], [subject] faces challenges..." then ends with "Despite these challenges, [optimistic conclusion].".

**Avoid patterns like:**
- "Despite these challenges, the initiative continues to thrive."
- "Despite its industrial and residential prosperity, Korattur faces challenges typical of urban areas."
- "Despite their promising applications, pyroelectric materials face several challenges that must be addressed for broader adoption."

**Write instead:** Commit to a weighing: "the latency problem is real, and until it's fixed I wouldn't use this for anything interactive." Acknowledged problems should be allowed to change the conclusion, not decorate it.

---

## Quick hunt list

For an editing pass, search the draft for these strings. Each hit is a candidate, not automatically a problem; judge it against its entry above.

- Words: `delve`, `tapestry`, `landscape`, `paradigm`, `leverage`, `utilize`, `robust`, `seamless`, `harness`, `streamline`, `quietly`, `fundamentally`, `remarkably`
- Phrases: `serves as`, `stands as`, `marks a`, `not just`, `isn't just`, `not because`, `worth noting`, `Importantly`, `Interestingly`, `Notably`, `Here's the`, `Think of it`, `It's like a`, `Imagine a`, `Let's break`, `Let's unpack`, `Let's dive`, `In conclusion`, `To sum up`, `In summary`, `Despite these`, `experts`, `observers`, `industry reports`
- Structure checks: count the em dashes (more than 2-3 per page is a cluster); scan bullet lists for bold-first labels; scan paragraph openings for repeated first words; check whether any "from X to Y" has a real middle; check the last paragraph for a restatement of the first.

---

Remember: any of these patterns used once might be fine. The problem is when
multiple tropes appear together or when a single trope is used repeatedly.
Write like a human: varied, imperfect, specific.
