import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const prontuario = searchParams.get('prontuario');

    if (!prontuario) {
      return NextResponse.json({ error: 'Prontuário é obrigatório' }, { status: 400 });
    }

    const data = dbMock.getIntervencoes(prontuario);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar intervenções' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    if (!body.prontuario || !body.tipo_intervencao_id) {
      return NextResponse.json({ error: 'Campos obrigatórios ausentes' }, { status: 400 });
    }

    const created = dbMock.addIntervencao(body);
    return NextResponse.json(created);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao criar intervenção' }, { status: 500 });
  }
}
