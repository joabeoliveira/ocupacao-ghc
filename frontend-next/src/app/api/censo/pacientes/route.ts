import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const page = searchParams.get('page') ? Number(searchParams.get('page')) : undefined;
    const page_size = searchParams.get('page_size') ? Number(searchParams.get('page_size')) : undefined;
    const prontuario = searchParams.get('prontuario') || undefined;
    const nome = searchParams.get('nome') || undefined;
    const especialidade = searchParams.get('especialidade') || undefined;
    const unidade = searchParams.get('unidade') || undefined;
    const min_dias = searchParams.get('min_dias') ? Number(searchParams.get('min_dias')) : undefined;
    const idade_minima = searchParams.get('idade_minima') ? Number(searchParams.get('idade_minima')) : undefined;
    const data_inicio = searchParams.get('data_inicio') || undefined;
    const data_fim = searchParams.get('data_fim') || undefined;

    const data = dbMock.getPacientes({
      page,
      page_size,
      prontuario,
      nome,
      especialidade,
      unidade,
      min_dias,
      idade_minima,
      data_inicio,
      data_fim
    });

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar pacientes' }, { status: 500 });
  }
}
