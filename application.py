#!/usr/bin/env python
# 
# application.py -- implementation of a Catalog
#


from flask import Flask, jsonify, render_template, request, redirect
import psycopg2
import psycopg2.extras

app = Flask(__name__)

catalog = {
  "category" : [
    {
      "id": 1,
      "name": "Soccer",
      "Items": [
          {
              "cat_id": 1, 
              "description": "The shoes",
              "id": 1,
              "title": "Soccer Cleats"
          },
          {
              "cat_id": 1,
              "description": "The shirt",
              "id": 2, 
              "title": "Jersey"
          }
      ]
    },
      {
          "id": 2,
          "name": "Basketball"
    },
      {
          "id": 3,
          "name": "Baseball",
          "Items": [
              {
                  "cat_id": 3,
                  "description": "The bat",
                  "id": 3,
                  "title": "Bat"
              }
        ]
      },
      {
          "id": 4,
          "name": "Fresbee"
    },
      {
          "id": 5,
          "name": "Snowboarding",
          "Items": [
              {
                "cat_id": 5,
                  "description": "Best of any terrain",
                  "id": 7,
                  "title": "Snowboard"
              }
          ]
    },
      {
          "id": 6,
          "name": "Rock Climbing"
      },
      {
        "id": 7,
          "name": "Foosball"
      },
      {
          "id": 8,
          "name": "Skating"
      },
    {
        "id": 9,
        "name": "Hockey"
    }
  ],
    "latest_items": [
        {
            "cat_id": 5,
            "cat_name": "Snowboarding",
            "description": "Best of any terrain",
            "id": 7,
            "title": "Snowboard"
        },
        {
            "cat_id": 3,
          "cat_name": "Baseball",
            "description": "The bat",
            "id": 3,
            "title": "Bat"          
        },
        {
            "cat_id": 1,
            "cat_name": "Soccer",
            "description": "The shoes",
            "id": 1,
            "title": "Soccer Cleats"
        }
    ]
}

valid_actions = ["add", "edit", "delete"]

# DB configuration:

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=catalog")

# DB extraction

def get_json():
    """
    Construct json, representing the whole catalog.
    """
    conn = connect()
    
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            category_list = curs.fetchall("SELECT * FROM categories")
            items_list = curs.fetchall("SELECT * FROM items")
            
    conn.close()

    return jsonify(catalog)

def get_item_by_title_db(item_title):
    """
    Return Item entry having title equal to provided item_title value
    or None.
    Note: there might be many items, having the same title, so this will
    return the first one.
    """
    conn = connect()
    
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM items WHERE title=%s", (item_title,))
            items = curs.fetchone()
            
    conn.close()

    return items
    
def get_category_by_id_db(cat_id):
    """
    Return Category entry that contains Item with provided item_id
    or None.
    Note: there might be many Categories, having the porvided item,
    so this will return the first one.
    """
    conn = connect()
    
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM categories WHERE id=%s", (cat_id,))
            category = curs.fetchone()
        
    conn.close()

    return category

def get_item_db(category_name, item_title):
    """
    This function returns the result of quering catalog
    based on category's name and item's title in this category.
    Returned result is one of:
    1) item with title equal to 'item_title' and residing in
    category with name equal to 'category_name'
    2) None
    """
    items = None

    conn = connect()

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM categories WHERE name=%s",
                         (category_name,))
            category = curs.fetchone()
    
    if (category):
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
                curs.execute("SELECT * FROM items WHERE cat_id=%s",
                             (category[0],))
                items_list = curs.fetchall()
                items = [item for item in items_list
                         if (item['title'] == item_title)]

    conn.close()

    if (items):
        return items[0]
    else:
        return None

def get_items_db(category_name):
    """
    This function returns the result of quering catalog
    based on category's name and item's title in this category.
    Returned result is one of:
    1) list of items residing in category with name equal to 
    'category_name'
    2) None
    """
    conn = connect()

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM categories WHERE name=%s",
                         (category_name,))
            category = curs.fetchone()
            
    if (category):
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
                curs.execute("SELECT * FROM items WHERE cat_id=%s",
                             (category['id'],))
                items_list = curs.fetchall()

    conn.close()

    return items_list

def get_categories_db():
    """
    This function returns the result of quering catalog
    based on category's name and item's title in this category.
    Returned result is one of:
    1) item with title equal to 'item_title' and residing in
    category with name equal to 'category_name'
    2) None
    """
    conn = connect()

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM categories")
            category_list = curs.fetchall()
    
    conn.close()
    
    return category_list

def delete_item_db(item_title):
    """
    This function deletes one item based on provided parameter.
    Returns 1 or None.
    """
    conn = connect()

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM items WHERE title=%s",
                         (item_title,))
            item = curs.fetchone()

            if (item):
                curs.execute("DELETE FROM items WHERE id=%s",
                             (int(item['id']),))
                ret = 1

    conn.close()

    return ret

