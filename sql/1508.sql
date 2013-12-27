begin;
alter table fb_pattern add column "slug" varchar(50);
update fb_pattern set slug = id;
alter table fb_pattern alter slug set not null;
alter table fb_pattern add unique(slug);
commit;
