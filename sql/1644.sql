begin;
set constraints all immediate;
alter table fb_pattern add column text_signature text;
UPDATE fb_pattern SET text_signature = '';
alter table fb_pattern alter column text_signature set not null;
commit;
