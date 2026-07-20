'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import {
  LayoutDashboard,
  BedDouble,
  Settings,
  Upload,
  LogOut,
  User,
  HeartPulse,
  Target
} from 'lucide-react';
import { VersionBadge } from './VersionBadge';
import { cn } from '@/lib/utils';

export function Sidebar() {
  const pathname = usePathname();
  const { usuario, logout } = useAuth();

  const links = [
    {
      href: '/dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
    },
    {
      href: '/longa-permanencia',
      label: 'Longa Permanência',
      icon: BedDouble,
    },
    {
      href: '/desfechos',
      label: 'Desfechos EGAA',
      icon: Target,
    },
    {
      href: '/upload',
      label: 'Cargas Censo',
      icon: Upload,
    },
    {
      href: '/configuracoes',
      label: 'Configurações',
      icon: Settings,
    },
  ];

  return (
    <aside className="w-64 bg-ghc-blue text-white flex flex-col min-h-screen border-r border-ghc-blue-dark shadow-md">
      {/* Brand Logo Header */}
      <div className="flex items-center space-x-2.5 px-6 py-5 border-b border-white/10 bg-ghc-blue-dark/30">
        <div className="p-1.5 bg-white rounded-lg text-ghc-blue">
          <HeartPulse className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h1 className="text-sm font-bold tracking-tight leading-none uppercase">
            Painel EGAA
          </h1>
          <span className="text-[10px] text-ghc-blue-light/75 font-medium uppercase tracking-wider block mt-1">
            Censo Hospitalar GHC
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1.5">
        {links.map((link) => {
          const isActive = pathname.startsWith(link.href);
          const Icon = link.icon;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                'flex items-center space-x-3 px-4 py-3 rounded text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-white text-ghc-blue font-semibold shadow-md translate-x-1'
                  : 'text-white/80 hover:bg-white/10 hover:text-white'
              )}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Version and Brand */}
      <div className="px-6 py-4 border-t border-white/10 bg-ghc-blue-dark/10">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-ghc-blue-light/80">
            GHC - EGAA © 2026
          </span>
          <VersionBadge />
        </div>
      </div>

      {/* User Session Footer */}
      <div className="p-4 border-t border-white/10 bg-ghc-blue-dark/30 flex flex-col space-y-3">
        <div className="flex items-center space-x-3 px-2">
          <div className="w-9 h-9 rounded-full bg-white/15 border border-white/10 flex items-center justify-center text-white font-bold text-sm">
            {usuario?.nome ? usuario.nome.charAt(0) : <User className="w-4 h-4" />}
          </div>
          <div className="overflow-hidden">
            <p className="text-xs font-semibold truncate leading-tight">
              {usuario?.nome || 'Conectado'}
            </p>
            <p className="text-[10px] text-white/60 truncate leading-tight">
              {usuario?.email || 'admin@ghc.com.br'}
            </p>
          </div>
        </div>
        <button
          onClick={logout}
          className="flex items-center justify-center space-x-2 w-full px-4 py-2 bg-white/10 hover:bg-white/15 active:scale-[0.98] border border-white/10 rounded text-xs font-semibold tracking-wider uppercase transition-all duration-200 text-white"
        >
          <LogOut className="w-4 h-4" />
          <span>Sair da Conta</span>
        </button>
      </div>
    </aside>
  );
}
