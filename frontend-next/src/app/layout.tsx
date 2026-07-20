import { Inter, JetBrains_Mono } from 'next/font/google';
import { Providers } from '@/components/providers';
import { AppShell } from '@/components/layout/AppShell';
import '@/app/globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});

export const metadata = {
  title: 'Painel de Regulação e Censo Hospitalar | GHC',
  description: 'Sistema de Monitoramento de Longa Permanência e Atuações do EGAA do Grupo Hospitalar Conceição.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="bg-slate-50 text-slate-900 font-sans antialiased min-h-screen">
        <Providers>
          <AppShell>{children}</AppShell>
        </Providers>
      </body>
    </html>
  );
}
