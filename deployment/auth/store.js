const crypto = require('crypto');

class AuthStore {
  constructor() {
    this.users = new Map();
    this.usersByEmail = new Map();
    this.verifications = new Map();
    this.sessions = new Map();
    this.audit = [];
  }

  newId(prefix) {
    return `${prefix}_${crypto.randomUUID()}`;
  }

  now() {
    return Date.now();
  }

  normalizeEmail(email) {
    return String(email || '')
      .trim()
      .toLowerCase();
  }

  getUserByEmail(email) {
    const normalized = this.normalizeEmail(email);
    const id = this.usersByEmail.get(normalized);
    return id ? this.users.get(id) : null;
  }

  createOrActivateUser(email) {
    const normalized = this.normalizeEmail(email);

    let user = this.getUserByEmail(normalized);

    if (!user) {
      const now = this.now();

      user = {
        id: this.newId('usr'),
        email: normalized,
        emailVerified: true,
        createdAt: now,
        verifiedAt: now,
        lastLoginAt: now,
        plan: 'free',
        entitlements: {
          plan: 'free',
          active: true,
        },
        trust: {
          level: 'email_verified',
          secondFactorVerified: false,
        },
      };

      this.users.set(user.id, user);
      this.usersByEmail.set(normalized, user.id);
    } else {
      user.emailVerified = true;
      user.lastLoginAt = this.now();
    }

    return user;
  }

  saveVerification(record) {
    this.verifications.set(record.id, record);
    return record;
  }

  getVerification(id) {
    return this.verifications.get(id) || null;
  }

  saveSession(session) {
    this.sessions.set(session.id, session);
    return session;
  }

  getSession(id) {
    return this.sessions.get(id) || null;
  }

  revokeSession(id) {
    const session = this.sessions.get(id);

    if (!session) {
      return false;
    }

    session.revokedAt = this.now();
    return true;
  }

  listUserSessions(userId) {
    return Array.from(this.sessions.values())
      .filter(session => session.userId === userId);
  }

  recordAudit(event) {
    this.audit.push({
      id: this.newId('evt'),
      at: this.now(),
      ...event,
    });
  }
}

module.exports = {
  AuthStore,
};
