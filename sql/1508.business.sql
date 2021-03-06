begin;
set constraints all immediate;
alter table fb_pattern add column send_sms boolean not null default false;
alter table fb_pattern alter column send_sms drop default;
alter table fb_pattern add column nexmo_api_key varchar(8) not null default '';
alter table fb_pattern alter column nexmo_api_key drop default;
alter table fb_pattern add column nexmo_secret_key  varchar(8) not null default '';
alter table fb_pattern alter column nexmo_secret_key drop default;
alter table fb_pattern add column sms_from_number varchar(15) not null default '';
alter table fb_pattern alter column sms_from_number drop default;
alter table fb_pattern add column sms_report_numbers text not null default '';
alter table fb_pattern alter column sms_report_numbers drop default;
alter table fb_pattern add column "slug" varchar(50);
update fb_pattern set slug = id;
alter table fb_pattern alter slug set not null;
alter table fb_pattern add unique(slug);
commit;
