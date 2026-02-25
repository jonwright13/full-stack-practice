import { useMemo, useState } from "react";
import "./App.css";
import type { Guest, GuestFormElement, Meals } from "./types";
import { buildMealSchedule } from "./lib/buildMealSchedule";
import { buildGuestsArray } from "./lib/buildGuestsArray";

function App() {
  const [guests, setGuests] = useState<Guest[]>([]);

  const onSubmit = (e: React.SubmitEvent<GuestFormElement>) => {
    e.preventDefault();

    const form = e.currentTarget;
    const formElements = form.elements;

    const name = formElements.name.value;
    if (name.length === 0) {
      alert("Name must be provided");
      return;
    }

    const checkIn = formElements["check-in"].value;
    const checkOut = formElements["check-out"].value;

    if (!checkIn || !checkOut) {
      alert("Check in and check out dates must be provided");
      return;
    }

    if (checkOut <= checkIn) {
      alert("Check out date must be ahead of check in date");
      return;
    }

    const guestsArr = buildGuestsArray(name, checkIn, checkOut);

    setGuests((prev) => [...prev, ...guestsArr]);
    form.reset();
  };

  const mealPlan: Meals[] = useMemo(() => buildMealSchedule(guests), [guests]);

  return (
    <>
      <div className="container">
        <h1>Check In Form</h1>
        <div className="divider" />
        <form onSubmit={onSubmit}>
          <div className="form">
            <label htmlFor="name">Name:</label>
            <input name="name" required />
            <label htmlFor="check-in">Check In</label>
            <input name="check-in" type="date" required />
            <label htmlFor="check-out">Check Out</label>
            <input name="check-out" type="date" required />
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
      {mealPlan.length > 0 && (
        <div className="meals-container">
          <h2>Meal Plan</h2>
          <table>
            <tr>
              <th>Date</th>
              <th>Name</th>
            </tr>
            {mealPlan.map((d) => (
              <tr key={d.date}>
                <td>{d.date}</td>
                <td>
                  {d.names.map((n) => (
                    <p key={n}>{n}</p>
                  ))}
                </td>
              </tr>
            ))}
          </table>
        </div>
      )}
    </>
  );
}

export default App;
