# Implementation Notes

Keep this short — 5 questions, answers under 200 words total.

---

**1. How did you structure your LLM analysis and why?**

_Single call vs multiple calls? How did you get structured output? What tradeoffs did you consider?_

I used a single LLM call per article to keep it simple and predictable. I asked the model to return strict JSON that matches the Pydantic schema. I chose this approach after reading that one structured call is easier to control and validate than splitting logic into multiple requests.

---

**2. How did you handle errors or unexpected LLM responses?**

_What can go wrong (malformed JSON, API errors, missing fields) and how does your code handle it?_

I handled basic failure cases like missing API key, API errors, and invalid JSON. The LLM call is wrapped in try/except, and I return a clear 502 error if it fails. I also validate the response with Pydantic and retry once if parsing doesn’t work. My main goal was to keep the API stable and not break the UI.

---

**3. What did you prioritise on the frontend and why?**

_What did you choose to display and how? What did you leave out?_

I focused on clarity and visual structure. I displayed sentiment with a badge and score, grouped signals into positive/negative/neutral columns, and added a significance bar. I didn’t include optional fields in the UI to avoid clutter and keep it clean.

---

**4. What would you add with more time?**

_Which optional fields did you skip? What would you improve or extend?_

I would implement optional fields like claims and contradictions. I would also improve schema enforcement and maybe cache responses. On the frontend, I’d add collapsible sections for advanced data and better loading/error states.

---

**5. How did you test your implementation?**

_Which articles did you test with? What edge cases did you cover? How did you validate correctness?_

I tested the provided articles and added three of my own: positive, negative, and mixed. I checked that the sentiment and signals match the article tone and that results stay consistent across runs. I also verified that the UI handles empty sections correctly.
