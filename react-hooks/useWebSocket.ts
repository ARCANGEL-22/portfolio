import { useEffect, useRef, useState, useCallback } from 'react';

/**
 * useWebSocket
 *
 * A production-ready WebSocket hook used in the ODEN PWA for real-time
 * field note synchronization across 60+ concurrent engineer sessions.
 *
 * Features:
 * - Automatic reconnection with exponential backoff
 * - Message queuing during disconnection
 * - Connection state tracking
 * - Cleanup on unmount
 *
 * @example
 * const { sendMessage, lastMessage, readyState } = useWebSocket('wss://api.example.com/ws');
 */

export type WebSocketStatus = 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED';

interface UseWebSocketOptions {
  reconnectAttempts?: number;
  reconnectInterval?: number;
  onOpen?: (event: Event) => void;
  onClose?: (event: CloseEvent) => void;
  onError?: (event: Event) => void;
}

interface UseWebSocketReturn<T> {
  sendMessage: (data: T) => void;
  lastMessage: T | null;
  readyState: WebSocketStatus;
  disconnect: () => void;
}

const READY_STATE_MAP: Record<number, WebSocketStatus> = {
  0: 'CONNECTING',
  1: 'OPEN',
  2: 'CLOSING',
  3: 'CLOSED',
};

export function useWebSocket<T = unknown>(
  url: string,
  options: UseWebSocketOptions = {}
): UseWebSocketReturn<T> {
  const {
    reconnectAttempts = 5,
    reconnectInterval = 2000,
    onOpen,
    onClose,
    onError,
  } = options;

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCount = useRef(0);
  const messageQueue = useRef<T[]>([]);
  const shouldReconnect = useRef(true);

  const [lastMessage, setLastMessage] = useState<T | null>(null);
  const [readyState, setReadyState] = useState<WebSocketStatus>('CLOSED');

  const flushQueue = useCallback(() => {
    while (messageQueue.current.length > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
      const queued = messageQueue.current.shift();
      if (queued !== undefined) {
        wsRef.current.send(JSON.stringify(queued));
      }
    }
  }, []);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(url);
    wsRef.current = ws;
    setReadyState('CONNECTING');

    ws.onopen = (event) => {
      setReadyState('OPEN');
      reconnectCount.current = 0;
      flushQueue();
      onOpen?.(event);
    };

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data) as T;
        setLastMessage(parsed);
      } catch {
        setLastMessage(event.data as unknown as T);
      }
    };

    ws.onclose = (event) => {
      setReadyState('CLOSED');
      onClose?.(event);

      if (shouldReconnect.current && reconnectCount.current < reconnectAttempts) {
        const backoff = reconnectInterval * Math.pow(2, reconnectCount.current);
        reconnectCount.current += 1;
        setTimeout(connect, backoff);
      }
    };

    ws.onerror = (event) => {
      onError?.(event);
    };
  }, [url, reconnectAttempts, reconnectInterval, onOpen, onClose, onError, flushQueue]);

  useEffect(() => {
    shouldReconnect.current = true;
    connect();

    return () => {
      shouldReconnect.current = false;
      wsRef.current?.close();
    };
  }, [connect]);

  const sendMessage = useCallback((data: T) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    } else {
      messageQueue.current.push(data);
    }
  }, []);

  const disconnect = useCallback(() => {
    shouldReconnect.current = false;
    wsRef.current?.close();
  }, []);

  return { sendMessage, lastMessage, readyState, disconnect };
}
