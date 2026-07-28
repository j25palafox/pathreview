# PathReview Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/43

**Issue title:** Agent session state is not cleared between reviews for the same user

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**

PathReview stores agent session state so that the agent can retain context during a portfolio review. Currently, that state is not cleared when the same user begins a different review, which can cause information from the previous review to carry over into the new one. The problem appears to involve the session-management logic in `agent/memory/session_store.py`. A successful fix will ensure that each new review begins with clean agent state while preserving context appropriately within an active review.

**Branch name:** `fix/43-clear-agent-session-state`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

### Selection Notes — Is This Issue Right for Me?

#### Part 1 — Understanding the Issue

**Can I explain what this issue is asking for in my own words?**

Yes. PathReview stores agent session state using the user ID, but that state is not cleared when the same user begins a different portfolio review. As a result, the agent may reuse messages or tool results from an earlier review instead of evaluating the newly updated portfolio. The expected behavior is for context to remain available within one active review while each new review starts with clean, isolated state.

**Do I understand which part of the app is affected?**

Yes. The issue is labeled `agent` and identifies `agent/memory/session_store.py` as the primary affected file. I located the file in the repository and reviewed the session-storage behavior described by the issue. The problem is specifically related to how agent state is associated with a user and reused across separate reviews.

**Do I understand what “done” looks like?**

Yes. Before the fix, a user who completes one review and then starts another may receive feedback influenced by state or tool results from the previous review. After the fix, starting a new review should create or load state belonging only to that review, while context should continue to persist normally during the active review. A regression test should confirm that state from one review is not available when the same user begins another review.

#### Part 2 — Tier Fit

**Is the tier a realistic match for where I am right now?**

Yes. Issue #43 is labeled Tier 1 and is described as a localized bug fix with an estimated effort of approximately 3–4 hours. This is my first contribution to this codebase, so choosing a focused Tier 1 issue is appropriate. The issue will still require me to trace the session lifecycle, understand the affected code, and add a regression test without requiring a broad change to the entire agent architecture.

#### Part 3 — Codebase Readiness

**Can I find the relevant code?**

Yes. I located `agent/memory/session_store.py`, the file identified by the issue, and reviewed the section responsible for storing and retrieving agent session state. I understand that the current state is associated with the user in a way that allows it to survive across separate reviews.

**Do I understand the surrounding code well enough to change it safely?**

I understand enough of the surrounding behavior to form an initial approach without assuming the final implementation. I need to trace where a new portfolio review is created and how that code interacts with the session store. The likely fix will involve giving separate reviews isolated state or explicitly clearing the existing state when a new review begins, while ensuring that state is not cleared during an active review.

**Have I read the relevant test file?**

There is not currently a dedicated test file for the affected session-store behavior. I reviewed the existing unit-test organization in the repository to understand where agent-related tests belong and how tests are structured. As part of the fix, I plan to create a new test file for the session store and add a regression test showing that state from one review is not reused when the same user begins another review.


#### Part 4 — Scope and Time

**How many others are already working on this issue?**

I checked both the issue comments and the cohort ledger. The ledger showed eight claims for Issue #43 when I reviewed it. Claims are non-exclusive, and I am comfortable continuing with the issue because my grade will be based on my own investigation, journal, implementation, tests, and pull request.

**Is the scope realistic for Weeks 8–9?**

Yes. The issue estimates approximately 3–4 hours of focused implementation work, although I am allowing additional time for reproduction, code exploration, testing, documentation, and addressing unexpected behavior. The scope is realistic within the Week 8 investigation and Week 9 implementation timeline.

**Are there any blockers or dependencies?**

The issue does not identify another unresolved GitHub issue or pull request that must be completed first. My initial local setup dependencies included creating the Python virtual environment and starting the project’s Docker services, including PostgreSQL and Redis. Those services are now running correctly, and the application launches locally, so I do not currently have a setup blocker preventing me from investigating the issue.

#### Verdict

This issue is a good fit for my current experience and the Module 3 timeline. I understand the incorrect behavior, have identified the affected area of the codebase, can describe the expected before-and-after behavior, and have a reasonable starting point for reproducing and testing the bug. The Tier 1 scope is appropriately focused for a first contribution to PathReview, so I am comfortable proceeding with Issue #43.


## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [Document review orchestration feature gap](https://github.com/j25palafox/pathreview/commit/f852ec9)

**Reproduction summary:**
I traced review creation from `create_review_endpoint()` through `process_review()` and found that `_run_agent_orchestration()` currently returns hardcoded output instead of invoking the real `Orchestrator`, preventing an end-to-end reproduction through the application. In the isolated orchestrator code, I observed that one persistent `ContextManager` is reused across `run()` calls and that Redis session state is keyed only by `profile_id`, so separate reviews are not isolated by a review identifier.

**PLAN.md link:** [PLAN.md](https://github.com/j25palafox/pathreview/blob/fix/43-clear-agent-session-state/PLAN.md)

**Blockers or open questions:**
I still need to confirm whether the intended fix is to reset context on every call to `Orchestrator.run()`, add a `review_id` to the orchestration and session APIs, or instantiate a new orchestrator for each review. I also need to determine whether replacing the placeholder implementation in `core/services/review_service.py` belongs within Issue #43 or should be handled as separate integration work.
