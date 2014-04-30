begin;
alter table fb_pattern rename email_template to template_name;
alter table fb_pattern rename email_body to content;
commit;
