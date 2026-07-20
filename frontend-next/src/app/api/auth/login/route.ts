import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { email, senha } = await request.json();

    // Standard MVP credentials as per /docs/AUTH.md
    if (email === 'admin@ghc.com.br' && senha === 'admin123') {
      // Create a simulated JWT token
      const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
      const payload = btoa(JSON.stringify({
        sub: email,
        nome: 'Administrador EGAA',
        exp: Math.floor(Date.now() / 1000) + (7 * 24 * 60 * 60) // 7 days expiration
      }));
      const signature = 'mock_signature';
      const token = `${header}.${payload}.${signature}`;

      const response = NextResponse.json({
        token,
        usuario: {
          nome: 'Administrador EGAA',
          email: 'admin@ghc.com.br'
        }
      });

      // Set cookie as well
      response.cookies.set('token', token, {
        path: '/',
        maxAge: 7 * 24 * 60 * 60, // 7 days
        httpOnly: false,
        secure: true,
        sameSite: 'strict',
      });

      return response;
    }

    return NextResponse.json({ error: 'Credenciais inválidas' }, { status: 401 });
  } catch (error) {
    return NextResponse.json({ error: 'Erro no servidor' }, { status: 500 });
  }
}
