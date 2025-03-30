// svelte
import { writable, derived, readable } from "svelte/store";
// lib
import MotorMonitorAPI from "../lib/api";
import MotorNetMessageManager from "../lib/message";
// assets
import {
  motor_monitor_api,
  motor_net_message_manager,
} from "../assets/config.json";

export const motorMonitorAPI = writable<MotorMonitorAPI>(
  new MotorMonitorAPI(
    motor_monitor_api.http_server,
    motor_monitor_api.ws_server
  )
);

export function resetAPI() {
  motorMonitorAPI.update((api) => {
    api = new MotorMonitorAPI(
      motor_monitor_api.http_server,
      motor_monitor_api.ws_server
    );
    return api;
  });
}

export const messageManager = writable<MotorNetMessageManager>(
  new MotorNetMessageManager(motor_net_message_manager.max_message_queue_length)
);
