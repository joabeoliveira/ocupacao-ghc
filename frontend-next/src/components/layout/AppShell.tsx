'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { Sidebar } from './Sidebar';
import { useAuth } from '@/lib/auth';

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { loading } = useAuth();
  const isLoginPage = pathname === '/login';

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-surface space-y-4">
        <div className="w-12 h-12 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
        <p className="text-xs font-semibold uppercase tracking-wider text-muted">Iniciando ambiente EGAA...</p>
      </div>
    );
  }

  if (isLoginPage) {
    return <div className="min-h-screen bg-slate-50">{children}</div>;
  }

  return (
    <div className="flex min-h-screen bg-slate-50/50">
      {/* Sidebar Navigation */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto px-8 py-8 max-w-7xl mx-auto w-full">
        {children}
      </main>
    </div>
  );
}
