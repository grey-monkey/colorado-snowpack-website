import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import worker from '../backend/worker.js';
import {dispatchWeekly, WEEKLY_CRON, DISPATCH_URL} from '../backend/weekly-scheduler.js';

test('cron dispatch preserves UTC time, exact workflow/ref and safe dry-run inputs', async () => {
 const original = globalThis.fetch;
 const log = console.log;
 const calls = [], logs = [];
 globalThis.fetch = async (url, options) => { calls.push({url, options}); return new Response(null, {status: 204}); };
 console.log = line => logs.push(line);
 const event = time => ({cron: WEEKLY_CRON, scheduledTime: Date.parse(time)});
 const env = {WEEKLY_SCHEDULER_MODE: 'enabled', NEWSLETTER_MODE: 'enabled', WEEKLY_DISPATCH_TOKEN: 'fake-test-token'};
 try {
  assert.equal(worker.scheduled, dispatchWeekly);
  // Mondays on both sides of the US daylight-saving change.
  for (const time of ['2026-10-26T15:17:00Z', '2026-11-02T15:17:00Z']) {
   await worker.scheduled(event(time), env);
   const {url, options} = calls.at(-1);
   assert.equal(url, DISPATCH_URL);
   assert.equal(options.method, 'POST');
   assert.equal(options.redirect, 'error');
   assert.equal(options.headers.Authorization, 'Bearer fake-test-token');
   assert.ok(options.signal instanceof AbortSignal);
   assert.deepEqual(JSON.parse(options.body), {ref: 'readiness-preview', inputs: {dry_run: false, scheduled_for: new Date(time).toISOString()}});
  }
  await worker.scheduled(event('2026-10-26T15:17:00Z'), {...env, WEEKLY_SCHEDULER_MODE: 'dry_run'});
  assert.equal(JSON.parse(calls.at(-1).options.body).inputs.dry_run, true);
  assert.ok(logs.every(line => !line.includes('fake-test-token')));
  assert.equal(calls.length, 3);
  for (const mode of [undefined, 'off', 'true', 'invalid']) await worker.scheduled(event('2026-10-26T15:17:00Z'), {...env, WEEKLY_SCHEDULER_MODE: mode});
  for (const mode of [undefined, 'disabled', 'private']) await worker.scheduled(event('2026-10-26T15:17:00Z'), {...env, NEWSLETTER_MODE: mode});
  assert.equal(calls.length, 3);
  await assert.rejects(worker.scheduled(event('2026-10-26T15:17:00Z'), {...env, WEEKLY_DISPATCH_TOKEN: ''}), /credential/);
  for (const time of ['invalid', '2026-10-25T15:17:00Z', '2026-10-26T16:17:00Z', '2026-10-26T15:18:00Z']) await assert.rejects(worker.scheduled(event(time), env), /Unexpected/);
  await assert.rejects(worker.scheduled({cron: '* * * * *', scheduledTime: Date.parse('2026-10-26T15:17:00Z')}, env), /Unexpected/);
  assert.equal(calls.length, 3);
  for (const status of [401, 403, 404, 422, 429, 500]) {
   let attempts = 0;
   globalThis.fetch = async () => { attempts++; return new Response('sensitive response', {status}); };
   await assert.rejects(worker.scheduled(event('2026-10-26T15:17:00Z'), env), new RegExp(`HTTP ${status}`));
   assert.equal(attempts, 1);
  }
  globalThis.fetch = async () => Response.json({workflow_run_id: 123});
  await worker.scheduled(event('2026-10-26T15:17:00Z'), env);
  let attempts = 0;
  globalThis.fetch = async () => { attempts++; throw Error('fake-test-token'); };
  await assert.rejects(worker.scheduled(event('2026-10-26T15:17:00Z'), env), /dispatch uncertain; inspect GitHub/);
  assert.equal(attempts, 1);
 } finally { globalThis.fetch = original; console.log = log; }
});

test('checked-in cron and workflow keep cutover gate, manual dry-run default and send safeguards', () => {
 const config = JSON.parse(readFileSync(new URL('../backend/wrangler.jsonc', import.meta.url)));
 assert.equal(WEEKLY_CRON, '17 15 * * MON');
 assert.deepEqual(config.triggers.crons, [WEEKLY_CRON]);
 assert.equal(config.vars.WEEKLY_SCHEDULER_MODE, 'off');
 assert.ok(config.durable_objects.bindings.some(b => b.name === 'EDITIONS' && b.class_name === 'EditionLedger'));
 const workflow = readFileSync(new URL('../.github/workflows/weekly.yml', import.meta.url), 'utf8');
 assert.match(workflow, /dry_run:[\s\S]*type: boolean\s+default: true/);
 assert.match(workflow, /vars.WEEKLY_SCHEDULER != 'cloudflare'/);
 assert.match(workflow, /vars.WEEKLY_ENABLED == 'true'/);
 assert.match(workflow, /cancel-in-progress: false/);
 assert.match(workflow, /python -m ops.send_weekly/);
 assert.match(workflow, /inputs.dry_run == false/);
 assert.match(workflow, /secrets.AUTOMATION_SECRET/);
});
