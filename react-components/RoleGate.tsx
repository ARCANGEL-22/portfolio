import React, { createContext, useContext, ReactNode } from 'react';

/**
 * RoleGate - Role-Based Access Control component
 * Used in the ODEN PWA to gate UI sections by user role.
 * Roles: 'admin' | 'engineer' | 'viewer'
 */

export type UserRole = 'admin' | 'engineer' | 'viewer';

interface AuthUser {
  uid: string;
  email: string;
  role: UserRole;
  displayName: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue>({ user: null, isAuthenticated: false });

interface AuthProviderProps { user: AuthUser | null; children: ReactNode; }

export function AuthProvider({ user, children }: AuthProviderProps) {
  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  return useContext(AuthContext);
}

interface RoleGateProps {
  /** Roles that are permitted to see the children */
  allowed: UserRole[];
  /** Optional fallback when access is denied */
  fallback?: ReactNode;
  children: ReactNode;
}

/**
 * RoleGate - render children only when the current user has an allowed role.
 */
export function RoleGate({ allowed, fallback = null, children }: RoleGateProps) {
  const { user } = useAuth();
  if (!user || !allowed.includes(user.role)) return <>{fallback}</>;
  return <>{children}</>;
}

/** Renders children only for admin users */
export function AdminOnly({ children, fallback }: Omit<RoleGateProps, 'allowed'>) {
  return <RoleGate allowed={['admin']} fallback={fallback}>{children}</RoleGate>;
}

/** Renders children for admin or engineer users */
export function EngineerAndAbove({ children, fallback }: Omit<RoleGateProps, 'allowed'>) {
  return <RoleGate allowed={['admin', 'engineer']} fallback={fallback}>{children}</RoleGate>;
}

/** HOC version of RoleGate for wrapping existing components */
export function withRoleGate<P extends object>(
  Component: React.ComponentType<P>,
  allowed: UserRole[],
  FallbackComponent?: React.ComponentType
) {
  return function ProtectedComponent(props: P) {
    return (
      <RoleGate allowed={allowed} fallback={FallbackComponent ? <FallbackComponent /> : null}>
        <Component {...props} />
      </RoleGate>
    );
  };
}
