import { NextResponse } from 'next/server';

const BACKEND_URL = (process.env.NEXT_PUBLIC_API_URL || '').replace(/\/+$/, '');

export async function POST(request: Request) {
  try {
    const formData = await request.formData();

    if (!BACKEND_URL) {
      return NextResponse.json({
        sucesso: true,
        mensagem: 'Modo desenvolvimento: simulação de carga realizada com sucesso.'
      });
    }

    const response = await fetch(`${BACKEND_URL}/upload/arquivo`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json({ error: data.detail || data.error || 'Erro no processamento do arquivo' }, { status: response.status });
    }

    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Erro no processamento do arquivo' }, { status: 500 });
  }
}
