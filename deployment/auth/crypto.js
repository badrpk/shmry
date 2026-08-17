const crypto = require('crypto');

function randomToken(bytes = 32) {
  return crypto
    .randomBytes(bytes)
    .toString('base64url');
}

function randomOtp() {
  return crypto
    .randomInt(0, 1000000)
    .toString()
    .padStart(6, '0');
}

function sha256(value) {
  return crypto
    .createHash('sha256')
    .update(String(value))
    .digest('hex');
}

function timingSafeHexEqual(a, b) {
  if (!a || !b) {
    return false;
  }

  const aa = Buffer.from(String(a), 'hex');
  const bb = Buffer.from(String(b), 'hex');

  if (aa.length !== bb.length) {
    return false;
  }

  return crypto.timingSafeEqual(aa, bb);
}

module.exports = {
  randomToken,
  randomOtp,
  sha256,
  timingSafeHexEqual,
};
