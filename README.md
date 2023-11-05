# team-zoe-plus: SurfSight
_Anthropic hackathon project for team zoe plus_ 

SurfSight is a browser extension that applies accessibility edits on the fly.

## Project Story

### Inspiration

> _"Making the web free and fair for everyone is a relatively low-cost investment, but it's one that we often choose to neglect."_ Abubakar Buwe

Did you know that **90%** of websites are incompatible with assistive technologies like screen readers? _[Source](https://abilitynet.org.uk/news-blogs/inaccessible-websites-keep-disabled-people-out-work-abilitynet-tells-government-taskforce)_

This means the majority of people living in the UK with disabilities are unable to complete _basic transactions_ on **25%** of websites. _[Source](https://www.clickawaypound.com/cap16finalreport.html)_

Our team was shocked at these statistics and frustrated at the state of accessibility in the tech industry. 
All four of us have worked at companies that built products for social good, but left accessibility as a problem for later. 
The issue is systemic: in 2023, we're still pushing for equity across the tech industry. 
We can't solve such an ingrained problem in one weekend, but we can make a small step.

### Implementation

We built our project in Python, Flask and TypeScript, connecting to two APIs:
- [WAVE](https://wave.webaim.org/standalone) web accessibility evaluation tool 
- Anthropic's [Claude API](https://claude.ai/) (obviously!)

and calling one HuggingFace model:
- [vit-gpt-2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning).

Our browser extension processes web pages by:
1. Extracting the URL and sending this to the WAVE API for accessibility auditing
2. Parsing accessibility errors from WAVE and extracting the offending sections
3. Sending these sections to Claude to fix.

We then re-render the edited page, so it is readable by screen readers and accessible to users.

We currently perform the following edits:
- Adding missing titles and headings (Claude)
- Increasing colour contrast (rule-based)
- Adding missing image alt text (vision captioning model)

Existing accessibility browser extensions cannot solve all of these problems, as they have no domain-specific text generation or image recognition capabilities. If we had more time, we would like to solve other problems that existing browser extensions cannot do, but we believe Claude can:
- Fix broken tags and buttons
- Outline required input on forms
- Edit the content for understandability, if desired.

### Challenges

We had two main challenges: API latency and HTML parsing.

#### API Latency

We initially tried chaining prompts together, asking Claude to identify accessibility issues in HTML, then asking Claude again to fix these edits.
However, since the HTML context contained so many tokens, each call to Claude took at least 30 seconds. Chaining these was not feasible, so we had to use external APIs instead.

Our extension still has fairly high latency because these API calls are sequential. If we had more time, we would love to solve this by: 
- parallelising requests
- chunking the HTML into smaller context windows for Claude
- self-hosting a Claude instance (when possible).

#### HTML DOM parsing

The WAVE accessibility audit API is fantastic at identifying where errors occur in the HTML. The main issue occurs when the page source is missing HTML tags, as the API does not identify where these should go. This means we have to pass the whole page to Claude to fix, which risks introducing new errors in Claude's output. 

Claude is not the best at generating the original page, as it often contains JavaScript code, which is likely to be unique and out of its distribution. This means the page can come out slightly garbled!

If we had more time, we would like to fix this by:
- more intelligently parsing the page for suspected areas to inject new HTML
- passing only these sections to Claude
- more intelligently rebuilding the page from the original code and Claude's output.

### Learnings

We learned many things over the weekend. Some are:
- Accessibility is a huge and widespread issue. It's particularly complex because web pages are so different and have a wide range of errors arising from many interacting sections of code.
- LLMs allow us to target abstract problems across a wide range of data in a standardised way (e.g. fixing inaccessible HTML), which would be impossible through rule-based methods.
- Deployment is hard, contracts are important and integration testing is essential!