'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter, CardDescription } from '@/components/ui/Card';
import { HeartPulse, ShieldAlert, Key } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, senha })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Credenciais inválidas');
      }

      // Store in context (which also writes cookie)
      login(data.token, data.usuario);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Falha ao autenticar.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50/50">
      <Card className="w-full max-w-md shadow-lg border border-panel-border bg-white rounded-lg overflow-hidden">
        {/* Banner Logo */}
        <div className="bg-ghc-blue text-white px-6 py-6 text-center space-y-2.5 border-b border-ghc-blue-dark">
          <div className="w-12 h-12 rounded-xl bg-white text-ghc-blue flex items-center justify-center mx-auto shadow">
            <HeartPulse className="w-7 h-7 animate-pulse" />
          </div>
          <div>
            <h2 className="text-sm font-black tracking-widest uppercase">
              Grupo Hospitalar Conceição
            </h2>
            <p className="text-[10px] text-ghc-blue-light font-bold uppercase tracking-wider">
              Painel de Regulação &amp; Censo Hospitalar (EGAA)
            </p>
          </div>
        </div>

        <CardContent className="p-6 space-y-5">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-red-50 text-priority-vermelho px-3 py-2.5 rounded border border-red-200 text-xs font-semibold flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <Input
              label="E-mail Funcional"
              placeholder="seu.nome@ghc.com.br"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <Input
              label="Senha de Acesso"
              placeholder="••••••••"
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />

            <Button
              type="submit"
              disabled={loading}
              className="w-full h-10 inline-flex items-center justify-center space-x-2 mt-2 uppercase font-semibold text-xs tracking-wider"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <Key className="w-4 h-4" />
              )}
              <span>Acessar o Painel</span>
            </Button>
          </form>

          {/* Helper box with credentials for easy testing */}
          <div className="bg-slate-50 border border-slate-200 p-3 rounded text-[11px] text-muted space-y-1">
            <p className="font-bold text-slate-700 uppercase tracking-wide">Acesso de Demonstração (MVP):</p>
            <p>E-mail: <strong className="text-slate-800">admin@ghc.com.br</strong></p>
            <p>Senha: <strong className="text-slate-800">admin123</strong></p>
          </div>
        </CardContent>

        <CardFooter className="bg-slate-50 text-center py-3 text-[10px] text-muted border-t border-panel-border uppercase font-bold tracking-wider">
          EGAA - Regulação e Gestão da Desospitalização
        </CardFooter>
      </Card>
    </div>
  );
}
