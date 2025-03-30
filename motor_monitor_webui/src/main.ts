import { mount } from "svelte";
import "./app.css";
import App from "./App.svelte";

import { library } from "@fortawesome/fontawesome-svg-core";
import { iconLibrary } from "./lib/icon";

library.add(...iconLibrary);

const app = mount(App, {
  target: document.getElementById("app")!,
});

export default app;
