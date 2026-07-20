import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function PUT(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const id = Number(params.id);
    const body = await request.json();
    const updated = dbMock.updateTipoIntervencao(id, body);
    if (!updated) {
      return NextResponse.json({ error: 'Tipo não encontrado' }, { status: 404 });
    }
    return NextResponse.json(updated);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao atualizar tipo de intervenção' }, { status: 500 });
  }
}
