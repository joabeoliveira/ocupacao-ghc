# Autenticação — JWT Simple

## Esquema

```
[Login] → POST /api/auth/login → { token, usuario }
                                      ↓
                             Cookie httpOnly + localStorage
                                      ↓
                          Next.js Middleware valida token
                                      ↓
                             Redireciona para /login se inválido
```

## Implementação no Backend (FastAPI)

Criar endpoint em `backend/app/routers/auth.py`:

```python
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

SECRET_KEY = "trocar-em-producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"])

# Usuário fixo para MVP (depois migrar para banco)
USUARIO_MVP = {
    "email": "admin@ghc.com.br",
    "senha_hash": pwd_context.hash("admin123"),
    "nome": "Administrador EGAA"
}

class LoginRequest(BaseModel):
    email: str
    senha: str

@router.post("/auth/login")
def login(payload: LoginRequest):
    if payload.email != USUARIO_MVP["email"]:
        raise HTTPException(401, "Credenciais inválidas")
    if not pwd_context.verify(payload.senha, USUARIO_MVP["senha_hash"]):
        raise HTTPException(401, "Credenciais inválidas")
    
    token = jwt.encode({
        "sub": payload.email,
        "nome": USUARIO_MVP["nome"],
        "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"token": token, "usuario": {"nome": USUARIO_MVP["nome"], "email": payload.email}}
```

## Implementação no Frontend (Next.js)

### Login Page (`/login`)

```tsx
'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email('Email inválido'),
  senha: z.string().min(3, 'Mínimo 3 caracteres'),
});

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) { /* erro */; return; }
    const { token } = await res.json();
    document.cookie = `token=${token}; path=/; max-age=${7*24*60*60}; Secure; SameSite=Strict`;
    window.location.href = '/dashboard';
  };

  return ( /* formulário */ );
}
```

### Middleware (`src/middleware.ts`)

```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const isLoginPage = request.nextUrl.pathname === '/login';

  if (!token && !isLoginPage) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  if (token && isLoginPage) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### API Client (`src/lib/api.ts`)

```ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

async function apiClient(path: string, options?: RequestInit) {
  const token = getCookie('token'); // função helper
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });
  if (res.status === 401) {
    document.cookie = 'token=; path=/; max-age=0';
    window.location.href = '/login';
  }
  return res.json();
}
```
