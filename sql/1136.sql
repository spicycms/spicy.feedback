begin;
set constraints all immediate;

ALTER TABLE fb_feedback ADD COLUMN var1 varchar(255);
UPDATE fb_feedback SET var1 = '';
alter table fb_feedback alter column var1 set not null;
ALTER TABLE fb_feedback ADD COLUMN var2 varchar(255);
UPDATE fb_feedback SET var2 = '';
alter table fb_feedback alter column var2 set not null;
ALTER TABLE fb_feedback ADD COLUMN var3 varchar(255);
UPDATE fb_feedback SET var3 = '';
alter table fb_feedback alter column var3 set not null;
commit;


