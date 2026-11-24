# Copy review — `Inbox`

Style: `software` (SaaS / web app), judged from the snippet alone — React web component, toast + spinner, an `/api/mail` list, English product UI. No repo and no `docs/copy-glossary.md` to override it, so names are checked against the skill defaults only. English surface, so the Chinese punctuation/spacing rules don't apply; the English-side rules come from the software file (GitHub Primer on tone, AWS Cloudscape on empty/loading, WCAG 2.1 on status messages).

Line numbers below are the snippet's own lines. Nothing is rewritten; each row gives only the smallest wording change, and says when the fix touches a state branch.

## What each state shows today

| State | The user sees |
|---|---|
| Loading | `Inbox · 0 messages` · `Showing up to 20 messages.` · a bare spinner |
| Success, 1 item | `Inbox · 1 messages` |
| Success, 20 items | `Inbox · 20 messages` · `Showing up to 20 messages.` · the list |
| Empty (request OK, no items) | `Inbox · 0 messages` · `Showing up to 20 messages.` · `Oops! Nothing here yet 🙂` |
| Failed (network, JSON parse, HTTP error) | a toast of the raw `e.message`, then the same `Oops! Nothing here yet 🙂` block |
| More than 20 on the server | `Inbox · 20 messages` · `Showing up to 20 messages.` · no way to reach 21+ |

## Problems

| # | Type | Copy and location | Smallest fix |
|---|---|---|---|
| 1 | Failure rendered as empty | L19 `toast.error(e.message)` is the only failure handling: `mail` stays `[]`, `loading` flips to false, so L27 falls through to `<Empty text="Oops! Nothing here yet 🙂" />` — a failed load tells the user the inbox is empty | Add an error branch that renders inline `Couldn't load messages. Try again.` + Retry; keep `Empty` for "request OK, 0 items" only (state branch) |
| 2 | Truncation reported as a total | L25 `<h3>Inbox · {mail.length} messages</h3>` — `mail.length` is capped by L11 `limit=${PAGE}`, so 20 messages reads as "your inbox has 20 messages" when the server may have hundreds | `First {mail.length} messages`, or `{d.total} messages` if the response carries a total |
| 3 | Count shown before there is one | L25 + L27: while loading, and after a failure, the header reads `Inbox · 0 messages`; the number then jumps to 20 | Render the count only after a successful response; plain `Inbox` while loading and on error (state branch) |
| 4 | Exception text in the UI | L19 `toast.error(e.message)` — that string is `Failed to fetch`, or, because `r.ok` is never checked (L12), V8's `Unexpected token '<' … is not valid JSON`; a `{error: …}` body makes `setMail(undefined)` at L15 and `mail.length` at L25 then throws with no copy at all | Never pass `e.message` through; fixed sentence `Couldn't load messages. Try again.` [fill: escalation path if the product has one] |
| 5 | Empty state without a next step | L27 `Oops! Nothing here yet 🙂` — no object name (`messages` everywhere else), and nothing the user can do next | `No messages yet.` + one next step [fill: the action this page offers] |
| 6 | Tone on a neutral state | same string: `Oops!` reads as "something went wrong" (and here it literally is the failure screen too), `🙂` is announced by screen readers as "slightly smiling face" | Drop `Oops!` and `🙂` |
| 7 | No loading copy, none announced | L27 `<Spinner />` — a spinner with no text and no live region, so nothing says what is loading and screen-reader users get no status change | `Loading messages` inside a `role="status"` element (state branch) |
| 8 | Plural | L25 `{mail.length} messages` renders `1 messages` | Pluralize: `1 message` / `20 messages` |
| 9 | Limit restated, no next step | L26 `Showing up to {PAGE} messages.` — repeats the cap already in L25, in vaguer words ("up to"), and offers no way forward | State the cap once, next to the control that shows more (`First 20 messages` + `View all`); if no such control exists, delete the line |

Minor:
- L26 `Showing up to 20 messages.` — a one-line hint takes no final period.
- L25 — the count sits inside the `h3`, so the heading text changes once data lands. Put the count next to the heading rather than in it.

## Checked, nothing wrong
- `20` in the hint matches `PAGE = 20` and the request's `limit` (L11, L26) — no stale number.
- The object has one name wherever it is named: `messages`.
- No `aria-label`, `title`, `placeholder` or `alt` in this component, so there is nothing to check there.
- The snippet ships no tests or gates, so none of these strings is anchored; no item needs a naming ruling.

## Needs your call
1. Does `/api/mail` return a total, or only `items`? That decides 2 and 3 (real count vs. "first N").
2. Is 20 a hard cap, or is there a paging / load-more path? If it is hard, messages 21+ are unreachable — a product gap, not a copy one.
3. Is `Inbox` the product's own name for this surface, or is it `Mail` / `Messages`? Nothing in the snippet anchors it.

Fixes 1, 3 and 7 touch a state branch, not only strings; the rest are string-only. Want me to apply them?
