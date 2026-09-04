# Test Design — how to derive cases worth running

This is the QA craft behind Casely. Read it before planning coverage (Phase 3) or
writing cases (Phase 4). Without it, generated suites drift toward whatever the
requirements happen to mention first: ten variations of the happy path and nothing
that would ever catch a bug.

## Contents

- [Start from the requirement, not the screen](#start-from-the-requirement-not-the-screen)
- [The five techniques that do most of the work](#the-five-techniques-that-do-most-of-the-work)
- [Quality bar for a single case](#quality-bar-for-a-single-case)
- [Coverage integrity](#coverage-integrity)
- [Spotting gaps in the requirements](#spotting-gaps-in-the-requirements)

---

## Start from the requirement, not the screen

For each requirement, ask three questions in order:

1. **What must be true when this works?** → the positive case.
2. **What can the user do wrong, and what can the system do wrong?** → negative cases.
3. **Where are the edges of the allowed range?** → boundary cases.

A requirement that produces only one case is usually a requirement that was not read
closely enough. "The user can transfer funds between their own accounts" hides a
currency, a limit, a balance check, an account state, and an audit trail.

---

## The five techniques that do most of the work

### Equivalence partitioning

Split each input into groups where every value behaves the same, then test one value
per group instead of many. The point is coverage without redundancy: if `1000 ₽` and
`1500 ₽` exercise the same code path, testing both buys nothing.

> Amount field, limit 100 000: partitions are *below minimum*, *valid*, *above limit*,
> *non-numeric*, *empty*. Five cases, not fifty.

### Boundary value analysis

Bugs cluster at the edges of a partition, because that's where `<` and `<=` get
confused. For a range of 1–100 000, test `0, 1, 100 000, 100 001` — the value on each
side of every boundary. Pair this with equivalence partitioning: partitions tell you
*which* groups exist, boundaries tell you *where they touch*.

Cover **both sides of every edge**. A suite with `100 000` and `100 001` but no `99 999`
proves the limit rejects, never that it accepts up to the limit — an off-by-one that
shifted the boundary down would pass. Same rule for time and age limits: a card usable
after 3 days needs 71 hours, 72 hours, and 73 hours, not just the rejection.

### Decision tables

When an outcome depends on several conditions at once, list the combinations
explicitly rather than reasoning in prose. This is where "we never tested that
combination" bugs live.

> Transfer allowed = account active AND balance sufficient AND under daily limit.
> Three conditions → the combinations that matter are: all true (success), plus one
> case per condition being the *only* false one (a distinct, specific error each time).

You rarely need all 2ⁿ rows. Cover every true-path and every single-condition failure;
add multi-condition failures only where the spec says the errors interact.

### State transitions

When an object moves through states, test the transitions and the ones that must be
rejected. An order that can go `created → paid → shipped` also needs a case proving it
*cannot* go `created → shipped`. Illegal transitions are where money goes missing.

### Error guessing

Apply what breaks in practice, even when the spec is silent. A short checklist to run
against any feature:

- Empty, whitespace-only, and maximum-length input
- Zero, negative, and fractional numbers where only positive integers are expected
- Special characters, emoji, right-to-left text, SQL/HTML-looking strings
- Double submit, back button after submit, refresh mid-flow
- Session expiry and permission loss in the middle of the flow
- Concurrent action on the same entity from two sessions
- Network failure between request and response — does the operation half-apply?

---

## Quality bar for a single case

A case is finished when someone who has never seen the feature could run it and get
the same verdict as you.

**Atomic** — one case verifies one behavior. If the title needs "and", it is two cases.
Bundling saves writing time and costs debugging time: a failed composite case tells you
something broke, not what.

**Independent** — it sets up its own preconditions and does not rely on a previous case
having run. Suites get reordered, parallelized, and partially executed.

**Deterministic expected result** — state the observable outcome, with the values.
"Balance decreases by 500 ₽ and a transaction appears in history with status
*Completed*" is verifiable. "Transfer works correctly" is an opinion.

One outcome per case, never a menu. "The minus sign is rejected **or** an error appears",
"the operation ends in **one of** created or pending" — a tester cannot mark either
pass or fail, so the case checks nothing. A genuine fork is two cases; an undecided spec
is a gap to report, and the case is written against a stated assumption.

**Reproducible data** — name the actual input. "Amount: 100 001" beats "an amount over
the limit", because the next person does not have to re-derive the limit.

**Steps are actions, not narration** — each step is something a person does. Assertions
belong in the expected result, not sprinkled through the steps.

Anti-patterns to avoid: "Check that everything works", "Verify the page displays
correctly", steps that restate the requirement without performing it, and cases whose
expected result is simply "no errors".

---

## Coverage integrity

Before handing a suite over, check three things:

1. **Every requirement in scope is covered by at least one case.** Keep the mapping
   explicit — requirement or section ID → case IDs. Anything with zero cases is either
   an oversight or out of scope, and both need saying out loud.
2. **No two cases test the same thing.** Duplicates inflate the count and the
   maintenance burden while adding no coverage.
3. **The mix is honest.** A suite that is 90% happy path is not coverage. Negative and
   boundary cases are where the defects are; if the plan promised them, the output must
   contain them.

---

## Spotting gaps in the requirements

Reading a spec closely surfaces things the author left undecided. Report these — a QA
lead who returns a list of holes alongside the cases is more valuable than one who
silently guesses. Flag a requirement when it is:

- **Untestable as written** — no observable outcome ("the system should be fast",
  "the UI should be intuitive"). Ask for the number or the criterion.
- **Ambiguous** — more than one reasonable reading ("the user is notified" — by email,
  push, in-app? immediately or batched?).
- **Contradictory** — two sections disagree ("limit is 100 000" vs. a later example
  showing 150 000 succeeding).
- **Silent on the error path** — the success flow is fully described and the failure
  flow is not mentioned at all. This is the most common gap.
- **Missing a rule the tests need** — rounding, time zone, currency conversion,
  retention period, permission matrix.
- **A gating term that is never defined** — the spec makes an outcome depend on a status
  or role it never specifies ("available to a *verified* user", "*premium* accounts may
  export"). It reads as understood, so it survives review, and then nobody can build the
  precondition. Ask where the state is set, how a tester puts an account into it, and what
  the user sees without it. This one hides in plain sight: if a phrase keeps landing in
  your preconditions and the spec never defines it, that is the gap.
- **An external dependency whose failure is unspecified** — the spec names a payment
  provider, an SMS gateway or a third-party API, describes the happy path, and says
  nothing about a timeout, a rejection or an outage. Writing a resilience case from
  experience is not enough; the missing decision belongs in the gap list, because only
  the analyst can say whether the operation retries, fails, or holds the funds.

Report them as a short list with the section reference and the specific question. Where
a gap blocks a case, write the case against a stated assumption and mark the assumption
rather than dropping the coverage.
