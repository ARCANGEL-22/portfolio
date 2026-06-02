import React, { useState, useMemo, useCallback } from 'react';

/**
 * DataTable - Generic sortable, filterable data table
 * Used in Make-Ready Workstation for pole data, clearance results, and permit checklists.
 */

export interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  render?: (row: T) => React.ReactNode;
  width?: string;
}

interface DataTableProps<T extends Record<string, unknown>> {
  columns: Column<T>[];
  data: T[];
  onRowClick?: (row: T) => void;
  loading?: boolean;
  emptyMessage?: string;
  searchable?: boolean;
  searchKeys?: (keyof T)[];
  rowKey: keyof T;
}

type SortDirection = 'asc' | 'desc' | null;

interface SortState<T> {
  key: keyof T | null;
  direction: SortDirection;
}

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  onRowClick,
  loading = false,
  emptyMessage = 'No data to display.',
  searchable = true,
  searchKeys,
  rowKey,
}: DataTableProps<T>) {
  const [sort, setSort] = useState<SortState<T>>({ key: null, direction: null });
  const [search, setSearch] = useState('');

  const handleSort = useCallback((key: keyof T) => {
    setSort((prev) => {
      if (prev.key !== key) return { key, direction: 'asc' };
      if (prev.direction === 'asc') return { key, direction: 'desc' };
      return { key: null, direction: null };
    });
  }, []);

  const filtered = useMemo(() => {
    if (!search.trim()) return data;
    const lower = search.toLowerCase();
    const keys = searchKeys ?? columns.map((c) => c.key);
    return data.filter((row) =>
      keys.some((k) => String(row[k] ?? '').toLowerCase().includes(lower))
    );
  }, [data, search, searchKeys, columns]);

  const sorted = useMemo(() => {
    if (!sort.key || !sort.direction) return filtered;
    return [...filtered].sort((a, b) => {
      const av = a[sort.key!], bv = b[sort.key!];
      if (av === bv) return 0;
      const cmp = av < bv ? -1 : 1;
      return sort.direction === 'asc' ? cmp : -cmp;
    });
  }, [filtered, sort]);

  if (loading) return <div className="dt-loading">Loading...</div>;

  return (
    <div className="dt-wrapper">
      {searchable && (
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="dt-search-input"
          aria-label="Filter table rows"
        />
      )}
      <div className="dt-scroll">
        <table className="dt-table" role="grid">
          <thead>
            <tr>
              {columns.map((col) => (
                <th
                  key={String(col.key)}
                  style={{ width: col.width }}
                  className={col.sortable ? 'dt-sortable' : ''}
                  onClick={col.sortable ? () => handleSort(col.key) : undefined}
                  aria-sort={sort.key === col.key ? (sort.direction === 'asc' ? 'ascending' : 'descending') : 'none'}
                >
                  {col.header}
                  {col.sortable && sort.key === col.key && (
                    <span>{sort.direction === 'asc' ? ' up' : ' down'}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.length === 0 ? (
              <tr><td colSpan={columns.length} className="dt-empty">{emptyMessage}</td></tr>
            ) : (
              sorted.map((row) => (
                <tr
                  key={String(row[rowKey])}
                  onClick={onRowClick ? () => onRowClick(row) : undefined}
                  className={onRowClick ? 'dt-clickable' : ''}
                  tabIndex={onRowClick ? 0 : undefined}
                >
                  {columns.map((col) => (
                    <td key={String(col.key)}>
                      {col.render ? col.render(row) : String(row[col.key] ?? '')}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <div className="dt-footer">{sorted.length} of {data.length} rows{search && ' (filtered)'}</div>
    </div>
  );
}
