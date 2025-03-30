// svelte
import { writable } from "svelte/store";
// lib
import {
  StateMachineStateEnum,
  type QS_M_STATE_Payload,
  type QS_SM_STATE_Payload,
} from "../lib/model/base";
// store
import { ConnectStatus } from "../lib/model/status";

export const apiConnectStatus = writable<ConnectStatus>(
  ConnectStatus.DISCONNECTED
);
export const motorStateWsConnectStatus = writable<ConnectStatus>(
  ConnectStatus.DISCONNECTED
);
export const stateMachineWsConnectStatus = writable<ConnectStatus>(
  ConnectStatus.DISCONNECTED
);
export const downstreamConnectStatus = writable<ConnectStatus>(
  ConnectStatus.DISCONNECTED
);

export const motorStateStore = writable<Array<QS_M_STATE_Payload>>([]);
export const stateMachineStateStore = writable<QS_SM_STATE_Payload>({
  state: StateMachineStateEnum.SM_UNKNOWN,
});
