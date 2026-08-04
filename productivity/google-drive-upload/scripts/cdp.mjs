// Minimal dependency-free CDP client using Node 22's global WebSocket.
const BASE = 'http://127.0.0.1:9222';

export async function targets() {
  const r = await fetch(`${BASE}/json/list`);
  return r.json();
}

export class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = []; }

  static async attach(wsUrl) {
    const ws = new WebSocket(wsUrl);
    const c = new CDP(ws);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    ws.onmessage = (m) => {
      const msg = JSON.parse(m.data);
      if (msg.id !== undefined && c.pending.has(msg.id)) {
        const { res, rej } = c.pending.get(msg.id);
        c.pending.delete(msg.id);
        msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
      } else if (msg.method) {
        c.events.push(msg);
      }
    };
    return c;
  }

  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    this.ws.send(JSON.stringify(payload));
    return new Promise((res, rej) => {
      this.pending.set(id, { res, rej });
      setTimeout(() => {
        if (this.pending.has(id)) { this.pending.delete(id); rej(new Error(`timeout: ${method}`)); }
      }, 60000);
    });
  }

  close() { this.ws.close(); }
}

export async function pageByUrl(match) {
  const ts = await targets();
  return ts.find(t => t.type === 'page' && t.url.includes(match));
}

export const sleep = (ms) => new Promise(r => setTimeout(r, ms));
