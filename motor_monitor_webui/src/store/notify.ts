import { writable } from "svelte/store";
import type { NotifyIcon, NotifyLevel } from "../lib/model/notify";

export const notify = writable({
  info: (
    message: string,
    option?: {
      title?: string;
      icon?: NotifyIcon;
    }
  ) => {
    console.warn("Notify not initialized");
  },
  error: (
    message: string,
    option?: {
      title?: string;
      icon?: NotifyIcon;
    }
  ) => {
    console.warn("Notify not initialized");
  },
  success: (
    message: string,
    option?: {
      title?: string;
      icon?: NotifyIcon;
    }
  ) => {
    console.warn("Notify not initialized");
  },
  warning: (
    message: string,
    option?: {
      title?: string;
      icon?: NotifyIcon;
    }
  ) => {
    console.warn("Notify not initialized");
  },
});
