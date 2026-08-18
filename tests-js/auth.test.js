const assert = require('assert');

const {
  AuthStore,
} = require('../deployment/auth/store');

const {
  ShmryMailer,
} = require('../deployment/auth/mailer');

const {
  AuthService,
} = require('../deployment/auth/service');

async function main() {
  const store =
    new AuthStore();

  const mailer =
    new ShmryMailer({
      mode: 'capture',
      baseUrl:
        'https://test.shmry.local',
    });

  const service =
    new AuthService({
      store,
      mailer,
      verificationTtlMs:
        60 * 1000,
    });

  const started =
    await service.startEmail(
      'User@Example.com'
    );

  assert.strictEqual(
    started.status,
    'verification_sent'
  );

  assert.strictEqual(
    mailer.capture.length,
    1
  );

  const message =
    mailer.capture[0];

  assert.ok(
    message.link.includes(
      '/api/auth/email/verify'
    )
  );

  assert.match(
    message.otp,
    /^\d{6}$/
  );

  const verification =
    store.getVerification(
      started.verificationId
    );

  assert.ok(
    verification
  );

  assert.notStrictEqual(
    verification.tokenHash,
    message.link
  );

  assert.notStrictEqual(
    verification.otpHash,
    message.otp
  );

  const result =
    service.verifyOtp({
      verificationId:
        started.verificationId,
      otp: message.otp,
    });

  assert.strictEqual(
    result.user.email,
    'user@example.com'
  );

  assert.strictEqual(
    result.user.plan,
    'free'
  );

  assert.strictEqual(
    result.user.entitlements.plan,
    'free'
  );

  assert.strictEqual(
    result.user.emailVerified,
    true
  );

  assert.ok(
    result.session.token
  );

  const authenticated =
    service.authenticateSession({
      sessionId:
        result.session.id,
      sessionToken:
        result.session.token,
    });

  assert.ok(
    authenticated
  );

  assert.strictEqual(
    authenticated.user.id,
    result.user.id
  );

  assert.throws(
    () =>
      service.verifyOtp({
        verificationId:
          started.verificationId,
        otp: message.otp,
      }),
    /already been used/
  );

  service.logout(
    result.session.id
  );

  assert.strictEqual(
    service.authenticateSession({
      sessionId:
        result.session.id,
      sessionToken:
        result.session.token,
    }),
    null
  );

  console.log(
    'SHMRY_FIRST_PARTY_AUTH_CORE=PASS'
  );
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
