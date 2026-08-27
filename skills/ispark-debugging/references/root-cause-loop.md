# Root-Cause Loop

1. Reproduce or confirm the exact symptom and establish the expected baseline.
2. Minimize to the smallest surface that still fails.
3. Inspect the relevant contract, recent changes, configuration, and known-good examples.
4. Trace the failing value or state backward across component boundaries to where it
   first became invalid; instrument both sides of a boundary when logs are ambiguous.
5. State competing hypotheses and choose the smallest probe that distinguishes them.
6. Fix the owning source, not the nearest crash site or downstream parser.
7. Add or run a regression check, then verify the adjacent integration boundary.

If reproduction is impossible, say what evidence is missing and propose the smallest next probe.

Do not propose a permanent fix while the cause is still only a guess. During an approved
incident response, a temporary mitigation may precede full diagnosis, but label it as a
workaround with an owner, removal condition, and follow-up verification.

High-risk signals:

- downstream parser guessing around invalid upstream output
- fallback defaults hiding missing required fields
- compatibility layer swallowing contract drift
- failure disappears only because the test no longer checks the original symptom
