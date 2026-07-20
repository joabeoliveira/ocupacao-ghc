'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { getCookie, setCookie, removeCookie } from './utils';

interface Usuario {
  nome: string;
  email: string;
}

interface AuthContextType {
  usuario: Usuario | null;
  token: string | null;
  loading: boolean;
  login: (token: string, usuario: Usuario) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists in cookies
    const currentToken = getCookie('token');
    if (currentToken) {
      try {
        // Decode simulated JWT payload
        const parts = currentToken.split('.');
        if (parts.length === 3) {
          const payload = JSON.parse(atob(parts[1]));
          // Check expiration
          if (payload.exp && payload.exp > Date.now() / 1000) {
            setToken(currentToken);
            setUsuario({
              nome: payload.nome || 'Usuário',
              email: payload.sub || ''
            });
          } else {
            // Expired
            removeCookie('token');
          }
        }
      } catch (e) {
        removeCookie('token');
      }
    }
    setLoading(false);
  }, []);

  const login = (newToken: string, novoUsuario: Usuario) => {
    setToken(newToken);
    setUsuario(novoUsuario);
    setCookie('token', newToken, 7);
  };

  const logout = () => {
    setToken(null);
    setUsuario(null);
    removeCookie('token');
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  };

  return (
    <AuthContext.Provider value={{ usuario, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
}
