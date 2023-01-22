from sqlalchemy import create_engine
import cryptography

def connectdb():
    engine = create_engine("mysql+pymysql://mbit:mbit@db_pictures:3306/pictures")
    return engine

def insert_picture_and_tags(filename,filesize,tags):
    engine = connectdb()
    with engine.connect() as conn:
        conn.execute(f"INSERT INTO pictures (filename,file_size)  VALUES ('{filename}' , {str(filesize)})")
        result = conn.execute(f"SELECT id FROM pictures WHERE filename = '{filename}'")
        returned_dataset = result.fetchone()[0]

        if tags:
            for tag in tags:
                 tag_value = tag[0]
                 tag_confidence = tag[1]
                 conn.execute(f"INSERT INTO tags (picture_id,tag,confidence)  VALUES ({returned_dataset} , '{tag_value}' , {tag_confidence} )")

def get_images(min_date,max_date,tags):
    SELECT =    f"SELECT id, pic_date  , GROUP_CONCAT(tag) as tag_list"
    FROM =      " FROM pictures p JOIN tags t ON p.id = t.picture_id"
    GROUPBY=    " GROUP BY id, pic_date";

    min_date_condition = f"'{min_date}'" if min_date is not None else 'pic_date'
    max_date_condition = f"'{max_date}'" if max_date is not None else 'pic_date'

    if tags:
       tags_condition =  " AND EXISTS ( SELECT picture_id from tags WHERE tag IN('"+tags.replace(',' , "','" )+"'))"
    else:
       tags_condition = ''

    # Building the where Clause
    where = f" WHERE (pic_date BETWEEN {min_date_condition} AND {max_date_condition}) {tags_condition}"

    query = SELECT + FROM + where +  GROUPBY
    #print(query)

    engine = connectdb()
    with engine.connect() as conn:
        result = conn.execute(query)

        columns = result.keys()
        data = [
            dict(zip(columns, row))
            for row in result
        ]
        return data


def get_image(id):
    query_pictures = f"SELECT id, pic_date,filename, file_size FROM pictures p WHERE id = {id}"
    query_tags = f"SELECT tag, confidence FROM tags WHERE picture_id = {id}"

    engine = connectdb()
    with engine.connect() as conn:
        result = conn.execute(query_tags)
        columns = result.keys()
        tags = [
            dict(zip(columns, row))
            for row in result
        ]

        result = conn.execute(query_pictures)
        columns = result.keys()

        picture = [
            dict(zip(columns, row))
            for row in result
        ]

        filename = picture[0]['filename']

        return picture, tags, filename

def get_tags(min_date,max_date):
    SELECT =    f"SELECT t.tag, min(confidence) as min_confidence, max(confidence) as max_confidence, round(avg(confidence), 2) as mean_confidence, count(id) n_images"
    FROM =      " FROM pictures p JOIN tags t ON p.id = t.picture_id"
    GROUPBY=    " GROUP BY tag";

    min_date_condition = f"'{min_date}'" if min_date is not None else 'pic_date'
    max_date_condition = f"'{max_date}'" if max_date is not None else 'pic_date'

    # Building the where Clause
    where = f" WHERE (pic_date BETWEEN {min_date_condition} AND {max_date_condition})"

    query = SELECT + FROM + where +  GROUPBY

    engine = connectdb()
    with engine.connect() as conn:
        result = conn.execute(query)

        columns = result.keys()
        data = [
            dict(zip(columns, row))
            for row in result
        ]
        return data






