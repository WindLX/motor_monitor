// svelte
import { writable, derived } from "svelte/store";
// lib
import MotorMonitorAPI from "../lib/api";
import {
  MotorMessageTypeEnum,
  StateMachineStateEnum,
  type QS_M_STATE_Payload,
  type QS_SM_STATE_Payload,
} from "../lib/model/base";
// store
import { messageManager } from "./instance";

export const apiConnected = writable<boolean>(false);
export const wsConnected = writable<boolean>(false);
export const downstreamConnected = writable<boolean>(false);

export const motorStateStore = writable<Array<QS_M_STATE_Payload>>;
export const stateMachineStateStore = writable<QS_SM_STATE_Payload>({
  state: StateMachineStateEnum.SM_UNKNOWN,
});
