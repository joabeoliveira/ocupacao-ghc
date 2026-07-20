import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const { pathname } = request.nextUrl;

  // Paths requiring authentication
  const securePaths = ['/dashboard', '/longa-permanencia', '/configuracoes', '/upload', '/desfechos'];
  const isSecurePath = securePaths.some(path => pathname.startsWith(path));

  // If accessing root "/", redirect to dashboard
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // If accessing a secure path without a token, redirect to login
  if (isSecurePath && !token) {
    const response = NextResponse.redirect(new URL('/login', request.url));
    return response;
  }

  // If accessing login page with a valid token, redirect to dashboard
  if (pathname === '/login' && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/', '/login', '/dashboard/:path*', '/longa-permanencia/:path*', '/configuracoes/:path*', '/upload/:path*'],
};
