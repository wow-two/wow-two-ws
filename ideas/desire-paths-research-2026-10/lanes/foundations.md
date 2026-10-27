# Desire paths: origin, software examples, "pave the cowpaths", and limits

*Lane: foundations. Research date: 2026-10-27. All pages fetched or searched on that date.*

*Tags used below:*
- **[PRIMARY]**: I read the original document or a faithful copy of it.
- **[FETCH]**: a fetch tool returned a summary of the page (small-model extraction), not verbatim text. Treat dates and figures as likely right, wording as unverified.
- **[SEARCH]**: only a search-result summary; I did not open the page (blocked, 403, timeout, or not attempted). Weakest tier.
- **[FOLKLORE]**: widely repeated, no primary source found.
- **[SELF-REPORTED]**: a founder or author telling their own story.

---

## 1. What does the seed video argue?

### Takeaway
The video is "Why the best software must LIE to you" by Kole Jain, published 2026-10-21, about 9.4 minutes. I could read its title, description, chapter list and cited sources, but **not a transcript**. It does not appear to be mainly about desire paths. Its chapters and sources point to interaction timing and intent prediction (double-click delays, hover-intent menus, destructive actions). What the video actually claims about desire paths, if anything, is unverified.

### Cited Findings
- Title "Why the best software must LIE to you"; author/channel "Kole Jain", `https://www.youtube.com/@kolejain` — [YouTube oEmbed for the video](https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=S8DcTJm8pYM&format=json) **[PRIMARY]**, fetched 2026-10-27.
- Page metadata, read from the watch-page HTML on 2026-10-27: published 2026-10-21 07:56 PT; length 563 s (9:23); 87,105 views at fetch time; category "People & Blogs"; owner "Kole Jain" — [YouTube watch page](https://www.youtube.com/watch?v=S8DcTJm8pYM) **[PRIMARY]**.
- Description (paraphrased): asks why some tools feel effortless and others painful; says it digs into "invisible specifics" of everyday software, naming pausing music from AirPods, how drag and drop works, and when buttons actually trigger. Opens with a sponsor line (Mobbin, 20% off) and links Figma files at kolejain.com. — [YouTube watch page](https://www.youtube.com/watch?v=S8DcTJm8pYM) **[PRIMARY]**.
- Chapters from the page metadata (timestamps from `timeRangeStartMillis`): The delay in interaction (0:00) · Competing UI actions (0:50) · Anticipating user intent (2:20) · Assumptions and tradeoffs (3:35) · Rethinking destructive actions (5:13) · The future of interaction (about 7:06) — [YouTube watch page](https://www.youtube.com/watch?v=S8DcTJm8pYM) **[PRIMARY]**.
- Sources listed in the description: Raymond Chen (Old New Thing, 2009-04-29), an Ohio State University "Desire Lines" page, and Ben Kamens's "Breaking down Amazon's mega dropdown" — [YouTube watch page](https://www.youtube.com/watch?v=S8DcTJm8pYM) **[PRIMARY]**.
- Raymond Chen's post "Why is there sometimes a half-second delay between the click and the action?" (2009-04-29): some clicks act only after the double-click interval because the software waits to see whether a second click follows; Chen calls this filtering "debouncing"; the cost is that single-clickers always wait about half a second. Example: a stray second click on a link that launches a new process (his example opens a control panel without focus) is harmful, while on a modal dialog it is mostly harmless. — [The Old New Thing](https://devblogs.microsoft.com/oldnewthing/20090429-00/?p=18413/) **[FETCH]**.
- The OSU source is an art show, not a campus-planning record: "Desire Lines", Urban Arts Space, 2025-02-11 to 2025-03-15, labelled an MFA thesis exhibition. It uses paths worn across OSU's campus as a metaphor for self-determined movement versus routes "decided for us by urban planning and civil engineering". The page says nothing about OSU paving or ignoring paths and does not explain where the term comes from. — [OSU Urban Arts Space](https://uas.osu.edu/events/desire-lines) **[FETCH]**.
- Ben Kamens's post could not be read (HTTP 403 on 2026-10-27). — [bjk5.com](https://bjk5.com/post/44698559168/breaking-down-amazons-mega-dropdown) (not retrieved).

### Inferences
- The title's "lie" most likely means software that acts on a guess about intent instead of the literal input (wait before acting, tolerate diagonal mouse travel, defer destructive actions). That reading rests on chapter names plus the Chen post, not on the video's words.
- Desire lines probably appear in the video as an analogy for "behaviour first, interface second". This is a guess. Do not attribute any specific desire-path claim to the video.
- The brief's "Ohio State wait-and-see paving" is **not** supported by the video's own OSU source. See section 2.

### Gaps
- No transcript. YouTube lists auto-generated English captions, but the caption endpoint returned an empty body to one request, a second attempt was blocked by the environment, and a third-party transcript site returned 403. I did not try to route around that.
- Main claims, narration and any desire-path segment of the video: unknown. A human could paste the transcript (the "Show transcript" panel under the video) to close this.
- Ben Kamens's post content: not read. Whether it describes the diagonal-travel / hover-intent technique in Amazon's mega dropdown is from my background knowledge, not from a fetched source.

---

## 2. Where does the term come from?

### Takeaway
The Bachelard attribution is a **myth**: two independent sources say the phrase is not in *The Poetics of Space*. "Desire line" is documented earlier as a **transport-planning** term for a straight origin-to-destination line (cited to a 1946 Portland survey), and the "worn trail" sense is the later popular one. The campus "wait and see, then pave" story is repeated widely but I found **no primary source** for Ohio State, Columbia/Eisenhower or Virginia Tech; Michigan State is reported secondhand only.

### Cited Findings
**Bachelard (debunked)**
- Tom Turner (Landscape Architecture, LAA, 2018-04-18): the phrase is "sometimes, and incorrectly, attributed to the French philosopher Gaston Bachelard"; *The Poetics of Space* (1958) is about topoanalysis and does not coin the term. — [Landscape Architecture, "Desire Lines are a key principle in landscape architecture"](https://www.landscapearchitecture.org.uk/desire-lines-key-principle-landscape-architecture/) **[FETCH]**.
- The Land Reader glossary reportedly states that neither "lignes de désir" nor "chemins du désir" nor a similar phrase appears in Bachelard's text, and lists the etymology as "uncertain". — [The Land Reader glossary](https://thelandreader.com/glossary/desire-path) **[SEARCH]** (page blocked by a bot check; two attempts).
- The attribution is still repeated: a Spitalfields Life column reportedly says Bachelard invented "desire paths" (lignes de désir) in *The Poetics of Space* (1958) while noting others question it. The search result did not say which of the site's several desire-path posts it is; this link is one of them. — [Spitalfields Life](https://spitalfieldslife.com/2025/05/30/east-end-desire-paths-i/) **[SEARCH]**.
- I found no source that identifies who first coined the French phrase.

**Earlier technical meaning**
- Turner: American transport planners used "desire line" a year before *A Streetcar Named Desire* (premiered 1947) to mean a straight line from an origin to a destination; example cited: the 1946 *Portland Metropolitan Area Traffic Survey*. He also says "the origin of the phrase 'desire line' is romantic" and floats the New Orleans streetcar named Desire as a possible influence on the phrase's romantic overtones. The streetcar idea is **speculation** ("may have influenced"). — [Landscape Architecture, 2018-04-18](https://www.landscapearchitecture.org.uk/desire-lines-key-principle-landscape-architecture/) **[FETCH]**.
- Wikipedia's "Desire path" article reportedly gives the 1959 *Chicago Area Transportation Study* (p. 40) as an early documented use; that conflicts with Turner's earlier 1946 cite (I did not see either primary document). Wikipedia also lists many synonyms (game trail, cow path, goat track, desire line in transport planning). — [Wikipedia: Desire path](https://en.wikipedia.org/wiki/Desire_path) **[FETCH]**.

**99% Invisible article (the usual pop source)**
- "Least Resistance: How Desire Paths Can Lead to Better Design", by Kurt Kohlstedt, published 2016-01-25. Claims: paths can form after as few as fifteen traversals and are self-reinforcing; reasons include shortcuts, gentler slopes, avoiding alarmed exits and superstition; signs and barriers often just produce new alternative paths; Finnish officials document where people walk in parks after the first snowfall; Michigan State paths were eventually turned into sidewalks; Virginia Tech and UC Berkeley have "reportedly" waited to see which routes people took before paving. — [99% Invisible](https://99percentinvisible.org/article/least-resistance-desire-paths-can-lead-better-design/) **[FETCH]**.
- The article does not discuss the term's origin, Bachelard or Ohio State, and has no direct quotes from its author. The brief's "Kurt Colstad" is a misspelling of the byline **Kohlstedt** (a search summary produced "Colstad"). — same source.
- It is a written article, not an episode; the audio version is reportedly a segment of episode 263 "You Should Do a Story" (2017-06-20). — [99% Invisible](https://99percentinvisible.org/article/least-resistance-desire-paths-can-lead-better-design/) and [podscripts transcript page](https://podscripts.co/podcasts/99-invisible/263-you-should-do-a-story) **[SEARCH]**.

**Campus "wait and see" claims**
- Michigan State: UW-Madison News (Parker Schorr, 2019-04-24) says MSU leaves campus unpaved, lets students wear paths, and later paves them. This is a Wisconsin article describing MSU, not an MSU source. UW-Madison itself does the opposite: it designs to prevent unwanted paths (runnels and a raised lawn on Bascom Hill, plantings, post-and-chain barriers, metal "staples" along University Avenue). — [UW-Madison News](https://news.wisc.edu/desire-paths-the-unofficial-footpaths-that-frustrate-captivate-campus-planners/) **[FETCH]**. **Status: secondhand, plausible, unconfirmed at the source.**
- Virginia Tech: Wikipedia cites a 2014 Virginia Tech News article reporting that dirt paths on the Drillfield would be paved. That supports "VT paved worn paths", not "VT waited and observed". — [Wikipedia: Desire path](https://en.wikipedia.org/wiki/Desire_path) **[FETCH]**. 99% Invisible's own wording is "reportedly".
- Columbia and Eisenhower: a FOAFtale (friend-of-a-friend) entry presents the story that Columbia's president Eisenhower had students' routes observed and then paved. The entry gives no primary source and cites a secondary author. — [FOAFtale News #66](https://www.folklore.ee/FOAFtale/ftn66.htm) **[SEARCH]**. **Status: FOLKLORE.**
- Ohio State: no source found for any OSU paving policy. Wikipedia only has a photo caption of a desire path at OSU. The OSU page the video cites is an MFA exhibition. **Status: unsupported.**
- A UMass blog comment recounts an engineering professor's story of a new college that waited a year before paving; the commenter says it is unverifiable. — [UMass blog](https://websites.umass.edu/wynn/2009/11/27/desire-lines) **[SEARCH]**. **Status: FOLKLORE.**
- UW-Madison planner Aaron Williams lists three responses to a path: formalize it, add an obstacle, or change the terrain to make it harder. — [UW-Madison News, 2019-04-24](https://news.wisc.edu/desire-paths-the-unofficial-footpaths-that-frustrate-captivate-campus-planners/) **[FETCH]**.

**Science of path formation**
- Helbing, Keltsch and Molnár, "Modelling the evolution of human trail systems", *Nature* 388, 47-50 (1997): an "active walker" model of pedestrians who shape the ground they walk on, which feeds back on later walkers; a [Discover article](https://www.discovermagazine.com/the-sciences/a-better-way-to-keep-us-off-the-grass) describes the trade-off as shortcut urge versus the convenience of following an existing path. I did not verify the comfort/detour wording in the Nature text. — [IDEAS/RePEc record](https://ideas.repec.org/a/nat/nature/v388y1997i6637d10.1038_40353.html) and [arXiv preprint](https://arxiv.org/abs/cond-mat/9805158) **[SEARCH]**.

**Carrying it into HCI**
- Carl Myhill, "Commercial Success by Looking for Desire Lines", APCHI 2004 (Rotorua, 2004-06-29 to 07-02), pp. 293-304. Reported claims: desire lines are the "ultimate unbiased expression of natural human purpose"; watching for them shows users' actual purpose more directly than focus groups; the commercial angle is reading what users type into site search. Myhill's own profile says the paper led William Lidwell to add Desire Lines to *Universal Principles of Design* (**[SELF-REPORTED]**). — [IxDF author page](https://ixdf.org/literature/author/carl-myhill) **[SEARCH]**; the "being alert for desire lines" line is also quoted in the [99% Invisible article](https://99percentinvisible.org/article/least-resistance-desire-paths-can-lead-better-design/) **[FETCH]**.
- Academic framing: Wiesche, Böhm and Schermann (*European Journal of Information Systems*, 2024) use "digital desire paths" for designers improving systems by watching how people work around them, noting the field usually treats IS workarounds as negative disturbances. — [TU Dortmund news item](https://dt.wiwi.tu-dortmund.de/en/newsdetail/publication-of-a-study-on-how-unintended-use-can-inform-information-system-design-39621) and [tandfonline DOI page](https://www.tandfonline.com/doi/full/10.1080/0960085X.2024.2313537) **[SEARCH]** (both pages failed on direct fetch: socket error and 403).

### Inferences
- The original technical "desire line" was an idealised, unconstrained demand line on a planning diagram. The worn-trail meaning is a different object (observed behaviour under constraints). Borrowing the term into UX blends "what users want" with "what users do given our constraints".
- Cite the origin as "obscure, with the Bachelard story debunked". Avoid "coined by".
- For the report: the safe campus claim is "some campuses reportedly observe before paving (Michigan State, per UW-Madison News; Virginia Tech and Berkeley, per 99% Invisible); others, like UW-Madison, design to prevent paths". Do not name Ohio State or Eisenhower/Columbia as fact.

### Gaps
- No primary source for Michigan State, Virginia Tech, Berkeley, Ohio State or Columbia policies.
- First coinage of the worn-trail sense (Wikipedia 1959 versus Turner 1946 conflict unresolved; neither primary survey document read).
- Wikipedia's article and the Wiesche et al. paper were read only through summaries.

---

## 3. Canonical software desire paths

### Takeaway
The best-sourced cases are **Twitter's @reply, hashtag, retweet and thread**, which a product team can cite with dates, and **email/self-messaging used as a notebook**. Instagram/Burbn and Slack are *pivots informed by usage*, not UI workarounds; Slack in particular has no desire-path sourcing at all. Screenshots-as-bookmarks and URL-bar-as-search are weakly sourced.

### Cited Findings
**Twitter @reply / mention**
- Users invented the @-prefix reply. Dates conflict: Quartz credits Robert S. Anderson with the first @-reply on 2006-11-02 (with a space) and Neil Crosby with the first no-space version on 2006-11-23; Kottke, citing Evan Henshaw's tweet digging, dates the first use to 2006-11-23 (Thanksgiving), and says Garrett Murray later found an earlier one. — [Kottke, "The history of Twitter's @reply" (2012)](https://kottke.org/12/07/the-history-of-twitters-reply) **[FETCH]**; [Quartz](https://qz.com/135149/the-first-ever-hashtag-reply-and-retweet-as-twitter-users-invented-them) **[SEARCH]** (403 on direct fetch).
- Twitter made @replies an official feature on 2007-05-30 with a dedicated replies page (Quartz, via search summary), and Wikipedia reportedly says the no-space form became the norm within 2007. — [Quartz](https://qz.com/135149/the-first-ever-hashtag-reply-and-retweet-as-twitter-users-invented-them) and [Wikipedia: Mention (blogging)](https://en.wikipedia.org/wiki/Mention_(blogging)) **[SEARCH]**.

**Hashtag**
- Chris Messina's proposal of 2007-08-23 (tweet asking about "# (pound) for groups", example #barcamp) and his longer post "Groups for Twitter; or a proposal for Twitter tag channels", dated 2007-08-25: channels created by prefixing words with `#`; "No one owns or administers a tag channel"; a channel exists once someone first posts with it. — [Messina's post](https://factoryjoe.com/2007/08/25/groups-for-twitter-or-a-proposal-for-twitter-tag-channels/) **[FETCH]**; [Wikipedia: Chris Messina](https://en.wikipedia.org/wiki/Chris_Messina_(inventor)) **[FETCH]**.
- Twitter's first reaction was reportedly that "these things are for nerds" (Smithsonian, Ben Panko, 2017-08-23, cited by Wikipedia). Later 2007 use around the San Diego wildfires spread it; Twitter began hyperlinking hashtags to search on 2009-07-02 (Wikipedia, uncited there). — [Wikipedia: Chris Messina](https://en.wikipedia.org/wiki/Chris_Messina_(inventor)) **[FETCH]**. The "nerds" quote is **secondhand**.
- The `#` came from IRC channel names; search summaries also report Messina saying he did not create it for Twitter. — [Texas Public Radio, 2017](https://www.tpr.org/science-technology/2017-08-23/happybirthday-quintessential-twitter-feature-turns-10) **[SEARCH]**; 99% Invisible also says hashtags and at-signs drew on IRC ([article](https://99percentinvisible.org/article/least-resistance-desire-paths-can-lead-better-design/) **[FETCH]**).

**Retweet, quote tweet, thread**
- 2009-08-13: Twitter announced "Project Retweet" Phase One with a retweeting API; Biz Stone called the copy-and-paste way "cumbersome"; developer Marcel Molina: "yet another example of Twitter's users discovering innovative ways to use the service." — [TechCrunch, 2009-08-13](https://techcrunch.com/2009/08/13/twitter-announces-a-retweeting-api) **[FETCH]**.
- Stone, in his blog post: retweeting is "a great example of Twitter teaching us what it wants to be". Steven Levy (*Wired*, Oct 2009) writes that users, not Twitter, created retweeting, and that the first official version dropped the ability to add commentary that users often wanted. — [Levy via 3 Quarks Daily](https://3quarksdaily.com/?p=31323) **[FETCH]**.
- The commentary function came back later: "retweet with comment" in April 2015, later called Quote Tweet. — [iClarified](https://www.iclarified.com/48260/twitter-introduces-revamped-quote-tweets) **[SEARCH]**.
- Threads: Twitter made native threads official on 2017-12-12; TechCrunch (Sarah Perez) frames tweetstorms as a user convention for working around the character limit, and says RT, @reply and hashtag followed the same user-first pattern. — [TechCrunch, 2017-12-12](https://techcrunch.com/2017/12/12/twitter-officially-launches-threads-a-new-feature-for-easily-writing-tweetstorms/) **[FETCH]**.

**Instagram from Burbn (pivot informed by usage; analogous, not a UI workaround)**
- Burbn was an HTML5 mobile web app with check-ins, plans, points for hanging out and photo posting; the iPhone version "felt cluttered, and overrun with features"; the team kept only photos, comments and likes. — [TechCrunch, "A Pivotal Pivot", 2010-11-08](https://techcrunch.com/?p=241149) **[FETCH]**.
- Systrom's statement that users "loved posting pictures on Burbn", and an NPR interview figure of about 100 users who each loved the photo part: seen only in search summaries; the NPR and CNN Money pages timed out or returned 503. — [NPR transcript](https://www.npr.org/transcripts/493923472) and [CNN Money, 2011-09-13](https://money.cnn.com/2011/09/13/technology/startups/instagram_burbn/) **[SEARCH]**, **[SELF-REPORTED]**.

**Slack**
- Slack began as an internal chat tool at Tiny Speck during development of the game Glitch; when Glitch proved unprofitable (by October 2012) Butterfield repurposed the tools. Sources do not describe it as a user workaround. — [Wikipedia: Slack](https://en.wikipedia.org/wiki/Slack_(software)) and [Britannica](https://britannica.com/technology/Slack) **[SEARCH]**. **Status: not a desire-path example. A pivot story.**

**Spreadsheets as databases**
- Airtable's Howie Liu (Founded & Funded, 2023-06-13): as Excel became mainstream "people ended up using it as their makeshift database" (customer, inventory and RSVP lists); Airtable was pitched as a spreadsheet-database hybrid. — [Madrona interview](https://madrona.com/airtable-howie-liu-no-code-apps-product-led-growth-ai-enabled-workflows) **[FETCH]**, **[SELF-REPORTED]**. TechCrunch's 2015-02-25 Airtable article frames it as making relational databases usable — [TechCrunch](https://techcrunch.com/2015/02/25/airtable/) **[SEARCH]**.
- "Almost 90% of spreadsheets don't have formulas" is attributed to Liu by Contrary and Nira; secondhand. — [Contrary](https://research.contrary.com/report/airtable) **[SEARCH]**.

**Email (and chat) as notebook / task list**
- Whittaker and Sidner, "Email Overload: Exploring Personal Information Management of Email", CHI '96, pp. 276-283: email, designed for communication, was being used for task management and personal archiving. — [CHI '96 proceedings](https://www.chi1996.chistatic.hosting.acm.org/proceedings/papers/Whittaker/sw_txt.html) **[SEARCH]**.
- WhatsApp announced "Message Yourself" on 2022-11-28. The earlier workaround was to create a group with a contact and remove them; Telegram had self-messaging from launch and Signal has Note to Self. — [TechCrunch, 2022-11-28](https://techcrunch.com/2022/11/28/whatsapp-rolls-out-a-feature-that-makes-it-easier-to-message-yourself/) **[SEARCH]**. No source for "emailing yourself" as a measured behaviour beyond Whittaker and Sidner.

**Screenshots as bookmarks / URL bar as search (weak)**
- Screenshots: a 2023 ITU Copenhagen study of 52 participants' screenshots looked at why people take them — [ITU publication page](https://pure.itu.dk/en/publications/why-do-people-take-screenshots-on-their-smartphones/) **[SEARCH]**; I did not see its findings. A Binghamton study in *Memory & Cognition* (seven experiments, 892 students) found screenshotting reduced memory of the content versus just viewing — [ConsumerAffairs summary](https://www.consumeraffairs.com/news/screenshots-are-supposed-to-help-you-remember-a-study-found-the-opposite-082626.html) **[SEARCH]**. Neither shows screenshots *as bookmarks* specifically.
- URL bar: Chrome launched in September 2008 with the Omnibox, a combined address and search box — [Search Engine Land](https://searchengineland.com/searching-with-google-chrome-omnibox-14664) **[SEARCH]**. Krug's *Don't Make Me Think* chapter 2 ("Scanning, satisficing, and muddling through") is summarised as using users typing full URLs into a search box as an example — [web-developpeur.com summary](https://www.web-developpeur.com/en/library/dont-make-me-think/) **[SEARCH]**. A claim that the Omnibox was designed *because of* that behaviour has no source.

### Inferences
- A clean desire-path case needs: (a) users built a convention in the gap, (b) the vendor later made it a first-class feature. Twitter's @, #, RT and thread all fit. Instagram, Slack and Airtable fit "observed behaviour became the product", not "workaround got paved".
- Retweet shows paving can lose what the path had: the first official retweet dropped commentary, and the feature returned years later.
- Several "canonical" examples are told by the people who profited from them (Systrom, Liu, Stone). Treat them as narrative, not evidence.

### Gaps
- No credible desire-path source for Slack, screenshots-as-bookmarks, or URL-bar-as-search.
- Primary Twitter announcements (2007 replies page, 2009 hashtag linking, 2015 retweet with comment) were not retrieved; only secondary coverage.
- First-use dates for @reply conflict across sources. For "RT", a search summary said the coinage is commonly credited to user Eric Rice on 2007-04-18, but no specific page backed it, so it is left here as an unverified lead.

---

## 4. "Pave the cowpaths": exact wording and scope

### Takeaway
The HTML-world phrase lives in the **W3C HTML Working Group's "HTML Design Principles"** (2007), section 2.4; I did not find it in the WHATWG Standard's introduction or design notes. It is a *compatibility* rule about markup authors' habits, with a modest example (`<br/>`). The same idiom means the **opposite** in Michael Hammer's 1990 reengineering article ("stop paving the cow paths"), which is a critical limit for any team that borrows the phrase.

### Cited Findings
- W3C "HTML Design Principles", editors Anne van Kesteren (Opera) and Maciej Stachowiak (Apple), from the HTML Working Group; the fetched copy is a Working Draft dated 2007-11-26 (First Public Working Draft, intended to become a Note). Section 2.4 "Pave the Cowpaths" sits under "2. Compatibility", beside 2.1 Support Existing Content, 2.2 Degrade Gracefully, 2.3 Do not Reinvent the Wheel and 2.5 Evolution Not Revolution. — [W3C HTML Design Principles](https://www.w3.org/TR/html-design-principles/) **[FETCH]**.
- Principle wording: "When a practice is already widespread among authors, consider adopting it rather than forbidding it or inventing something new." Example, verbatim: "Authors already use the `<br/>` syntax as opposed to `<br>` in HTML and there is no harm done by allowing that to be used." — [W3C HTML Design Principles](https://www.w3.org/TR/html-design-principles/) **[FETCH]** (the fetch tool truncated the principle sentence at its quote limit; the ending "or inventing something new" is confirmed by the Hunt thread below, which quotes the existing wording).
- Intended scope was debated at the time. Lachlan Hunt (public-html list, 2007-08-14) argued the wording was vague and invited literal copying of existing markup. He proposed: "Investigate existing practices and design or adopt features that meet the desires of authors." He explained the idiom through desire lines: landscapers study where people walk and pave those routes. In his reading the principle means analysing what authors are trying to do and designing features to match, not adopting whatever markup they happen to use. — [public-html list post](https://lists.w3.org/Archives/Public/public-html/2007Aug/0435.html) **[FETCH]**. The fetched W3C copy still shows the older wording, so I cannot say his proposal was adopted.
- The current WHATWG HTML Standard: the Introduction chapter, including section 1.7 "Design notes", does not contain the phrase "pave the cowpaths" (checked 2026-10-27; I did not search the rest of the very large spec). It says HTML's inconsistencies come from many sources over decades and that "implementation bugs have often become de-facto, and now de-jure, standards"; its history section stresses backwards compatibility. — [WHATWG: Introduction](https://html.spec.whatwg.org/multipage/introduction.html#design-notes) **[FETCH]**.
- Opposite sense: Michael Hammer, "Reengineering Work: Don't Automate, Obliterate", *Harvard Business Review*, July-August 1990 (Reprint 90406): "It is time to stop paving the cow paths. Instead of embedding outdated processes in silicon and software, we should obliterate them and start over." — [HBR reprint PDF](https://folk.idi.ntnu.no/thomasos/paper/hammer_reengineering.pdf) **[PRIMARY]** (text extracted from the PDF).
- Idiom origin: a Boston anecdote says the early city "merely paved the paths that had been worn by cattle", yielding an illogical street plan; the source quotes a StackExchange answer. — [Craig Bailey, "Paving the cow paths"](https://www.craigbailey.net/paving-the-cow-paths/) **[FETCH]**. **Status: FOLKLORE.** No primary source found for the Boston claim, and nothing ties the phrase to Hammer as coiner.

### Inferences
- The W3C principle is permissive ("consider adopting"), not mandatory, and its only example is harmless syntax. It does not say "adopt every widespread workaround", and it gives no test for when a practice should *not* be adopted. That test is the missing piece for a UI team.
- For a frontend team: use "pave the cowpaths" in Hunt's sense (serve the intent behind the path) rather than the literal sense (ratify the exact workaround). Hammer's sense is the warning for when the path is a symptom of a broken process.
- Cite the phrase to the W3C 2007 draft, not to WHATWG.

### Gaps
- Whether a later W3C Note or the HTML5 spec text changed the wording; I read one copy only.
- Who first used "pave the cowpaths" in software design. Not found.

---

## 5. Critiques and limits

### Takeaway
A desire path is evidence of *behaviour under current constraints*, not of a good need or a good solution. The cited limits are: paths can be unsafe or harmful, can be circumvention of a bad control, are self-reinforcing (popular is not the same as preferred), show only the people who arrived, and can be flattened by a clumsy first paving. Blocking tends to fail and redirects or redesign tends to work better, but the evidence for software is mostly by analogy.

### Cited Findings
**Danger and harm**
- UW-Madison planners treat some paths as safety problems: shortcuts across streets, intersections and railroad tracks; they added "staples" (short metal barriers) along University Avenue, removed a path on Observatory Drive, and planned a safer alternative route beside the railroad. Paths damaged effigy mounds, and the Lakeshore Nature Preserve restricts paths to protect habitat. — [UW-Madison News, 2019-04-24](https://news.wisc.edu/desire-paths-the-unofficial-footpaths-that-frustrate-captivate-campus-planners/) **[FETCH]**.
- Ecology: Wikipedia reports habitat fragmentation and edge effects (strongest about 50 m from a forest edge) from desire paths, and says signage reduces but does not stop use (citing Primack & Terry 2021, Tatsumi et al. 2023, Saxena et al. 2020). — [Wikipedia: Desire path](https://en.wikipedia.org/wiki/Desire_path) **[FETCH]**.

**Blocking is weak**
- 99% Invisible: signs and barriers often produce new alternative paths. — [99% Invisible](https://99percentinvisible.org/article/least-resistance-desire-paths-can-lead-better-design/) **[FETCH]**.
- A study titled "Pedestrian Characteristics That Favor Desire Lines Despite Closure" exists (ASCE, *Journal of Urban Planning and Development*); I could not read its abstract. — [ASCE Library](https://ascelibrary.com/doi/10.1061/%28ASCE%29UP.1943-5444.0000577) **[SEARCH]** (403).

**Workarounds that circumvent a control**
- Adams and Sasse, "Users are not the enemy", *Communications of the ACM* (1999): security departments often treat users as a risk; the study found circumvention was often caused by how mechanisms were implemented and by users' lack of knowledge; authors argue for user-centred security design. — [CACM](https://cacm.acm.org/?p=5985) and [UCL PDF](https://discovery-pp.ucl.ac.uk/20247/2/CACM%20FINAL.pdf) **[SEARCH]**.

**Manipulated or misleading signals**
- Mathur et al., "Dark Patterns at Scale", CSCW 2019: crawl of about 11K shopping sites found 1,818 dark-pattern instances across 15 types and 7 categories; defines dark patterns as UI choices that benefit the service by coercing, steering or deceiving users into unintended, potentially harmful decisions. Harry Brignull coined the term in 2010. — [arXiv 1907.07032](https://arxiv.org/pdf/1907.07032) and [deceptive.design](https://deceptive.design/about-us/dr-harry-brignull) **[SEARCH]**. Prevalence figures differ across secondary reports.

**Self-reinforcement and "unbiased" claims**
- 99% Invisible says paths form after about fifteen traversals and are self-reinforcing because later walkers follow the visible route. — [99% Invisible](https://99percentinvisible.org/article/least-resistance-desire-paths-can-lead-better-design/) **[FETCH]**. Myhill calls desire lines the "ultimate unbiased expression of natural human purpose" ([IxDF](https://ixdf.org/literature/author/carl-myhill) **[SEARCH]**). The two statements are in tension.

**Survivorship bias**
- Abraham Wald, Statistical Research Group, WWII: armour belonged where returning bombers had *no* holes because planes hit there did not return. Accounts differ on details (Navy versus Air Force, background). — [History of Data Science](https://historyofdatascience.com/abraham-wald-a-statistical-hero) **[SEARCH]**.

**"Faster horses"**
- The Ford quote is probably misattributed: Quote Investigator's earliest link to Ford is *Cruise Industry News Quarterly* (1999), first ascription to Ford a 2001 *Marketing Week* letter; Patrick Vlaskovits (*HBR*, 2011-08-29) argued Ford's disdain for customer input hurt him later. — [Quote Investigator](https://quoteinvestigator.com/2011/07/28/ford-faster-horse/) **[SEARCH]**; Vlaskovits's HBR piece itself was not retrieved.

**Paving can flatten a path**
- The first official retweet dropped the commentary users added (Levy, *Wired* 2009, via [3 Quarks Daily](https://3quarksdaily.com/?p=31323) **[FETCH]**).

**Unintended behaviours become dependencies**
- Hyrum's Law: "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." Credited to Hyrum Wright and named by Titus Winters. — [hyrumslaw.com](https://www.hyrumslaw.com/) **[FETCH]**.

**Whose path it is**
- Nielsen (1997-09-30): users mostly don't read pages; 79% of test users always scanned new pages and 16% read closely. — [NN/g, "How Users Read on the Web"](https://www.nngroup.com/articles/how-users-read-on-the-web/) **[FETCH]**. Krug's "satisficing" and "muddling through" framing describes typical users taking the first reasonable option. — [chapter list and summaries](https://www.web-developpeur.com/en/library/dont-make-me-think/) **[SEARCH]**.

### Inferences
These are the researcher's synthesis. They are not sourced as such.
- **Pave when:** the path is frequent, harms nobody, serves a goal that is legitimately the user's, and the community already shares a convention (Twitter's @ and #). Pave the *intent* and keep what the path did (retweet commentary).
- **Redirect or redesign when:** the path avoids a control that is too costly (Adams and Sasse). Fix the cost, then retire the workaround.
- **Block, or leave unpaved, when:** the path crosses a safety, privacy or data-integrity boundary, or only exists because a dark pattern shaped behaviour. Blocking alone tends to spawn new paths, so pair it with a cheaper legitimate route.
- **Read telemetry with care.** A path in click data shows what survivors did under today's UI. It does not show users who bounced, users without the access or time to find the workaround, or users who took the route because the designed one was hidden or deceptive.
- **Local optimum:** a path is a compromise between the designed route and the user's effort. Paving it may lock in a mediocre route; no source found, so treat as a hypothesis.
- **Novice versus power user:** workarounds from muddling-through novices (typing URLs in a search box) and from experts (keyboard shortcuts, scripts) call for different fixes. Novice paths point to discoverability failures; expert paths point to missing capability or speed. Inference only.

### Gaps
- No empirical study of paving-versus-blocking outcomes in software UI. All guidance comes by analogy from physical paths and from security research.
- No source found on accessibility or on who is excluded from the visible path.
- Vlaskovits's HBR article, the Wiesche et al. paper, the ASCE abstract and the dark-pattern paper were not read in full.

---

## 6. Related concepts a UI team should know

### Takeaway
Affordances and signifiers say *what the interface communicates*; Jakob's Law says *why users arrive with habits from other products* (which become paths); the pit of success says *the default route should be the good one*; progressive disclosure says *where a paved path should sit*; "users don't read" says *don't expect documentation to redirect a path*; emergent trail models say *why paths self-reinforce*.

### Cited Findings
- **Affordances:** a term from James J. Gibson (reported as 1977) that Norman redefined for design in 1988 toward what is perceivable; the revised *Design of Everyday Things* (2013) adds **signifiers**: affordances say what actions are possible, signifiers say where the action should happen. — [Wikipedia: Affordance](https://en.wikipedia.org/wiki/Affordance) and [Wikipedia: The Design of Everyday Things](https://en.wikipedia.org/wiki/The_Design_of_Everyday_Things) **[SEARCH]**. In a 2008-11-17 post Norman says he should have said "perceived affordance" and that a cursor "is not an affordance; it is visual feedback"; the post does not mention desire lines. — [jnd.org](https://jnd.org/affordances-and-design/) **[FETCH]**.
- **Jakob's Law:** "Users spend most of their time on other sites." Users transfer expectations from familiar products to similar ones and prefer yours to work the same way; when changing, let users keep a familiar version for a limited time. Coined by Jakob Nielsen (his Substack dates the formulation to 2000). — [Laws of UX](https://lawsofux.com/jakobs-law/) **[FETCH]**; [NN/g video page](https://nngroup.com/videos/jakobs-law-internet-ux/) and [Nielsen's Substack](https://jakobnielsenphd.substack.com/p/jakobs-law) **[SEARCH]**.
- **Pit of success:** "we want our customers to simply fall into winning practices by using our platform and frameworks. To the extent that we make it easy to get into trouble we fail." Rico Mariani, MS Research MindSwap, October 2003, quoted by Brad Abrams (post dated 2003-10-02); Abrams generalises it to API design: steer developers in the right direction. — [Brad Abrams, "The Pit of Success"](https://learn.microsoft.com/en-us/archive/blogs/brada/the-pit-of-success) **[PRIMARY]**; popularised by [Jeff Atwood, 2007-08-29](https://blog.codinghorror.com/falling-into-the-pit-of-success/) **[FETCH]**.
- **Progressive disclosure:** Nielsen, 2006-12-03. Show core options first; defer advanced or rare features to a secondary display on request. "The very fact that something appears on the initial display tells users that it's important." Decide placement from task analysis, field studies and usage logs; more than two levels tends to confuse; distinct from staged disclosure (wizards). — [NN/g](https://www.nngroup.com/articles/progressive-disclosure/) **[FETCH]**.
- **Users don't read:** Nielsen, 1997-09-30, "How users read on the web": "They don't"; 79% always scanned, 16% read closely. — [NN/g](https://www.nngroup.com/articles/how-users-read-on-the-web/) **[FETCH]**. Krug, *Don't Make Me Think*, chapter 2 "Scanning, satisficing, and muddling through" (satisficing from Herbert Simon, 1957, per a summary). — [summary](https://www.web-developpeur.com/en/library/dont-make-me-think/) **[SEARCH]**.
- **Emergent behaviour:** Helbing et al. 1997 (see section 2) model trails as emerging from many walkers' decisions plus ground wear, and the Active Walker companion paper describes pedestrians producing a minimal-detour system. — [arXiv cond-mat/9805158](https://arxiv.org/abs/cond-mat/9805158) and [Physical Review E companion](https://ar5iv.labs.arxiv.org/html/cond-mat/9806097) **[SEARCH]**.
- **Hyrum's Law:** see section 5.

### Inferences
- Jakob's Law explains why paths often *import* a convention from elsewhere (hashtag and @ from IRC; "Message Yourself" from other messengers). When paving, match the imported convention rather than inventing a new one.
- The pit of success is the design goal; a desire path is the *measurement* that the goal was missed. Progressive disclosure tells you where the paved shortcut belongs (initial display versus secondary level).
- Because users scan and muddle, a desire path in a product often appears with no awareness that a designed route exists. Fix discoverability before declaring the designed route wrong.
- Because paths self-reinforce, early adoption by a small group can look like mass preference; check for survivorship and social-proof effects before paving.

### Gaps
- Affordance history (Gibson 1977, Norman 1988) is from Wikipedia-level sources; the books were not read.
- Lidwell *Universal Principles of Design* and Norman's own writing on desire lines: no direct source retrieved. A claim in Wikipedia that Norman (2010) used desire paths as a metaphor for intuitive design is unverified.
- The Rico Mariani original (2003) is only available as quoted by Abrams.
