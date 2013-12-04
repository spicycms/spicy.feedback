begin;
set constraints all immediate;

ALTER TABLE fb_pattern ADD COLUMN use_captcha boolean default false not null;
UPDATE fb_pattern SET use_captcha = false;

ALTER TABLE fb_pattern ADD COLUMN auto_signup boolean default true not null;
UPDATE fb_pattern SET auto_signup = true;

commit;
