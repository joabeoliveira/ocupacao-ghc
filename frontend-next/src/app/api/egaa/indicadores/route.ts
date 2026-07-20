import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET() {
  try {
    const data = dbMock.getIndicadores();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar indicadores' }, { status: 500 });
  }
}
