import type { Guest, Meals } from "../types";

export const buildMealSchedule = (guests: Guest[]): Meals[] => {
  const dedupeDates = Array.from(
    new Set(
      guests
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
        .map((g) => g.date),
    ),
  );
  return dedupeDates.map((d) => {
    const names = guests.filter((g) => g.date === d).map((g) => g.name);
    return {
      date: d,
      names,
    };
  });
};
