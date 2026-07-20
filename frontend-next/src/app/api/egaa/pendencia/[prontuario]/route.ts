import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(
  request: Request,
  { params }: { params: { prontuario: string } }
) {
  try {
    const prontuario = params.prontuario;
    const list = dbMock.getPendencias(prontuario);
    return NextResponse.json(list);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar pendências' }, { status: 500 });
  }
}

export async function POST(
  request: Request,
  { params }: { params: { prontuario: string } }
) {
  try {
    const prontuario = params.prontuario;
    const { codigo } = await request.json();

    if (!codigo) {
      return NextResponse.json({ error: 'Código da pendência é obrigatório' }, { status: 400 });
    }

    const created = dbMock.addPendencia(prontuario, codigo);
    return NextResponse.json(created);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao criar pendência' }, { status: 500 });
  }
}
