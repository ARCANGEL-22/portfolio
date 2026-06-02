import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * useApiFetch
 *
 * A flexible, caching API fetch hook used across the Make-Ready Workstation
 * and ODEN PWA to pull data from Katapult Pro, ArcGIS, and internal APIs.
 *
 * Features:
 * - In-memory cache with configurable TTL (time-to-live)
 * - Automatic abort on component unmount or URL change
 * - Loading, error, and data states
 * - Manual refetch trigger
 * - Generic type safety
 *
 * @example
 * const { data, loading, error, refetch } = useApiFetch<Job[]>(
 *   'https://api.katapultpro.com/jobs',
 *   { headers: { Authorization: 'Bearer ...' }, cacheTTL: 60000 }
 * );
 */

interface FetchOptions extends RequestInit {
  cacheTTL?: number;
  enabled?: boolean;
}

interface UseApiFetchReturn<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

const cache = new Map<string, CacheEntry<unknown>>();

export function useApiFetch<T>(
  url: string | null,
  options: FetchOptions = {}
): UseApiFetchReturn<T> {
  const { cacheTTL = 0, enabled = true, ...fetchOptions } = options;

  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [tick, setTick] = useState(0);

  const abortRef = useRef<AbortController | null>(null);

  const refetch = useCallback(() => {
    if (url) cache.delete(url);
    setTick((t) => t + 1);
  }, [url]);

  useEffect(() => {
    if (!url || !enabled) return;

    if (cacheTTL > 0) {
      const cached = cache.get(url) as CacheEntry<T> | undefined;
      if (cached && Date.now() - cached.timestamp < cacheTTL) {
        setData(cached.data);
        setLoading(false);
        setError(null);
        return;
      }
    }

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setLoading(true);
    setError(null);

    fetch(url, { ...fetchOptions, signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) throw new Error('HTTP ' + res.status + ': ' + res.statusText);
        const json = (await res.json()) as T;
        if (cacheTTL > 0) cache.set(url, { data: json, timestamp: Date.now() });
        setData(json);
        setLoading(false);
      })
      .catch((err: Error) => {
        if (err.name === 'AbortError') return;
        setError(err);
        setLoading(false);
      });

    return () => { controller.abort(); };
  }, [url, enabled, tick, cacheTTL]);

  return { data, loading, error, refetch };
}

export function clearApiFetchCache(): void { cache.clear(); }
export function invalidateApiFetchCache(url: string): void { cache.delete(url); }
