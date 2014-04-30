begin;
alter table fb_pattern rename email_template to template_name;
alter table fb_pattern add column content text not null default '';
alter table fb_pattern alter column content drop default;
commit;
