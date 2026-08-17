const {
  randomOtp,
  randomToken,
  sha256,
  timingSafeHexEqual,
} = require('./crypto');

class AuthError extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'AuthError';
    this.code = code;
  }
}

class AuthService {
  constructor({
    store,
    mailer,
    verificationTtlMs = 10 * 60 * 1000,
    sessionTtlMs = 30 * 24 * 60 * 60 * 1000,
    maxVerifyAttempts = 5,
  }) {
    this.store = store;
    this.mailer = mailer;
    this.verificationTtlMs =
      verificationTtlMs;
    this.sessionTtlMs =
      sessionTtlMs;
    this.maxVerifyAttempts =
      maxVerifyAttempts;
  }

  normalizeEmail(email) {
    const normalized =
      this.store.normalizeEmail(email);

    if (
      !normalized ||
      !normalized.includes('@') ||
      normalized.length > 320
    ) {
      throw new AuthError(
        'invalid_email',
        'A valid email address is required.'
      );
    }

    return normalized;
  }

  async startEmail(email) {
    const normalized =
      this.normalizeEmail(email);

    const token = randomToken(32);
    const otp = randomOtp();

    const now = this.store.now();

    const record = {
      id: this.store.newId('ver'),
      email: normalized,
      tokenHash: sha256(token),
      otpHash: sha256(otp),
      createdAt: now,
      expiresAt:
        now + this.verificationTtlMs,
      usedAt: null,
      attempts: 0,
    };

    this.store.saveVerification(record);

    await this.mailer.sendVerification({
      email: normalized,
      token,
      otp,
      expiresMinutes:
        Math.ceil(
          this.verificationTtlMs / 60000
        ),
    });

    this.store.recordAudit({
      type: 'email_verification_started',
      email: normalized,
      verificationId: record.id,
    });

    return {
      status: 'verification_sent',
      verificationId: record.id,
      email: normalized,
    };
  }

  verifyRecord(record, candidate, kind) {
    if (!record) {
      throw new AuthError(
        'verification_not_found',
        'Verification request not found.'
      );
    }

    if (record.usedAt) {
      throw new AuthError(
        'verification_used',
        'Verification has already been used.'
      );
    }

    if (this.store.now() > record.expiresAt) {
      throw new AuthError(
        'verification_expired',
        'Verification has expired.'
      );
    }

    if (
      record.attempts >=
      this.maxVerifyAttempts
    ) {
      throw new AuthError(
        'verification_locked',
        'Verification attempt limit reached.'
      );
    }

    record.attempts += 1;

    const candidateHash =
      sha256(candidate);

    const expected =
      kind === 'token'
        ? record.tokenHash
        : record.otpHash;

    if (
      !timingSafeHexEqual(
        candidateHash,
        expected
      )
    ) {
      throw new AuthError(
        'verification_invalid',
        'Verification value is invalid.'
      );
    }

    record.usedAt = this.store.now();

    return record;
  }

  completeVerification(record) {
    const user =
      this.store.createOrActivateUser(
        record.email
      );

    const sessionToken =
      randomToken(32);

    const session = {
      id: this.store.newId('ses'),
      userId: user.id,
      secretHash: sha256(sessionToken),
      createdAt: this.store.now(),
      expiresAt:
        this.store.now()
        + this.sessionTtlMs,
      revokedAt: null,
    };

    this.store.saveSession(session);

    this.store.recordAudit({
      type: 'login_success',
      userId: user.id,
      sessionId: session.id,
    });

    return {
      user,
      session: {
        id: session.id,
        token: sessionToken,
        expiresAt: session.expiresAt,
      },
    };
  }

  verifyMagicToken(token) {
    if (!token) {
      throw new AuthError(
        'missing_token',
        'Token is required.'
      );
    }

    const tokenHash =
      sha256(token);

    const record =
      Array.from(
        this.store.verifications.values()
      ).find(
        item =>
          item.tokenHash === tokenHash
      );

    const verified =
      this.verifyRecord(
        record,
        token,
        'token'
      );

    return this.completeVerification(
      verified
    );
  }

  verifyOtp({
    verificationId,
    otp,
  }) {
    if (!verificationId || !otp) {
      throw new AuthError(
        'missing_otp',
        'Verification ID and OTP are required.'
      );
    }

    const record =
      this.store.getVerification(
        verificationId
      );

    const verified =
      this.verifyRecord(
        record,
        otp,
        'otp'
      );

    return this.completeVerification(
      verified
    );
  }

  authenticateSession({
    sessionId,
    sessionToken,
  }) {
    const session =
      this.store.getSession(sessionId);

    if (
      !session ||
      session.revokedAt ||
      this.store.now() >
        session.expiresAt
    ) {
      return null;
    }

    const suppliedHash =
      sha256(sessionToken || '');

    if (
      !timingSafeHexEqual(
        suppliedHash,
        session.secretHash
      )
    ) {
      return null;
    }

    const user =
      this.store.users.get(
        session.userId
      );

    if (!user) {
      return null;
    }

    return {
      user,
      session,
    };
  }

  logout(sessionId) {
    return this.store.revokeSession(
      sessionId
    );
  }
}

module.exports = {
  AuthError,
  AuthService,
};
