import { expect, test } from "vitest";
import { buildMealSchedule } from "../lib/buildMealSchedule";
import { buildGuestsArray } from "../lib/buildGuestsArray";

test("Should generate an array with no duplicate dates", () => {
  const name1 = "Jon";
  const checkIn1 = "2026-02-01";
  const checkOut1 = "2026-02-03";
  const arr1 = buildGuestsArray(name1, checkIn1, checkOut1);

  const name2 = "Jon";
  const checkIn2 = "2026-02-01";
  const checkOut2 = "2026-02-04";
  const arr2 = buildGuestsArray(name2, checkIn2, checkOut2);

  const guests = [...arr1, ...arr2];

  const meals = buildMealSchedule(guests);

  // First element's names array has 2 names
  expect(meals[0].names.length).toBe(2);

  // Last element's names array has 1 name
  expect(meals[meals.length - 1].names.length).toBe(1);

  //   last element's date is after first
  expect(new Date(meals[meals.length - 1].date).getTime()).toBeGreaterThan(
    new Date(meals[0].date).getTime(),
  );

  //   Meal plan array is smaller than guests array
  expect(meals.length).toBeLessThan(guests.length);
});
