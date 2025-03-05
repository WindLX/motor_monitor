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

export const motorPositionStore = derived(motorStateStore, ($motorStateStore) => {
    const motorPosition = $motorStateStore.map((item) => {
        const positions: Record<number, number> = {};
        for (const [key, motor] of Object.entries(item)) {
            positions[Number(key)] = motor.position;
        }
        return positions;
    });
    return motorPosition;
});
export const latestMotorPositionStore = derived(motorPositionStore, ($latestMotorStateStore) => {
    if ($latestMotorStateStore.length === 0) {
        return null;
    }
    return $latestMotorStateStore[$latestMotorStateStore.length - 1];
});

export const motorVelocityStore = derived(motorStateStore, ($motorStateStore) => {
    const motorVelocity = $motorStateStore.map((item) => {
        const velocities: Record<number, number> = {};
        for (const [key, motor] of Object.entries(item)) {
            velocities[Number(key)] = motor.velocity;
        }
        return velocities;
    });
    return motorVelocity;
});
export const latestMotorVelocityStore = derived(motorVelocityStore, ($latestMotorStateStore) => {
    if ($latestMotorStateStore.length === 0) {
        return null;
    }
    return $latestMotorStateStore[$latestMotorStateStore.length - 1];
});

export const motorCurrentStore = derived(motorStateStore, ($motorStateStore) => {
    const motorCurrent = $motorStateStore.map((item) => {
        const currents: Record<number, number> = {};
        for (const [key, motor] of Object.entries(item)) {
            currents[Number(key)] = motor.current;
        }
        return currents;
    });
    return motorCurrent;
});
export const latestMotorCurrentStore = derived(motorCurrentStore, ($latestMotorStateStore) => {
    if ($latestMotorStateStore.length === 0) {
        return null;
    }
    return $latestMotorStateStore[$latestMotorStateStore.length - 1];
});