def edit_item_db(item_original_title, item_original_description, item_title, item_description, category_name):
    """
    This function edits one item based on provided parameters.
    Returns 1 or None.
    """
    conn = connect()
    ret = None

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:

            curs.execute("SELECT * FROM categories WHERE name=%s",
                         (category_name,))
            category_list = curs.fetchall()

            curs.execute("SELECT * FROM items WHERE title=%s AND description=%s",
                         (item_original_title, item_original_description))
            item_list = curs.fetchall()
            
            if (category_list and item_list):
                for category in category_list:
                    for item in item_list:
                        if (item['cat_id'] == category['id']):
                            curs.execute("UPDATE items SET title=%s, description=%s WHERE id=%s", (item_title,item_description,int(item['id'])))
                            ret = 1

    conn.close()

    return ret

def add_item_db(item_title, item_description, category_name):
    """
    This function adds one item with provided parameters.
    Returns 1 or None.
    """
    conn = connect()
    ret = None
    print 'Received params:'
    print item_title, item_description, category_name
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM categories WHERE name=%s",
                         (category_name,))
            category = curs.fetchone()

            if (category):
                cat_id = int(category['id'])
                print 'cat_id=',cat_id
                curs.execute("INSERT INTO items (cat_id,title,description) VALUES (%s,%s,%s);", (cat_id,item_title,item_description))
                ret = 1

    conn.close()

    return ret
    
def get_latest_items_db():
    """
    This function returns the result of quering catalog
    based on category's name and item's title in this category.
    Returned result is one of:
    1) item with title equal to 'item_title' and residing in
    category with name equal to 'category_name'
    2) None
    """
    conn = connect()

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute("SELECT * FROM items ORDER BY id DESC LIMIT 5")
            latest_items_list = curs.fetchall()

    conn.close()

    return latest_items_list

# Enpoints configuration

@app.route('/')
def catalog_app():
    """
    HTTP request handler.
    Renders 'catalog.html' template with fetched values. 
    """
    categories = get_categories_db()
    latest = get_latest_items_db()
    return render_template('catalog.html', categories=categories, latest=latest)

@app.route('/catalog.json')
def catalog_json():
    """
    HTTP request handler.
    Returns json, representing catalog data.
    """
    return get_json()

@app.route('/catalog/add', methods=["GET"])
def add_item():
    """
    HTTP request handler.
    Renders 'edit.html' template with empty values.
    Note: template for adding a new item is the same as editing new item.
    """
    categories = get_categories_db()
    
    return render_template('edit.html', item={"title":"", "description":""},
                           categories=categories, category={})

@app.route('/catalog/add', methods=['POST'])
def add_item_redirect():
    """
    HTTP request handler.
    Inserts new item into database and redirects to '/'
    """
    item_title = request.form['title']
    item_description = request.form['description']
    category_name = request.form['categories']

    ret = add_item_db(item_title, item_description, category_name)

    if (ret):
        return redirect('/')
    else:
        return render_template('error.html')

@app.route('/catalog/<item>/delete', methods=["GET"])
def delete_item(item):
    """
    HTTP request handler.
    Renders 'delete.html' template.
    """
    return render_template('delete.html', item=item)

@app.route('/catalog/delete', methods=['POST'])
def delete_item_redirect():
    """
    HTTP request handler.
    Deletes item from database and redirects to '/'
    """
    item_title = request.form['item_title']

    ret = delete_item_db(item_title)

    if (ret):
        return redirect('/')
    else:
        return render_template('error.html')

@app.route('/catalog/<item>/edit', methods=["GET"])
def edit_item(item):
    """
    HTTP request handler.
    Renders 'edit.html' template with fetched values or
    'error.html' template if any errors occurred.
    """
    it = get_item_by_title_db(item)

    if (it):
        category = get_category_by_id_db(int(it['cat_id']))
        categories = get_categories_db()

        return render_template('edit.html', item=it, categories=categories,
                               category=category)
    else:
        return render_template('error.html')

@app.route('/catalog/edit', methods=['POST'])
def edit_item_redirect():
    """
    HTTP request handler.
    Inserts new item into database and redirects to '/'
    """
    item_original_title = request.form['original_title']
    item_original_description = request.form['original_description']
    item_title = request.form['title']
    item_description = request.form['description']
    category_name = request.form['categories']

    ret = edit_item_db(item_original_title, item_original_description, item_title, item_description, category_name)

    if (ret):
        return redirect('/')
    else:
        return render_template('error.html')

@app.route('/catalog/<category>/<item>')
def category(category, item):
    """
    HTTP request handler.
    Renders 'items.html' template with fetched values or
    'item.html' template depending on last part of the path.
    If any errors occur, renders 'error.html' template.
    # TODO: make case insensitive?
    """
    if (item == 'items'):
        items = get_items_db(category)
        if (items):
            return render_template('items.html',
                                   categories=catalog["category"],
                                   category=category, items=items)
        else:
            return render_template('error.html')
    else:
        item = get_item_db(category, item)
        if (item):
            return render_template('item.html', item=item,
                                   category=category)
        else:
            return render_template('error.html')

if __name__ == '__main__':
    app.debug = True # TODO: remove debug
    app.run(port=8000)
