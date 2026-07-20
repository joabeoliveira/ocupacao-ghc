import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function PUT(
  request: Request,
  { params }: { params: { prontuario: string } }
) {
  try {
    const prontuario = params.prontuario;
    const { evolucao } = await request.json();

    const updated = dbMock.updateEvolucao(prontuario, evolucao);
    if (!updated) {
      return NextResponse.json({ error: 'Paciente não encontrado' }, { status: 404 });
    }

    return NextResponse.json(updated);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao atualizar evolução' }, { status: 500 });
  }
}
