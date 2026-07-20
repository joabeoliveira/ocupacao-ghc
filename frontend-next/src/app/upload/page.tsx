'use client';

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import {
  Upload,
  FileSpreadsheet,
  CheckCircle,
  Database,
  History,
  AlertTriangle,
  ClipboardCheck
} from 'lucide-react';
import { cn } from '@/lib/utils';

type UploadType = 'censo' | 'historico' | 'arquivo';

export default function UploadPage() {
  const [activeTab, setActiveTab] = useState<UploadType>('censo');
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ sucesso: boolean; mensagem: string } | null>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      // Accept only excel or csv
      if (
        file.name.endsWith('.xlsx') ||
        file.name.endsWith('.xls') ||
        file.name.endsWith('.csv')
      ) {
        setSelectedFile(file);
        setUploadResult(null);
      }
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setUploadResult(null);
    }
  };

  const handleUploadSubmit = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setUploadResult(null);

    // Map tab type to API endpoint
    const endpoints = {
      censo: '/api/upload/censo',
      historico: '/api/upload/historico',
      arquivo: '/api/upload/arquivo'
    };

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch(endpoints[activeTab], {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setUploadResult({
          sucesso: true,
          mensagem: data.mensagem || `Carga realizada com sucesso! ${data.linhas_processadas || ''} registros processados.`
        });
        setSelectedFile(null);
      } else {
        throw new Error(data.error || data.detail || 'Erro no processamento.');
      }
    } catch (err: any) {
      setUploadResult({
        sucesso: false,
        mensagem: err.message || 'Erro inesperado na carga do arquivo.'
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title Header Section */}
      <div className="border-b border-panel-border pb-5">
        <div className="flex items-center space-x-2">
          <Upload className="w-5 h-5 text-ghc-blue" />
          <h1 className="text-xl font-extrabold text-text uppercase tracking-tight">
            Importação de Carga de Dados e Censo
          </h1>
        </div>
        <p className="text-xs text-muted font-medium mt-1">
          Atualização das bases de leitos e internação por cargas de planilhas de censo diário hospitalar ou bancos históricos.
        </p>
      </div>

      {/* Tabs Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Tab 1 */}
        <Card
          className={cn(
            'cursor-pointer transition-all duration-300 border hover:shadow-md select-none p-5 flex items-center space-x-4',
            activeTab === 'censo'
              ? 'border-ghc-blue bg-ghc-blue-light/10 ring-1 ring-ghc-blue'
              : 'border-panel-border bg-white'
          )}
          onClick={() => {
            setActiveTab('censo');
            setSelectedFile(null);
            setUploadResult(null);
          }}
        >
          <div className={cn('p-3 rounded-lg border', activeTab === 'censo' ? 'bg-white text-ghc-blue border-ghc-blue/20' : 'bg-gray-50 border-gray-100')}>
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">Censo Diário GHC</h3>
            <p className="text-[10px] text-muted font-medium">Atualizar base ativa de internados</p>
          </div>
        </Card>

        {/* Tab 2 */}
        <Card
          className={cn(
            'cursor-pointer transition-all duration-300 border hover:shadow-md select-none p-5 flex items-center space-x-4',
            activeTab === 'historico'
              ? 'border-ghc-blue bg-ghc-blue-light/10 ring-1 ring-ghc-blue'
              : 'border-panel-border bg-white'
          )}
          onClick={() => {
            setActiveTab('historico');
            setSelectedFile(null);
            setUploadResult(null);
          }}
        >
          <div className={cn('p-3 rounded-lg border', activeTab === 'historico' ? 'bg-white text-ghc-blue border-ghc-blue/20' : 'bg-gray-50 border-gray-100')}>
            <History className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">Carga Histórica</h3>
            <p className="text-[10px] text-muted font-medium">Bases consolidadas de longa permanência</p>
          </div>
        </Card>

        {/* Tab 3 */}
        <Card
          className={cn(
            'cursor-pointer transition-all duration-300 border hover:shadow-md select-none p-5 flex items-center space-x-4',
            activeTab === 'arquivo'
              ? 'border-ghc-blue bg-ghc-blue-light/10 ring-1 ring-ghc-blue'
              : 'border-panel-border bg-white'
          )}
          onClick={() => {
            setActiveTab('arquivo');
            setSelectedFile(null);
            setUploadResult(null);
          }}
        >
          <div className={cn('p-3 rounded-lg border', activeTab === 'arquivo' ? 'bg-white text-ghc-blue border-ghc-blue/20' : 'bg-gray-50 border-gray-100')}>
            <FileSpreadsheet className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">Arquivo Geral</h3>
            <p className="text-[10px] text-muted font-medium">Subir relatórios temáticos e laudos</p>
          </div>
        </Card>
      </div>

      {/* Main Upload Box Area */}
      <Card className="bg-white border border-panel-border rounded-lg shadow-sm">
        <CardContent className="p-8 space-y-6">
          <div className="flex items-center justify-between border-b border-panel-border pb-4">
            <div>
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-800">
                {activeTab === 'censo' && 'Importar Planilha do Censo Diário'}
                {activeTab === 'historico' && 'Sincronizar Banco de Dados Histórico'}
                {activeTab === 'arquivo' && 'Anexar Laudos / Pareceres em Lote'}
              </h3>
              <p className="text-xs text-muted mt-1">
                Envie arquivos consolidados em formato Excel (.xlsx, .xls) ou CSV delimitados por vírgulas.
              </p>
            </div>
            <Badge variant="default" className="text-[10px]">
              {activeTab === 'censo' && 'Foco: Censo Ativo'}
              {activeTab === 'historico' && 'Foco: Análise Histórica'}
              {activeTab === 'arquivo' && 'Foco: Auxiliares'}
            </Badge>
          </div>

          {/* Drag & Drop Area */}
          <div
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={cn(
              'border-2 border-dashed rounded-lg p-12 text-center transition-all duration-300 relative',
              dragActive
                ? 'border-ghc-blue bg-ghc-blue-light/10 scale-[0.99]'
                : 'border-slate-300 bg-slate-50 hover:bg-slate-100/50 hover:border-slate-400'
            )}
          >
            <input
              type="file"
              id="file-upload-input"
              className="hidden"
              onChange={handleFileInput}
              accept=".xlsx,.xls,.csv"
            />

            <div className="space-y-4 max-w-sm mx-auto">
              <div className="w-12 h-12 rounded-full bg-ghc-blue-light/20 text-ghc-blue flex items-center justify-center mx-auto">
                <Upload className="w-6 h-6" />
              </div>
              <div className="space-y-1">
                <p className="text-sm font-bold text-slate-800">
                  Arraste e solte o arquivo aqui
                </p>
                <p className="text-xs text-muted font-medium">
                  ou se preferir,{' '}
                  <label
                    htmlFor="file-upload-input"
                    className="text-ghc-blue font-extrabold hover:underline cursor-pointer"
                  >
                    selecione do seu computador
                  </label>
                </p>
              </div>
              <p className="text-[10px] text-muted font-semibold uppercase tracking-wider">
                Extensões suportadas: XLSX, XLS, CSV (Max. 15MB)
              </p>
            </div>
          </div>

          {/* Selected File Section */}
          {selectedFile && (
            <div className="bg-slate-50 border border-slate-200/80 p-4 rounded-lg flex items-center justify-between animate-in fade-in slide-in-from-bottom-2 duration-150">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-emerald-100 text-emerald-800 rounded-lg">
                  <FileSpreadsheet className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-800 truncate max-w-md">
                    {selectedFile.name}
                  </p>
                  <p className="text-[10px] text-muted">
                    Tamanho: {(selectedFile.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
              <div className="flex space-x-3">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedFile(null)}
                  className="text-muted hover:text-text font-bold"
                >
                  Cancelar
                </Button>
                <Button
                  size="sm"
                  onClick={handleUploadSubmit}
                  disabled={isUploading}
                  className="font-bold inline-flex items-center space-x-1"
                >
                  {isUploading ? (
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <ClipboardCheck className="w-4 h-4" />
                  )}
                  <span>Processar Arquivo</span>
                </Button>
              </div>
            </div>
          )}

          {/* Results Feedback Box */}
          {uploadResult && (
            <div
              className={cn(
                'border p-5 rounded-lg flex items-start space-x-4 animate-in fade-in slide-in-from-bottom-3 duration-200',
                uploadResult.sucesso
                  ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                  : 'bg-rose-50 text-priority-vermelho border-rose-200'
              )}
            >
              <div className={cn('p-2.5 rounded-lg', uploadResult.sucesso ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-priority-vermelho')}>
                {uploadResult.sucesso ? <CheckCircle className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
              </div>
              <div className="space-y-1">
                <h4 className="text-xs font-black uppercase tracking-wider">
                  {uploadResult.sucesso ? 'Processamento Concluído' : 'Falha na Carga de Arquivo'}
                </h4>
                <p className="text-xs leading-relaxed font-medium">
                  {uploadResult.mensagem}
                </p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
