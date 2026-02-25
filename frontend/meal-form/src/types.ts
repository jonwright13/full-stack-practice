export interface Guest {
  name: string;
  date: string;
}
export interface Meals {
  date: string;
  names: string[];
}
interface FormElements extends HTMLFormControlsCollection {
  name: HTMLInputElement;
  "check-in": HTMLInputElement;
  "check-out": HTMLInputElement;
}
export interface GuestFormElement extends HTMLFormElement {
  readonly elements: FormElements;
}
