begin;
set constraints all immediate;

ALTER TABLE fb_feedback ADD COLUMN use_captcha boolean default false not null;
UPDATE fb_feedback SET use_captcha = false;

ALTER TABLE fb_feedback ADD COLUMN auto_signup boolean default true not null;
UPDATE fb_feedback SET auto_signup = true;

commit;
