import { CDP, sleep } from './cdp.mjs';

const tabId = process.argv[2];
const files = process.argv.slice(3);
if (!tabId || files.length === 0) {
  throw new Error('usage: node upload_drive_cdp.mjs TAB_ID FILE...');
}

const client = await CDP.attach(`ws://127.0.0.1:9222/devtools/page/${tabId}`);
await client.send('Runtime.enable');
await client.send('Page.enable');
await client.send('DOM.enable');
await client.send('Page.setInterceptFileChooserDialog', { enabled: true });

async function evaluate(expression) {
  const result = await client.send('Runtime.evaluate', {
    expression,
    returnByValue: true,
    awaitPromise: true,
  });
  if (result.exceptionDetails) {
    throw new Error(JSON.stringify(result.exceptionDetails));
  }
  return result.result.value;
}

async function waitFor(predicate, timeoutMs = 20000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const value = await predicate();
    if (value) return value;
    await sleep(250);
  }
  throw new Error('timed out waiting for Drive UI');
}

await evaluate(`(() => {
  const nodes = [...document.querySelectorAll('button, [role="button"]')];
  const button = nodes.find((node) =>
    (node.innerText || node.getAttribute('aria-label') || '').trim() === '新規'
  );
  if (!button) return false;
  button.click();
  return true;
})()`);

await waitFor(async () => evaluate(`(() => {
  const nodes = [...document.querySelectorAll('[role="menuitem"], [role="option"]')];
  return nodes.some((node) =>
    (node.innerText || node.getAttribute('aria-label') || '').includes('ファイルをアップロード')
  );
})()`));

await evaluate(`(() => {
  const nodes = [...document.querySelectorAll('[role="menuitem"], [role="option"]')];
  const item = nodes.find((node) =>
    (node.innerText || node.getAttribute('aria-label') || '').includes('ファイルをアップロード')
  );
  if (!item) return false;
  item.click();
  return true;
})()`);

const chooser = await waitFor(async () => {
  const index = client.events.findIndex((event) => event.method === 'Page.fileChooserOpened');
  if (index < 0) return null;
  return client.events.splice(index, 1)[0].params;
});

await client.send('DOM.setFileInputFiles', {
  files,
  backendNodeId: chooser.backendNodeId,
});

const expected = files.map((path) => path.split('/').pop());
const status = await waitFor(async () => evaluate(`(() => {
  const expected = ${JSON.stringify(expected)};
  const text = document.body.innerText;
  const found = expected.filter((name) => text.includes(name));
  const done = text.includes('アップロード完了') ||
    text.includes('アップロードしました') ||
    found.length === expected.length;
  return done ? { found, bodyTail: text.slice(-1800) } : null;
})()`), 120000);

await sleep(3000);
await client.send('Page.reload', { ignoreCache: true });
await sleep(5000);

const finalState = await evaluate(`(() => {
  const expected = ${JSON.stringify(expected)};
  const text = document.body.innerText;
  return {
    found: expected.filter((name) => text.includes(name)),
    bodyText: text.slice(0, 5000),
  };
})()`);

console.log(JSON.stringify({ uploaded: expected, status, finalState }, null, 2));
client.close();
process.exit(0);
