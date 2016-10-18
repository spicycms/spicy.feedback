begin;
alter table fb_pattern add column token varchar(255);
alter table fb_pattern add column url_to_api varchar(300);
commit;