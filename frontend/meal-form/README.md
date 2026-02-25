# 🍽️ Guest Meal Schedule — React Challenge

A small React application that collects guest stay data and derives a daily meal schedule.

This project is part of my Full Stack Practice repository and focuses on:

- Pure data derivation
- Deterministic date handling
- Immutable state updates
- Clean separation between UI and logic
- Test-driven development

## 🧠 Problem

Guests enter:

- Name
- Check-in date
- Check-out date

The application generates a daily meal schedule showing which guests receive meals on each date.

The schedule is grouped by date and sorted ascending.

Example output:

| Date       | Guests         |
| ---------- | -------------- |
| 2026-02-01 | ["Jon"]        |
| 2026-02-02 | ["Jon", "Amy"] |
| 2026-02-03 | ["Amy"]        |

## 📏 Business Rules

### Date Inclusion Rule

Meals are generated for every date from:

check-in (inclusive) → check-out (inclusive)

Example:

- Check-in: 2026-02-01
- Check-out: 2026-02-03

Produces:

- 2026-02-01
- 2026-02-02
- 2026-02-03

(3 total days)

## 🧱 Architecture

### Core Pure Functions

Located in lib/:

- buildGuestsArray(name, checkIn, checkOut)
- buildMealSchedule(guests)

These functions:

- Contain no React logic
- Perform no side effects
- Are fully testable in isolation

### React Layer

- Controlled form inputs
- Immutable state updates
- Derived meal schedule from current state

## 🧪 Testing

Built with Vitest.

### Unit tests include

- Correct date expansion across a range
- Correct grouping by date
- No duplicate dates in meal schedule
- Chronological sorting
- Validation of invalid date ranges

Run tests:

```Bash
npm run test
```

## ⚠️ Edge Case Handling

- Invalid date ranges throw errors
- Empty names are rejected
- Date stepping avoids timezone drift (UTC-safe parsing)
- Input data is never mutated

## 🚀 Running Locally

```Bash
npm install
npm run dev
```

## Running with Docker

Build:

```Bash
docker build -t guest-meal-schedule .
```

Run:

```Bash
docker run -p 3000:3000 guest-meal-schedule
```
