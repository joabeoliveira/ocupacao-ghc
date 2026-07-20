import { getCookie } from './utils';

const API_URL = (process.env.NEXT_PUBLIC_API_URL || '').replace(/\/+$/, '');

/** Remove prefixo /api do path se a API_URL já termina com /api */
function buildUrl(path: string): string {
  const cleanPath = API_URL && /\/api$/.test(API_URL) ? path.replace(/^\/api/, '') : path;
  return `${API_URL}${cleanPath}`;
}

export const api = {
  async get(path: string, options?: { params?: Record<string, any> }) {
    let url = buildUrl(path);
    if (options?.params) {
      const q = new URLSearchParams();
      Object.entries(options.params).forEach(([k, v]) => {
        if (v !== undefined && v !== null) {
          q.append(k, String(v));
        }
      });
      const qStr = q.toString();
      if (qStr) {
        url += (url.includes('?') ? '&' : '?') + qStr;
      }
    }
    return this.request(url, { method: 'GET' });
  },

  async post(path: string, data?: any) {
    return this.request(buildUrl(path), {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async put(path: string, data?: any) {
    return this.request(buildUrl(path), {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async delete(path: string) {
    return this.request(buildUrl(path), {
      method: 'DELETE',
    });
  },

  async request(url: string, options: RequestInit = {}) {
    const token = getCookie('token');
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };

    const res = await fetch(url, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      } as Record<string, string>,
    });

    if (res.status === 401) {
      if (typeof window !== 'undefined') {
        document.cookie = 'token=; path=/; max-age=0';
        window.location.href = '/login';
      }
      throw new Error('Unauthorized');
    }

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(errorText || 'API Error');
    }

    return res.json();
  }
};
