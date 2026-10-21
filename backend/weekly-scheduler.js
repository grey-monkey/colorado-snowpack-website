// Only dispatch the existing workflow. Kit and the edition ledger stay downstream.
export const WEEKLY_CRON = '17 15 * * 1';
export const DISPATCH_URL = 'https://api.github.com/repos/grey-monkey/colorado-snowpack-website/actions/workflows/weekly.yml/dispatches';

export async function dispatchWeekly(controller, env) {
 const mode = env.WEEKLY_SCHEDULER_MODE;
 if (!['dry_run', 'enabled'].includes(mode)) return;
 if (mode === 'enabled' && env.NEWSLETTER_MODE !== 'enabled') return;
 const scheduled = new Date(controller.scheduledTime);
 if (controller.cron !== WEEKLY_CRON || !Number.isFinite(scheduled.getTime()) ||
     scheduled.getUTCDay() !== 1 || scheduled.getUTCHours() !== 15 || scheduled.getUTCMinutes() !== 17) {
  throw Error('Unexpected weekly schedule');
 }
 if (!env.WEEKLY_DISPATCH_TOKEN) throw Error('Weekly dispatch credential is missing');
 const scheduledFor = scheduled.toISOString();
 let response;
 try {
  response = await fetch(DISPATCH_URL, {
   method: 'POST', redirect: 'error', signal: AbortSignal.timeout(15000),
   headers: {
    Authorization: `Bearer ${env.WEEKLY_DISPATCH_TOKEN}`,
    Accept: 'application/vnd.github+json', 'Content-Type': 'application/json',
    'User-Agent': 'ColoradoSnowpack-Weekly-Scheduler',
    'X-GitHub-Api-Version': '2022-11-28'
   },
   body: JSON.stringify({ref: 'readiness-preview', inputs: {
    dry_run: mode === 'dry_run', scheduled_for: scheduledFor
   }})
  });
 } catch {
  // No retry: a lost response may already have dispatched the workflow.
  throw Error('Weekly dispatch uncertain; inspect GitHub Actions before retrying');
 }
 if (response.status !== 204) throw Error(`Weekly dispatch rejected (HTTP ${response.status})`);
 // No token, payload, recipient or provider response is logged.
 console.log(JSON.stringify({status: 'workflow_dispatched', scheduled_for: scheduledFor, dry_run: mode === 'dry_run'}));
}
