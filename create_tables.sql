
use pictures;

create table if not exists pictures
(id integer AUTO_INCREMENT, 
 filename VARCHAR(260),
 file_size INT,
 pic_date  timestamp DEFAULT CURRENT_TIMESTAMP ,
 PRIMARY KEY(id)
 );
 
create table if not exists tags
(tag VARCHAR(32), 
 picture_id integer,
 confidence int,
 tag_date timestamp DEFAULT CURRENT_TIMESTAMP ,
 PRIMARY KEY(tag, picture_id),
 FOREIGN KEY(picture_id) REFERENCES pictures(id)
 );

 
 