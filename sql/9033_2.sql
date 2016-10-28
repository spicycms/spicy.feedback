begin;
alter table fb_pattern add column send_to_api boolean default false;
commit;