// svelte
import { writable, derived } from "svelte/store";
// lib
import MotorMonitorAPI from "../lib/api";
import type { MotorStateRecord } from "../lib/model";
// assets
import { http_server, ws_server } from "../assets/config.json";

export const motorMonitorAPI = writable<MotorMonitorAPI>(new MotorMonitorAPI(http_server, ws_server));
export const apiConnected = writable<boolean>(false);
export const wsConnected = writable<boolean>(false);
export const downstreamConnected = writable<boolean>(false);

export const motorStateStore = writable<Array<Record<number, MotorStateRecord>>>([]);
export const latestMotorStateStore = derived(motorStateStore, ($motorStateStore) => {
    if ($motorStateStore.length === 0) {
        return null;
    }
    return $motorStateStore[$motorStateStore.length - 1];
});

export function resetAPI() {
    motorMonitorAPI.update((api) => {
        api = new MotorMonitorAPI(http_server, ws_server);
        return api;
    });
}