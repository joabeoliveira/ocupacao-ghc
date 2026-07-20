import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function PUT(
  request: Request,
  { params }: { params: { prontuario: string; id: string } }
) {
  try {
    const prontuario = params.prontuario;
    const id = Number(params.id);
    const { resolvida } = await request.json();

    const updated = dbMock.updatePendencia(prontuario, id, resolvida);
    if (!updated) {
      return NextResponse.json({ error: 'Pendência não encontrada' }, { status: 404 });
    }

    return NextResponse.json(updated);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao atualizar pendência' }, { status: 500 });
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { prontuario: string; id: string } }
) {
  try {
    const prontuario = params.prontuario;
    const id = Number(params.id);

    const deleted = dbMock.deletePendencia(prontuario, id);
    if (!deleted) {
      return NextResponse.json({ error: 'Pendência não encontrada' }, { status: 404 });
    }

    return NextResponse.json({ sucesso: true, deleted });
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao deletar pendência' }, { status: 500 });
  }
}
