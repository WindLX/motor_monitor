// svelte
import { writable, readable, derived } from "svelte/store";
// lib
import MotorMonitorAPI from "../lib/api";
import type { MotorStateRecord } from "../lib/model";
// assets
import { http_server, ws_server } from "../assets/config.json";

export const motorMonitorAPI = readable<MotorMonitorAPI>(new MotorMonitorAPI(http_server, ws_server));
export const connected = writable<boolean>(false);

export const motorStateStore = writable<Array<Record<number, MotorStateRecord>>>([]);
export const latestMotorStateStore = derived(motorStateStore, ($motorStateStore) => {
    if ($motorStateStore.length === 0) {
        return null;
    }
    return $motorStateStore[$motorStateStore.length - 1];
});
