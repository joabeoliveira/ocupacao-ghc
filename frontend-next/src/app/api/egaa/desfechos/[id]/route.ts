import { NextResponse } from 'next/server';
import { dbMock } from '@/lib/db-mock';

export async function GET(request: Request, { params }: { params: { id: string } }) {
  try {
    const id = Number(params.id);
    const desfechos = dbMock.getDesfechos();
    const desfecho = desfechos.find(d => d.id === id);

    if (!desfecho) {
      return NextResponse.json({ error: 'Desfecho não encontrado' }, { status: 404 });
    }

    return NextResponse.json(desfecho);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao carregar desfecho' }, { status: 500 });
  }
}

export async function PUT(request: Request, { params }: { params: { id: string } }) {
  try {
    const id = Number(params.id);
    const body = await request.json();

    if (body.tipo && body.tipo !== 'alta' && body.tipo !== 'obito') {
      return NextResponse.json({ error: 'Tipo deve ser "alta" ou "obito"' }, { status: 400 });
    }

    const updated = dbMock.updateDesfecho(id, body);

    if (!updated) {
      return NextResponse.json({ error: 'Desfecho não encontrado' }, { status: 404 });
    }

    return NextResponse.json(updated);
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao atualizar desfecho' }, { status: 500 });
  }
}

export async function DELETE(request: Request, { params }: { params: { id: string } }) {
  try {
    const id = Number(params.id);
    const deleted = dbMock.deleteDesfecho(id);

    if (!deleted) {
      return NextResponse.json({ error: 'Desfecho não encontrado' }, { status: 404 });
    }

    return NextResponse.json({ message: 'Desfecho removido com sucesso' });
  } catch (error) {
    return NextResponse.json({ error: 'Erro ao remover desfecho' }, { status: 500 });
  }
}
