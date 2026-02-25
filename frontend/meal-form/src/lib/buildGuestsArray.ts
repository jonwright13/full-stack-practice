import type { Guest } from "../types";

export const buildGuestsArray = (
  name: string,
  checkIn: string,
  checkOut: string,
): Guest[] => {
  if (checkIn > checkOut) {
    throw new Error("Check in date should be before check out date");
  }

  if (isNaN(Date.parse(checkIn)) || isNaN(Date.parse(checkOut))) {
    throw new Error("Invalid date supplied");
  }

  let guestsArr: Guest[] = [];
  for (
    let d = new Date(checkIn);
    d <= new Date(checkOut);
    d.setDate(d.getDate() + 1)
  ) {
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = String(d.getFullYear());

    const guest: Guest = {
      name,
      date: `${year}-${month}-${day}`,
    };

    guestsArr.push(guest);
  }

  return guestsArr;
};
