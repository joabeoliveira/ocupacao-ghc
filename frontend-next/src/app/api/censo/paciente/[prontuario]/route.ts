import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(
  request: Request,
  { params }: { params: { prontuario: string } }
) {
  try {
    const prontuario = params.prontuario;
    const paciente = dbMock.getPaciente(prontuario);
    if (!paciente) {
      return NextResponse.json({ error: 'Paciente não encontrado' }, { status: 404 });
    }
    return NextResponse.json(paciente);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar paciente' }, { status: 500 });
  }
}
