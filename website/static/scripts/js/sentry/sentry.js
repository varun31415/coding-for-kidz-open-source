import * as Sentry from '@sentry/browser';
import { Integrations } from '@sentry/tracing';

Sentry.init({
  dsn: 'https://e1cc379dd8b44743a408f535e8115806@o440973.ingest.sentry.io/5415318',
  integrations: [
    new Integrations.BrowserTracing(),
  ],
  tracesSampleRate: 1.0,
});
// TODO: make the script work