import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const data_inicio = searchParams.get('data_inicio') || undefined;
    const data_fim = searchParams.get('data_fim') || undefined;

    const kpis = dbMock.getKPIs(data_inicio, data_fim);
    return NextResponse.json(kpis);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar KPIs' }, { status: 500 });
  }
}
