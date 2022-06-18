# wkflws_aftership
This Trigger Node is for picking up the `tracking_update` webhook event from AfterShip.

## Node Configuration
Aftership webhooks contain [a signature](https://www.aftership.com/docs/aftership/webhook/webhook-signature) in the payload header: `aftership-hmac-sha256`. To lookup the associated user's workflow, request user to provide their "Webhook Secret" found in Settings > Webhooks. Once provided encrypt it as base64-encoded HMAC using sha256 algorithm and store the webhook secret to the database.