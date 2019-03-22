begin;
alter table fb_feedback alter COLUMN var1 TYPE text;
alter table fb_feedback alter COLUMN var1 DROP NOT NULL;
commit;
begin;
alter table fb_feedback alter COLUMN var2 TYPE text;
alter table fb_feedback alter COLUMN var2 DROP NOT NULL;
commit;
begin;
alter table fb_feedback alter COLUMN var3 TYPE text;
alter table fb_feedback alter COLUMN var3 DROP NOT NULL;
commit;

