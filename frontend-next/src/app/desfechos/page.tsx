'use client';

import React, { useState } from 'react';
import {
  useDesfechos,
  useIndicadoresDesfecho,
  useCriarDesfecho,
  useRemoverDesfecho,
} from '@/lib/queries';
import { useAuth } from '@/lib/auth';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { KpiCard } from '@/components/ui/KpiCard';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Badge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import {
  HeartPulse,
  Target,
  Plus,
  Trash2,
  Search,
  Activity,
  Skull,
  Users,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const COLORS = {
  alta: '#005C99',
  obito: '#C62828',
};

const GHC_COLORS = ['#005C99', '#00A79D', '#0288D1', '#2E7D32', '#004A7A', '#C62828'];

function CustomTooltip({ active, payload }: any) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-panel-border px-3 py-2 rounded shadow-md">
        <p className="text-xs font-bold text-text uppercase tracking-wider mb-0.5">
          {payload[0].payload.mes || payload[0].name}
        </p>
        <p className="text-xs text-ghc-blue font-semibold">
          {payload[0].value} desfecho(s)
        </p>
      </div>
    );
  }
  return null;
}

export default function DesfechosPage() {
  const { usuario } = useAuth();
  const { data: indicadores, isLoading: loadingIndicadores } = useIndicadoresDesfecho();
  const { data: desfechos, isLoading: loadingDesfechos } = useDesfechos();
  const criarDesfecho = useCriarDesfecho();
  const removerDesfecho = useRemoverDesfecho();

  const [search, setSearch] = useState('');
  const [filtroTipo, setFiltroTipo] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    prontuario: '',
    tipo: 'alta' as string,
    data_desfecho: new Date().toISOString().split('T')[0],
    descricao: '',
    usuario_responsavel: usuario?.nome || '',
  });

  const filteredDesfechos = (desfechos || []).filter((d: any) => {
    const matchSearch = !search || d.prontuario.includes(search) || (d.descricao && d.descricao.toLowerCase().includes(search.toLowerCase()));
    const matchTipo = !filtroTipo || d.tipo === filtroTipo;
    return matchSearch && matchTipo;
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await criarDesfecho.mutateAsync(formData);
      setIsModalOpen(false);
      setFormData({
        prontuario: '',
        tipo: 'alta',
        data_desfecho: new Date().toISOString().split('T')[0],
        descricao: '',
        usuario_responsavel: usuario?.nome || '',
      });
    } catch (err) {
      console.error('Erro ao criar desfecho:', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja remover este desfecho?')) {
      try {
        await removerDesfecho.mutateAsync(id);
      } catch (err) {
        console.error('Erro ao remover desfecho:', err);
      }
    }
  };

  const chartData = indicadores?.por_mes || [];
  const pieData = indicadores?.por_tipo || [];

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-panel-border pb-5 gap-3">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <Target className="w-5 h-5 text-ghc-blue" />
            <h1 className="text-xl font-extrabold text-text uppercase tracking-tight">
              Desfechos EGAA
            </h1>
          </div>
          <p className="text-xs text-muted font-medium">
            Registro de altas e óbitos com atuação do EGAA — demonstrando resultados da desospitalização
          </p>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)}>
          <Plus className="w-4 h-4 mr-1.5" />
          Novo Desfecho
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="Total de Desfechos"
          value={loadingIndicadores ? '...' : (indicadores?.total_desfechos ?? 0)}
          icon={<Activity className="w-5 h-5" />}
        />
        <KpiCard
          title="Altas"
          value={loadingIndicadores ? '...' : (indicadores?.total_altas ?? 0)}
          icon={<HeartPulse className="w-5 h-5" />}
          subtitle="Com apoio do EGAA"
        />
        <KpiCard
          title="Óbitos"
          value={loadingIndicadores ? '...' : (indicadores?.total_obitos ?? 0)}
          icon={<Skull className="w-5 h-5" />}
          subtitle="Com suporte EGAA à família"
        />
        <KpiCard
          title="Pacientes Atendidos"
          value={loadingIndicadores ? '...' : (indicadores?.pacientes_com_desfecho ?? 0)}
          icon={<Users className="w-5 h-5" />}
          subtitle="Com desfecho registrado"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bar chart by month */}
        <Card>
          <CardHeader>
            <CardTitle>Desfechos por Mês</CardTitle>
            <CardDescription>Evolução temporal dos desfechos registrados pelo EGAA</CardDescription>
          </CardHeader>
          <CardContent className="h-[280px]">
            {loadingIndicadores ? (
              <div className="h-full flex items-center justify-center">
                <div className="w-10 h-10 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
              </div>
            ) : chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                  <XAxis
                    dataKey="mes"
                    tick={{ fill: '#64748B', fontSize: 11, fontWeight: 600 }}
                    axisLine={{ stroke: '#CBD5E1' }}
                    tickLine={false}
                    tickFormatter={(val) => {
                      const [ano, mes] = val.split('-');
                      const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
                      return `${meses[parseInt(mes) - 1]}/${ano}`;
                    }}
                  />
                  <YAxis tick={{ fill: '#64748B', fontSize: 11 }} axisLine={false} tickLine={false} allowDecimals={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="total" radius={[4, 4, 0, 0]} maxBarSize={50}>
                    {chartData.map((_: any, index: number) => (
                      <Cell key={index} fill={GHC_COLORS[index % GHC_COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-muted text-sm">
                Nenhum desfecho registrado ainda
              </div>
            )}
          </CardContent>
        </Card>

        {/* Pie chart by type */}
        <Card>
          <CardHeader>
            <CardTitle>Desfechos por Tipo</CardTitle>
            <CardDescription>Distribuição entre altas e óbitos com atuação do EGAA</CardDescription>
          </CardHeader>
          <CardContent className="h-[280px]">
            {loadingIndicadores ? (
              <div className="h-full flex items-center justify-center">
                <div className="w-10 h-10 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
              </div>
            ) : pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="total"
                    nameKey="tipo"
                    cx="50%"
                    cy="50%"
                    outerRadius={90}
                    innerRadius={50}
                    paddingAngle={3}
                    label={({ tipo, total, percent }) => {
                      const labels: Record<string, string> = { alta: 'Altas', obito: 'Óbitos' };
                      return `${labels[tipo] || tipo}: ${total} (${(percent * 100).toFixed(0)}%)`;
                    }}
                    labelLine={false}
                  >
                    {pieData.map((entry: any) => (
                      <Cell key={entry.tipo} fill={COLORS[entry.tipo as keyof typeof COLORS] || '#94A3B8'} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-muted text-sm">
                Nenhum desfecho registrado ainda
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Filters and List */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <CardTitle>Registros de Desfechos</CardTitle>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <div className="relative flex-1 sm:flex-none sm:w-48">
                <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
                <input
                  type="text"
                  placeholder="Buscar por prontuário..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 text-sm border border-panel-border rounded bg-white focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue"
                />
              </div>
              <select
                value={filtroTipo}
                onChange={(e) => setFiltroTipo(e.target.value)}
                className="px-3 py-1.5 text-sm border border-panel-border rounded bg-white focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue"
              >
                <option value="">Todos os tipos</option>
                <option value="alta">Altas</option>
                <option value="obito">Óbitos</option>
              </select>
            </div>
          </div>
          <CardDescription>
            {filteredDesfechos.length} registro(s) encontrado(s)
          </CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          {loadingDesfechos ? (
            <div className="flex items-center justify-center py-12">
              <div className="w-10 h-10 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
            </div>
          ) : filteredDesfechos.length === 0 ? (
            <div className="text-center py-12 text-muted text-sm">
              Nenhum desfecho encontrado.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-panel-border bg-gray-50/80">
                    <th className="text-left px-6 py-3 text-xs font-semibold text-muted uppercase tracking-wider">Prontuário</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-muted uppercase tracking-wider">Tipo</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-muted uppercase tracking-wider">Data</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-muted uppercase tracking-wider">Responsável</th>
                    <th className="text-left px-6 py-3 text-xs font-semibold text-muted uppercase tracking-wider">Descrição</th>
                    <th className="text-right px-6 py-3 text-xs font-semibold text-muted uppercase tracking-wider">Ações</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-panel-border">
                  {filteredDesfechos.map((desfecho: any) => (
                    <tr key={desfecho.id} className="hover:bg-gray-50/50 transition-colors">
                      <td className="px-6 py-3.5 font-mono text-xs font-bold text-text">
                        {desfecho.prontuario}
                      </td>
                      <td className="px-6 py-3.5">
                        <Badge
                          variant={desfecho.tipo === 'alta' ? 'success' : 'error'}
                          className="uppercase text-[10px] tracking-wider"
                        >
                          {desfecho.tipo === 'alta' ? 'Alta' : 'Óbito'}
                        </Badge>
                      </td>
                      <td className="px-6 py-3.5 text-muted text-xs">
                        {new Date(desfecho.data_desfecho + 'T00:00:00').toLocaleDateString('pt-BR')}
                      </td>
                      <td className="px-6 py-3.5 text-xs text-text font-medium">
                        {desfecho.usuario_responsavel || '-'}
                      </td>
                      <td className="px-6 py-3.5 text-xs text-muted max-w-xs truncate">
                        {desfecho.descricao || '-'}
                      </td>
                      <td className="px-6 py-3.5 text-right">
                        <button
                          onClick={() => handleDelete(desfecho.id)}
                          className="p-1.5 rounded text-muted hover:text-priority-vermelho hover:bg-red-50 transition-colors"
                          title="Remover desfecho"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Modal para criar novo desfecho */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Novo Desfecho EGAA" size="lg">
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Prontuário do Paciente"
              placeholder="Ex: 8399062"
              value={formData.prontuario}
              onChange={(e) => setFormData({ ...formData, prontuario: e.target.value })}
              required
            />
            <Select
              label="Tipo de Desfecho"
              value={formData.tipo}
              onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
              options={[
                { value: 'alta', label: 'Alta Hospitalar' },
                { value: 'obito', label: 'Óbito' },
              ]}
              required
            />
          </div>

          <Input
            label="Data do Desfecho"
            type="date"
            value={formData.data_desfecho}
            onChange={(e) => setFormData({ ...formData, data_desfecho: e.target.value })}
            required
          />

          <div>
            <label className="block text-sm font-medium text-text mb-1.5">Descrição / Observação</label>
            <textarea
              className="flex w-full rounded border border-panel-border bg-white px-3 py-2 text-sm text-text transition-colors duration-200 placeholder:text-muted focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue min-h-[100px]"
              placeholder="Descreva como o EGAA atuou neste desfecho..."
              value={formData.descricao}
              onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
            />
          </div>

          <Input
            label="Responsável EGAA"
            placeholder="Seu nome"
            value={formData.usuario_responsavel}
            onChange={(e) => setFormData({ ...formData, usuario_responsavel: e.target.value })}
          />

          <div className="flex justify-end gap-3 pt-3 border-t border-panel-border">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit" disabled={criarDesfecho.isPending}>
              {criarDesfecho.isPending ? 'Salvando...' : 'Registrar Desfecho'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
