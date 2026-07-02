# Root-Cause Loop

1. Reproduce or confirm the symptom.
2. Minimize to the smallest surface that still fails.
3. State competing hypotheses.
4. Gather evidence that distinguishes them.
5. Fix the root cause, not the nearest crash site.
6. Add or run a regression check.

If reproduction is impossible, say what evidence is missing and propose the smallest next probe.

High-risk signals:

- downstream parser guessing around invalid upstream output
- fallback defaults hiding missing required fields
- compatibility layer swallowing contract drift
- failure disappears only because the test no longer checks the original symptom

