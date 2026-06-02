import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * useIndexedDB
 *
 * A typed IndexedDB hook used in the ODEN PWA to cache GIS feature data,
 * permit records, and field notes for offline-first operation.
 *
 * Supports:
 * - Typed get/set/delete operations with full TypeScript generics
 * - Multiple object stores per database
 * - Automatic DB version management
 * - Loading and error state tracking
 *
 * @example
 * const { get, set, remove, loading } = useIndexedDB<PermitRecord>('oden-db', 'permits');
 */

interface UseIndexedDBReturn<T> {
  get: (key: IDBValidKey) => Promise<T | undefined>;
  set: (key: IDBValidKey, value: T) => Promise<void>;
  remove: (key: IDBValidKey) => Promise<void>;
  getAll: () => Promise<T[]>;
  clear: () => Promise<void>;
  loading: boolean;
  error: Error | null;
}

interface StoreConfig {
  storeName: string;
  keyPath?: string;
  autoIncrement?: boolean;
}

function openDatabase(
  dbName: string,
  version: number,
  stores: StoreConfig[]
): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(dbName, version);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      for (const store of stores) {
        if (!db.objectStoreNames.contains(store.storeName)) {
          db.createObjectStore(store.storeName, {
            keyPath: store.keyPath,
            autoIncrement: store.autoIncrement ?? false,
          });
        }
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export function useIndexedDB<T>(
  dbName: string,
  storeName: string,
  version = 1
): UseIndexedDBReturn<T> {
  const dbRef = useRef<IDBDatabase | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    openDatabase(dbName, version, [{ storeName }])
      .then((db) => {
        dbRef.current = db;
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err);
        setLoading(false);
      });

    return () => {
      dbRef.current?.close();
      dbRef.current = null;
    };
  }, [dbName, storeName, version]);

  const withStore = useCallback(
    <R>(
      mode: IDBTransactionMode,
      operation: (store: IDBObjectStore) => IDBRequest<R>
    ): Promise<R> => {
      return new Promise((resolve, reject) => {
        if (!dbRef.current) {
          reject(new Error('IndexedDB not initialized'));
          return;
        }
        const tx = dbRef.current.transaction(storeName, mode);
        const store = tx.objectStore(storeName);
        const request = operation(store);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    },
    [storeName]
  );

  const get = useCallback(
    (key: IDBValidKey) => withStore<T | undefined>('readonly', (store) => store.get(key)),
    [withStore]
  );

  const set = useCallback(
    (key: IDBValidKey, value: T): Promise<void> =>
      withStore<IDBValidKey>('readwrite', (store) => store.put(value, key)).then(() => undefined),
    [withStore]
  );

  const remove = useCallback(
    (key: IDBValidKey): Promise<void> =>
      withStore<undefined>('readwrite', (store) => store.delete(key)),
    [withStore]
  );

  const getAll = useCallback(
    () => withStore<T[]>('readonly', (store) => store.getAll()),
    [withStore]
  );

  const clear = useCallback(
    (): Promise<void> =>
      withStore<undefined>('readwrite', (store) => store.clear()),
    [withStore]
  );

  return { get, set, remove, getAll, clear, loading, error };
}
