import type { MotorMessageTypeEnum } from "./model/base";
import type { MotorNetMessageResponse } from "./model/net";

class MotorNetMessageManager {
  private messageQueue: Array<MotorNetMessageResponse>;
  private maxMessageQueueLength: number;

  private onMessageAdded: (message: MotorNetMessageResponse) => void;

  constructor(maxMessageQueueLength: number = 100) {
    this.maxMessageQueueLength = maxMessageQueueLength;
    this.messageQueue = [];
    this.onMessageAdded = () => {};
  }

  public subscribeOnMessageAdded(
    callback: (message: MotorNetMessageResponse) => void
  ): () => void {
    this.onMessageAdded = callback;
    return () => {
      this.onMessageAdded = () => {};
    };
  }

  public addMessage(message: MotorNetMessageResponse) {
    if (
      this.messageQueue.length >= this.maxMessageQueueLength &&
      this.maxMessageQueueLength > 0
    ) {
      this.messageQueue.shift();
    }
    this.messageQueue.push(message);
    this.onMessageAdded(message);
  }

  public clearMessage() {
    this.messageQueue = [];
  }

  public get messageQueueLength(): number {
    return this.messageQueue.length;
  }

  public get allMessages(): Array<MotorNetMessageResponse> {
    return this.messageQueue;
  }

  public static getMessageId(message: MotorNetMessageResponse): string {
    return message.raw_message.id;
  }

  public static getMessageTimestamp(message: MotorNetMessageResponse): number {
    return message.raw_message.timestamp;
  }

  public static getMessageType(
    message: MotorNetMessageResponse
  ): MotorMessageTypeEnum {
    return message.raw_message.message_type;
  }

  public getByIndex(index: number): MotorNetMessageResponse | null {
    if (index < 0 || index >= this.messageQueue.length) {
      return null;
    }
    return this.messageQueue[index];
  }

  public getByUUID(id: string): MotorNetMessageResponse | null {
    for (const message of this.messageQueue) {
      if (message.raw_message.id === id) {
        return message;
      }
    }
    return null;
  }

  public getByTimestamp(timestamp: number): MotorNetMessageResponse | null {
    for (const message of this.messageQueue) {
      if (message.raw_message.timestamp === timestamp) {
        return message;
      }
    }
    return null;
  }

  public filter(
    predicate: (message: MotorNetMessageResponse) => boolean
  ): Array<MotorNetMessageResponse> {
    return this.messageQueue.filter(predicate);
  }
}

export default MotorNetMessageManager;
