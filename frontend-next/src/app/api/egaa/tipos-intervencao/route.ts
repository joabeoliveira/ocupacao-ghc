import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET() {
  try {
    const list = dbMock.getTiposIntervencao();
    return NextResponse.json(list);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar tipos de intervenção' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    if (!body.nome) {
      return NextResponse.json({ error: 'Nome é obrigatório' }, { status: 400 });
    }
    const record = dbMock.saveTipoIntervencao(body);
    return NextResponse.json(record);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao criar tipo de intervenção' }, { status: 500 });
  }
}
