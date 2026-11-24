# UI copy review — `Inbox`

Problems only, no rewrites. Scope is the strings this component puts on screen and the states where it puts none.

## The heading: `Inbox · {mail.length} messages`

1. **The count is not a message count.** The list is fetched with `limit=20`, so `mail.length` can never exceed 20. An inbox with 500 messages reads "20 messages": the label claims a total it cannot know.
2. **Heading and hint describe the same number two incompatible ways** — one as a total ("N messages"), one as a cap ("up to 20"). Seeing "20 messages", a reader cannot tell "20 total" from "20 of 500".
3. **No pluralization.** One message renders "Inbox · 1 messages".
4. **It states a value before it has one.** `mail` starts as `[]`, so first paint says "0 messages" while the request is still in flight, then silently corrects itself. A guess is presented as a fact.
5. **It keeps stating "0" after a failure.** The catch leaves `mail` empty, so a failed load settles on "0 messages" — a false claim about the inbox instead of an error.
6. **It is stale by design.** The effect runs once (`[]` deps), so the number never changes after mount, yet it is presented as current inbox state.
7. **The unit is undefined.** "messages" doesn't say whether it means total, unread, or on-this-page — three readings a reader will consider.
8. **The name and the number are one fused, hard-coded string** with a decorative mid-dot. Translation can't reorder it, number formatting can't be applied to it, and screen readers get one run-on phrase ("Inbox middle dot twenty messages"). The section's only title is glued to live data, so there is no stable "Inbox" heading text anywhere.
9. **Changes to it are unannounced.** No live region, so the count mutating from 0 to N is silent to assistive tech.

## The hint: `Showing up to {PAGE} messages.`

10. **It exposes an implementation constant as user copy.** "20" is the fetch page size; readers don't need the limit.
11. **It is static, so it is wrong most of the time.** It renders unchanged next to "3 messages", next to an empty list, and during loading — "Showing up to 20 messages" over a list of 3.
12. **"up to" is hedging that carries no information.** It doesn't say which messages are shown, or whether more exist.
13. **It promises more than the UI delivers.** It implies the inbox may hold more, but there is no pagination, no load-more, no "showing 20 of N" — the copy points at an affordance that doesn't exist.
14. **It is redundant with the heading.** Two of the three copy elements in the section exist only to report quantity.
15. **Register and punctuation clash** with the terse heading and with the exclamation-and-emoji empty state: three voices in a four-line section.
16. **It appears in the loading state**, describing a list that hasn't arrived and where the body shows only a spinner.

## The empty state: `Oops! Nothing here yet 🙂`

17. **"Oops!" calls a normal state an error.** An empty inbox is not a mistake, and "Oops" is the vocabulary a user would expect for a failure — but the failure path doesn't own it.
18. **This is the copy users see after a failed load.** Errors only fire a transient toast, so once the toast disappears the screen reads "Oops! Nothing here yet 🙂" — a failed request is reported as an empty inbox.
19. **"Nothing here yet" doesn't name what is empty** and offers no explanation, no next step, no retry.
20. **"yet" is an unverifiable promise.** It tells the user messages are coming; for a genuinely empty account that is untrue.
21. **The emoji is a tone decision smuggled into a string.** `🙂` is announced by screen readers ("slightly smiling face"), renders differently per platform, can't be translated or dropped per locale, and reads as passive-aggressive after "Oops!".
22. **It is hard-coded into a `text` prop**, so one sentence has to serve "new user", "all read", "no results", and "load failed" alike, with no way to vary copy by context.
23. **Three tones in one sentence** — interjection, vague negation, emoji — matching nothing else on the screen.

## Copy that is missing or wrong in the other states

24. **There is no loading copy at all.** Loading renders a bare `<Spinner />`: no text status, nothing announced, and the heading meanwhile asserts "0 messages".
25. **Error copy is the raw exception.** `toast.error(e.message)` surfaces `Failed to fetch`, `Unexpected token '<', "<!DOCTYPE"... is not valid JSON`, or `undefined` when the rejection isn't an `Error` — internal text, in the runtime's language rather than the UI's, with no fallback and no statement of what failed.
26. **The error text describes the wrong failure.** With no `r.ok` check, an HTTP 500 surfaces as a JSON-parse message, and a changed payload (`d.items` undefined) surfaces the same way; what the user reads never matches what happened.
27. **The error has no persistent copy and no recovery copy.** After the toast clears, the failed state is visually identical to the empty state, and neither offers a retry.

## Cross-cutting

28. **No single voice.** Data label ("Inbox · 0 messages"), system hedge ("Showing up to 20 messages."), and chirpy exclamation ("Oops! Nothing here yet 🙂") sit in the same section.
29. **No localization seam.** Every string is an inline literal; counts are concatenated rather than formatted; there is no plural rule, and no key by which copy could be translated or varied.
30. **Terminology drifts.** The route says `mail`, the component says `Inbox`, the copy says "messages", and the empty state drops all three — the screen never settles on one name for what it lists.
31. **Nothing announces the state transitions.** Loading, the count settling, and the failure are all silent except for the toast, and the emoji adds unrequested verbosity to the one string that is read out.
