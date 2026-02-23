# Implementation Notes

Keep this short — 5 questions, answers under 200 words total.

---

**1. How did you structure your LLM analysis and why?**

_Single call vs multiple calls? How did you get structured output? What tradeoffs did you consider?_

Single call to keep cost low, reduce latency and maintains single context for reasoning across fields.
Sent the existing pydantic model to send to openAI to get validated, structured JSON output.

---

**2. How did you handle errors or unexpected LLM responses?**

_What can go wrong (malformed JSON, API errors, missing fields) and how does your code handle it?_

Added a generic try catch that logs any HTTP errors from API for debugging.
Pydantic automatically handles validation errors or missing fields, raising exceptions if response doesn't match schema.

---

**3. What did you prioritise on the frontend and why?**

_What did you choose to display and how? What did you leave out?_

I chose to display all required fields and use colour coding to highlight positive/negative items.

---

**4. What would you add with more time?**

_Which optional fields did you skip? What would you improve or extend?_

I'd add some unit tests for the api. If adding the optional fields I'd create Pyfantic models for each dictionary, making it easy to pass structured data to OpenAI.


---

**5. How did you test your implementation?**

_Which articles did you test with? What edge cases did you cover? How did you validate correctness?_

Tested all articles in articles.json, checking for positive and negative reputation signals and checking for confidence score on articles.
Verified correctness by ensuring structured output matched the Pydantic model.
