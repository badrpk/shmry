const {
  AuthStore,
} = require('./store');

const {
  ShmryMailer,
} = require('./mailer');

const {
  AuthService,
} = require('./service');

const {
  buildAuthRouter,
} = require('./router');

function createShmryAuth(
  options = {}
) {
  const store =
    options.store ||
    new AuthStore();

  const mailer =
    options.mailer ||
    new ShmryMailer(
      options.mailerOptions
    );

  const service =
    options.service ||
    new AuthService({
      store,
      mailer,
    });

  const router =
    buildAuthRouter({
      service,
      store,
    });

  return {
    store,
    mailer,
    service,
    router,
  };
}

module.exports = {
  createShmryAuth,
};
