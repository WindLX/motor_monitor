import { writable } from "svelte/store";
import type { NotifyLevel } from "../lib/utils";

export const notify = writable(
    {
        notify: (message: string, level: NotifyLevel) => {
            console.warn('Notify not initialized');
        },
        info: (message: string) => {
            console.warn('Notify not initialized');
        },
        error: (message: string) => {
            console.warn('Notify not initialized');
        },
        success: (message: string) => {
            console.warn('Notify not initialized');
        },
        warning: (message: string) => {
            console.warn('Notify not initialized');
        },
    }
)