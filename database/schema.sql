create table blog_post(
    PID int primary key,
    title varchar(255),
    content text,
    pdate varchar(32)
);

create table comment(
    CID int primary key,
    nickname varchar(64),
    email varchar(64),
    content text,
    cdate varchar(32) 
);

create table admins(
    username varchar(32) primary key,
    pwd varchar(32),
    email varchar(64)
);

create table contacts(
    username varchar(32) primary key,
    content text
);