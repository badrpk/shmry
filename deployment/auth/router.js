const express = require('express');
const rateLimit =
  require('express-rate-limit');

const {
  AuthError,
} = require('./service');

function cookieOptions() {
  return {
    httpOnly: true,
    secure:
      process.env.NODE_ENV ===
      'production',
    sameSite: 'lax',
    path: '/',
  };
}

function buildAuthRouter({
  service,
  store,
}) {
  const router =
    express.Router();

  const startLimiter =
    rateLimit({
      windowMs: 10 * 60 * 1000,
      limit: 5,
      standardHeaders: true,
      legacyHeaders: false,
    });

  const verifyLimiter =
    rateLimit({
      windowMs: 10 * 60 * 1000,
      limit: 10,
      standardHeaders: true,
      legacyHeaders: false,
    });

  function setSessionCookies(
    res,
    result
  ) {
    res.cookie(
      'shmry_sid',
      result.session.id,
      {
        ...cookieOptions(),
        maxAge:
          result.session.expiresAt
          - Date.now(),
      }
    );

    res.cookie(
      'shmry_session',
      result.session.token,
      {
        ...cookieOptions(),
        maxAge:
          result.session.expiresAt
          - Date.now(),
      }
    );
  }

  function currentAuth(req) {
    return service.authenticateSession({
      sessionId:
        req.cookies?.shmry_sid,
      sessionToken:
        req.cookies?.shmry_session,
    });
  }

  router.post(
    '/email/start',
    startLimiter,
    async (req, res) => {
      try {
        const result =
          await service.startEmail(
            req.body?.email
          );

        res.status(202).json(result);
      } catch (error) {
        respondError(res, error);
      }
    }
  );

  router.get(
    '/email/verify',
    verifyLimiter,
    (req, res) => {
      try {
        const result =
          service.verifyMagicToken(
            req.query?.token
          );

        setSessionCookies(
          res,
          result
        );

        res.json({
          status: 'authenticated',
          user: publicUser(
            result.user
          ),
        });
      } catch (error) {
        respondError(res, error);
      }
    }
  );

  router.post(
    '/email/verify-otp',
    verifyLimiter,
    (req, res) => {
      try {
        const result =
          service.verifyOtp({
            verificationId:
              req.body
                ?.verificationId,
            otp:
              req.body?.otp,
          });

        setSessionCookies(
          res,
          result
        );

        res.json({
          status: 'authenticated',
          user: publicUser(
            result.user
          ),
        });
      } catch (error) {
        respondError(res, error);
      }
    }
  );

  router.get(
    '/me',
    (req, res) => {
      const auth =
        currentAuth(req);

      if (!auth) {
        return res
          .status(401)
          .json({
            error:
              'authentication_required',
          });
      }

      res.json({
        user: publicUser(
          auth.user
        ),
      });
    }
  );

  router.get(
    '/sessions',
    (req, res) => {
      const auth =
        currentAuth(req);

      if (!auth) {
        return res
          .status(401)
          .json({
            error:
              'authentication_required',
          });
      }

      const sessions =
        store.listUserSessions(
          auth.user.id
        )
        .map(session => ({
          id: session.id,
          createdAt:
            session.createdAt,
          expiresAt:
            session.expiresAt,
          revoked:
            Boolean(
              session.revokedAt
            ),
          current:
            session.id ===
            auth.session.id,
        }));

      res.json({
        sessions,
      });
    }
  );

  router.post(
    '/sessions/:id/revoke',
    (req, res) => {
      const auth =
        currentAuth(req);

      if (!auth) {
        return res
          .status(401)
          .json({
            error:
              'authentication_required',
          });
      }

      const target =
        store.getSession(
          req.params.id
        );

      if (
        !target ||
        target.userId !==
          auth.user.id
      ) {
        return res
          .status(404)
          .json({
            error:
              'session_not_found',
          });
      }

      store.revokeSession(
        target.id
      );

      res.json({
        status: 'revoked',
        sessionId:
          target.id,
      });
    }
  );

  router.post(
    '/logout',
    (req, res) => {
      const auth =
        currentAuth(req);

      if (auth) {
        service.logout(
          auth.session.id
        );
      }

      res.clearCookie(
        'shmry_sid',
        cookieOptions()
      );

      res.clearCookie(
        'shmry_session',
        cookieOptions()
      );

      res.json({
        status: 'logged_out',
      });
    }
  );

  router.get(
    '/health',
    (_req, res) => {
      res.json({
        status: 'healthy',
        identityOwner: 'shmry',
        primaryMethod:
          'email_magic_link',
        otpFallback: true,
        thirdPartyRequired:
          false,
      });
    }
  );

  return router;
}

function publicUser(user) {
  return {
    id: user.id,
    email: user.email,
    emailVerified:
      user.emailVerified,
    createdAt:
      user.createdAt,
    plan:
      user.plan,
    entitlements:
      user.entitlements,
    trust:
      user.trust,
  };
}

function respondError(
  res,
  error
) {
  if (
    error instanceof AuthError
  ) {
    return res
      .status(400)
      .json({
        error: error.code,
        message:
          error.message,
      });
  }

  console.error(
    'Auth error:',
    error
  );

  return res
    .status(500)
    .json({
      error:
        'internal_error',
    });
}

module.exports = {
  buildAuthRouter,
};
