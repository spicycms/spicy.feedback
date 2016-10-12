begin;
alter table fb_pattern add column token boolean default false;
alter table fb_pattern add column url_to_api varchar(300);
commit;