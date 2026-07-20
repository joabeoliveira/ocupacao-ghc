'use client';

import React, { useState } from 'react';
import { useTiposIntervencao } from '@/lib/queries';
import { useQueryClient } from '@tanstack/react-query';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { api } from '@/lib/api';
import { TipoIntervencao } from '@/types';
import { Settings, PlusCircle, ToggleLeft, ToggleRight, Sparkles, Sliders } from 'lucide-react';

export default function ConfiguracoesPage() {
  const queryClient = useQueryClient();
  const { data: tipos, isLoading } = useTiposIntervencao();

  const [nome, setNome] = useState('');
  const [descricao, setDescricao] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState('');

  const handleAddTipo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nome.trim()) return;

    setIsSubmitting(true);
    setFeedback('');

    try {
      await api.post('/api/egaa/tipos-intervencao', {
        nome,
        descricao,
        ativo: true,
        ordem_exibicao: (tipos || []).length + 1
      });

      setNome('');
      setDescricao('');
      queryClient.invalidateQueries({ queryKey: ['tipos-intervencao'] });
      setFeedback('Tipo de intervenção adicionado com sucesso!');
    } catch (err) {
      setFeedback('Erro ao cadastrar tipo de atuação.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleToggleAtivo = async (tipo: TipoIntervencao) => {
    try {
      await api.put(`/api/egaa/tipos-intervencao/${tipo.id}`, {
        ativo: !tipo.ativo
      });
      queryClient.invalidateQueries({ queryKey: ['tipos-intervencao'] });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title Header Section */}
      <div className="border-b border-panel-border pb-5">
        <div className="flex items-center space-x-2">
          <Settings className="w-5 h-5 text-ghc-blue" />
          <h1 className="text-xl font-extrabold text-text uppercase tracking-tight">
            Configurações do Fluxo EGAA
          </h1>
        </div>
        <p className="text-xs text-muted font-medium mt-1">
          Customização do dicionário de intervenções, gatilhos de monitoramento e atuações clínicas para deshospitalização.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left pane: dictionary list */}
        <div className="lg:col-span-2 space-y-4">
          <Card className="bg-white border border-panel-border rounded-lg shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Tipos de Atuação Cadastrados</CardTitle>
                <CardDescription>
                  Dicionário ativo de classificações das intervenções do EGAA
                </CardDescription>
              </div>
              <Badge variant="default">Censo Ativo</Badge>
            </CardHeader>
            <CardContent className="p-0">
              {isLoading ? (
                <div className="py-12 flex items-center justify-center space-y-2 flex-col">
                  <div className="w-8 h-8 border-3 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
                  <p className="text-xs text-muted font-medium">Carregando atuações...</p>
                </div>
              ) : (tipos || []).length === 0 ? (
                <div className="py-12 text-center text-sm text-muted">
                  Nenhum tipo cadastrado.
                </div>
              ) : (
                <div className="divide-y divide-panel-border">
                  {(tipos || []).map((tipo: TipoIntervencao) => (
                    <div
                      key={tipo.id}
                      className="px-6 py-4 flex items-center justify-between hover:bg-slate-50/50 transition-colors duration-150"
                    >
                      <div className="space-y-1 pr-4">
                        <div className="flex items-center space-x-2">
                          <h4 className="text-sm font-bold text-slate-800 uppercase">
                            {tipo.nome}
                          </h4>
                          <Badge variant={tipo.ativo ? 'success' : 'neutral'} className="text-[8px] px-1 py-0 scale-95">
                            {tipo.ativo ? 'Ativo' : 'Inativo'}
                          </Badge>
                        </div>
                        {tipo.descricao && (
                          <p className="text-xs text-muted leading-relaxed">
                            {tipo.descricao}
                          </p>
                        )}
                      </div>

                      {/* Toggle button */}
                      <button
                        onClick={() => handleToggleAtivo(tipo)}
                        className="text-ghc-blue hover:text-ghc-blue-dark focus:outline-none p-1 transition-transform duration-150 active:scale-95"
                        title={tipo.ativo ? 'Desativar classificação' : 'Ativar classificação'}
                      >
                        {tipo.ativo ? (
                          <ToggleRight className="w-9 h-9 text-ghc-blue" />
                        ) : (
                          <ToggleLeft className="w-9 h-9 text-slate-300" />
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right pane: Add new type */}
        <div className="space-y-4">
          <Card className="bg-white border border-panel-border rounded-lg shadow-sm">
            <CardHeader className="flex items-center space-x-2">
              <Sliders className="w-5 h-5 text-ghc-blue" />
              <div>
                <CardTitle>Nova Classificação</CardTitle>
                <CardDescription>
                  Adicione novos tipos de parecer ou acompanhamento ao fluxo
                </CardDescription>
              </div>
            </CardHeader>
            <CardContent className="p-6">
              <form onSubmit={handleAddTipo} className="space-y-4">
                {feedback && (
                  <div className="bg-emerald-50 text-emerald-800 px-3 py-2 rounded text-xs font-semibold border border-emerald-200">
                    {feedback}
                  </div>
                )}

                <Input
                  label="Nome da Intervenção"
                  placeholder="Ex: Contato com Posto de Saúde"
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  required
                />

                <div>
                  <label className="block text-sm font-medium text-text mb-1.5">
                    Descrição do Propósito
                  </label>
                  <textarea
                    rows={3}
                    className="flex w-full rounded border border-panel-border bg-white px-3 py-2 text-sm text-text transition-colors duration-200 placeholder:text-muted focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue"
                    placeholder="Explique resumidamente quando os profissionais de regulação devem utilizar este tipo de classificação..."
                    value={descricao}
                    onChange={(e) => setDescricao(e.target.value)}
                  />
                </div>

                <Button
                  type="submit"
                  disabled={isSubmitting || !nome.trim()}
                  className="w-full inline-flex items-center justify-center space-x-2"
                >
                  {isSubmitting ? (
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <PlusCircle className="w-4 h-4" />
                  )}
                  <span>Cadastrar Tipo</span>
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
