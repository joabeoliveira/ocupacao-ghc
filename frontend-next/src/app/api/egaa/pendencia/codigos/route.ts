import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET() {
  try {
    const list = dbMock.getPendenciaCodigos();
    return NextResponse.json(list);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar códigos de pendências' }, { status: 500 });
  }
}
