import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const filters = {
      prontuario: searchParams.get('prontuario') || undefined,
      tipo: searchParams.get('tipo') || undefined,
      data_inicio: searchParams.get('data_inicio') || undefined,
      data_fim: searchParams.get('data_fim') || undefined,
    };

    const data = dbMock.getDesfechos(
      filters.prontuario || filters.tipo || filters.data_inicio || filters.data_fim
        ? filters
        : undefined
    );
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar desfechos' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    if (!body.prontuario || !body.tipo || !body.data_desfecho) {
      return NextResponse.json({ error: 'Campos obrigatórios ausentes (prontuario, tipo, data_desfecho)' }, { status: 400 });
    }

    if (body.tipo !== 'alta' && body.tipo !== 'obito') {
      return NextResponse.json({ error: 'Tipo deve ser "alta" ou "obito"' }, { status: 400 });
    }

    const created = dbMock.addDesfecho(body);
    return NextResponse.json(created, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao criar desfecho' }, { status: 500 });
  }
}
