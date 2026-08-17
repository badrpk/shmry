const nodemailer = require('nodemailer');

class ShmryMailer {
  constructor(options = {}) {
    this.mode =
      options.mode ||
      process.env.SHMRY_MAIL_MODE ||
      'capture';

    this.from =
      options.from ||
      process.env.SHMRY_AUTH_FROM ||
      'auth@shmry.com';

    this.baseUrl =
      options.baseUrl ||
      process.env.SHMRY_PUBLIC_URL ||
      'http://localhost:3000';

    this.capture = [];

    this.transporter = null;

    if (this.mode === 'smtp') {
      this.transporter = nodemailer.createTransport({
        host:
          process.env.SHMRY_SMTP_HOST ||
          'smtp.shmry.com',
        port:
          Number(
            process.env.SHMRY_SMTP_PORT ||
            587
          ),
        secure:
          String(
            process.env.SHMRY_SMTP_SECURE ||
            'false'
          ) === 'true',
        auth:
          process.env.SHMRY_SMTP_USER
            ? {
                user: process.env.SHMRY_SMTP_USER,
                pass: process.env.SHMRY_SMTP_PASS,
              }
            : undefined,
      });
    }
  }

  async sendVerification({
    email,
    token,
    otp,
    expiresMinutes,
  }) {
    const link =
      `${this.baseUrl}/api/auth/email/verify`
      + `?token=${encodeURIComponent(token)}`;

    const message = {
      to: email,
      from: this.from,
      subject: 'Your Shmry sign-in link',
      text: [
        'Sign in to Shmry:',
        link,
        '',
        `Fallback code: ${otp}`,
        '',
        `This verification expires in ${expiresMinutes} minutes.`,
      ].join('\n'),
      html: `
        <h2>Sign in to Shmry</h2>
        <p>
          <a href="${link}">
            Continue to Shmry
          </a>
        </p>
        <p>
          Fallback verification code:
          <strong>${otp}</strong>
        </p>
        <p>
          Expires in ${expiresMinutes} minutes.
        </p>
      `,
      link,
      otp,
    };

    if (this.mode === 'capture') {
      this.capture.push(message);
      return {
        mode: 'capture',
        accepted: [email],
      };
    }

    const info =
      await this.transporter.sendMail(message);

    return {
      mode: 'smtp',
      messageId: info.messageId,
      accepted: info.accepted,
      rejected: info.rejected,
    };
  }
}

module.exports = {
  ShmryMailer,
};
