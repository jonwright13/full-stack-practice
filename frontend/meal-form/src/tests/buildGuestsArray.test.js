import { expect, test } from "vitest";
import { buildGuestsArray } from "../lib/buildGuestsArray";

test("Should generate an array of the right size with the check in and check out dates at either end", () => {
  const name = "Jon";
  const checkIn = "2026-02-01";
  const checkOut = "2026-02-03";
  const arr = buildGuestsArray(name, checkIn, checkOut);

  // Check length is 3
  expect(arr.length).toBe(3);

  // Confirm check in date is the first element while check out is the last
  expect(arr[0].date).toBe(checkIn);
  expect(arr[arr.length - 1].date).toBe(checkOut);

  // Check that there is only 1 day between the first and second element
  expect(
    new Date(arr[1].date).getDate() - new Date(arr[0].date).getDate(),
  ).toBe(1);
});

test("Later check in should throw error", () => {
  const name = "Jon";
  const checkIn = "2026-02-01";
  const checkOut = "2026-02-03";

  expect(() => buildGuestsArray(name, checkOut, checkIn)).toThrowError(
    "Check in date should be before check out date",
  );
});

test("Invalid date throws error", () => {
  const name = "Jon";
  const checkIn = "fsdfsdf";
  const checkOut = "2026-02-03";

  expect(() => buildGuestsArray(name, checkOut, checkIn)).toThrowError(
    "Invalid date supplied",
  );
});
