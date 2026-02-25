React Challenge: Guest Stays → Daily Meal Schedule

Build a small React app that takes guest stay info from a form and renders a derived Meal Schedule table grouped by date, where each day shows an array/list of guest names who should receive meals that day.

Core idea

User submits stays: name + check-in date + check-out date

App expands each stay into daily meal entries

UI shows a table like:

Date Guests with meals
2026-03-01 ["Aisha", "Ben"]
2026-03-02 ["Aisha"]

Sorted ascending by date.

Requirements

1. Form

Fields:

Guest name (string)

Check-in date (YYYY-MM-DD)

Check-out date (YYYY-MM-DD)

Buttons:

Add Stay

(Optional) Clear All

Validation (minimum):

Name required (trimmed, non-empty)

Both dates required

checkOut must be after checkIn (see rules below)

2. State + Data model

Maintain a list of stays, e.g.

{ id, name, checkIn, checkOut } 3) Meal schedule derivation

Generate a map keyed by date:

Record<YYYY-MM-DD, string[]>

And render it as a sorted list of rows by date.

Meal inclusion rule (pick this exact rule for determinism)

Meals are provided for every night stayed, i.e. for dates from checkIn (inclusive) up to checkOut (exclusive).

Example:

Check-in: 2026-03-01

Check-out: 2026-03-03
→ meals on 2026-03-01 and 2026-03-02 (2 days)

This avoids ambiguity around checkout day.

Sorting rules

Table sorted by date ascending.

Guest names within each date sorted alphabetically (case-insensitive).

If the same guest is added twice for the same day (duplicate stays), show the name once (dedupe per day).

Suggested constraints (to make it “interview-real”)
Architecture constraints

Derivation must be pure: schedule computed from stays via a function like buildMealSchedule(stays).

No mutation of existing state (immutable updates only).

Use controlled inputs.

No date libraries (no Moment/dayjs). Use native Date + careful YYYY-MM-DD handling OR string-based date stepping you implement.

UX constraints

Validation errors must render inline and block submission.

Reset form after successful add.

Show empty state: “No stays yet” / “No meals scheduled”.

Edge-case constraints

Support overlapping stays (multiple guests same day).

Support same guest with multiple stays (dedupe per day, but allow multiple stays in list).

Treat names case-insensitively for dedupe (“Sam” == “sam”).

Ensure no timezone drift: treat YYYY-MM-DD as a date key, not a datetime.

Optional stretch constraints

Allow deleting a stay and ensure schedule updates.

Allow editing a stay.

Add a “Guests” list above the meal schedule to verify raw state.

Tests to include (React Testing Library + Vitest/Jest)
Unit tests (pure function)

buildMealSchedule(stays)

Single stay expands correctly

(2026-03-01 → 2026-03-03) includes 01 and 02 only.

Multiple guests same day

Two stays overlapping produce both names in that day.

Sorted dates

Input stays out of order → output date keys sorted.

Sorted names

Names appear alphabetically per day.

Dedup per day

Same guest overlapping stays does not duplicate name for the same date.

Case-insensitive dedupe

“Sam” and “sam” collapse to one entry.

Empty input

Returns empty schedule.

Component tests (integration)

Form validation: empty submit

Shows error messages for name/dates.

Form validation: checkout <= checkin

Blocks submit and shows message.

Successful add

Stay appears in stays list (if you render it) and meal schedule table rows appear.

Derived table updates

Add a second stay → table updates correctly without refresh.

Reset behavior

After adding, inputs clear.

Delete stay (if implemented)

Removing a stay updates meal schedule.

Deliverables (what “done” means)

buildMealSchedule.ts (pure logic)

App.tsx with form + table

Tests for derivation + UI

Minimal styling (readable table + errors)

If you want, I can also write the exact buildMealSchedule() spec (date stepping algorithm + dedupe/sorting behavior) as a “contract” so implementation stays crisp.
