create table users(
  email varchar(80) primary key not null,
  username varchar(80) not null
);
create table items(
  itemId serial primary key not null,
  itemName varchar(80) not null,
  description text,
  startPrice money not null,
  ownedBy varchar(80) references users(email) not null
);
create table message(
  messageId serial primary key not null,
  messTime timestamp not null default now(),
  messText text,
  senderID varchar(80) references users(email) not null,
  receiverID varchar(80) references users(email) not null
);
create table auction(
  auctionId serial primary key not null,
  startTime timestamp not null,
  endTime timestamp not null,
  endPrice money not null,
  buyerID varchar(80) references users(email),
  itemSelling serial references items(itemId) not null
);

create table category(
  catId serial primary key not null,
  catName varchar(80) not null
);

create table friends(
  friend1 varchar(80) references users(email) not null,
  friend2 varchar(80) references users(email) not null,
  dateAdded timestamp not null default now(),
  primary key(friend1, friend2)
);

create table search(
  searchID serial primary key not null,
  searchText text,
  searchUser varchar(80) references users(email) not null
);

create table item_types(
  itemId serial references items(itemId) not null,
  catId serial references category(catId) not null,
  primary key(itemid, catid)
);

create table bid(
  auctionId serial references auction(auctionId) not null,
  bidder varchar(80) references users(email) not null,
  bidPrice money not null, 
  bidTime timestamp not null default now(),
  primary key(auctionId, bidder, bidPrice, bidTime)
);

create table chat(
  chatId serial primary key not null,
  chatText text,
  chatTime timestamp,
  chatter varchar(80) references users(email) not null,
  auctionId serial references auction(auctionId) not null
);

