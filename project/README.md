# UNISTORE
A web application named UNISTORE is constructed for U.S. college and university students to sell and buy second-hand products online using Python(Flask), SQLite3, HTML, CSS, JavaScript, Bootstrap, and Jinja2.

View demo on https://youtu.be/xeIeQ9Pz5ZM

## HTML Pages:
1. Register, Login, and Logout Page:\
  Site users can register for the web application with a unique username and password. Users are able to log in and log out of the website.

2. Index Page/Product Page/Main Page:\
Once logged in, site users are taken to the home page which contains all products that are sold by college and university students. On this main page, there is a filter section allowing site users to filter products by keywords, price range, location, and types. Products can be sorted by price from high to low and from low to high. By clicking the name of the product, the website directs to the product page containing more information about a particular product. Site users are able to add any item to the shopping cart.
3. Product Page\
A product page has detailed information (price, description, selling address, etc.) about a specific product. Site users are able to add an item to the shopping cart on this page.
4. Shopping Cart Page\
It is the page where users can pile up what they want to buy from the website and then simply check out all items in the cart. Users can return to the main page by clicking the “continue shopping” button.
5. Profile Page\
It is the page that contains the site user’s profile picture, saving amount, and transaction history. A site user is able to save money and change username on this page. Users can change their profile pictures by choosing profile pictures from their local computers. Without enough money, site users are not able to purchase second-hand products.
6. Selling Page\
Users can input the necessary information about products that they want to sell.\
Following details needed to provide in order to sell a product:
    * name: the name of the product
    * price: the price of the product in dollars
    * university: the unviersity of the product, where buyers can pickup product at
    * address: the unviersity address of the product, where buyers can pickup the product at
    * type: the type of the product. Site users should choose an option from either “furniture”, “book”, “kitchen”, or “other”
    * Description: the description of the product
    * Product Picture: the picture of the product in jpg or png format
## Database
After performing data wrangling and data collecting processes, I created a relational SQL database on disk-based SQLite using sqlite3 in Python. There are four tables in the database, which are transactions, transations_info, users, products, and university table.
  * **3NF Normalization**\
I used 3NF decomposition to normalize the dependencies. Thus, I could ensure that there are no redundancy after the decomposition and there were only minimal dependencies. With 3NF, I was able to guarantee lossless join and dependency preservation.
  * **Indexing**\
Creating a SQL index help system retrieve data from a database very fast. In this project, indexing was used to improve the performance of queries and applications. I applied the indexing technique on username since every user needs to log in with a username if they want to view this website. Username is a feature searched frequently in my SQL database. I also created an index on the "university" column of the products table because "university" is a foreign key to connect the products table and the university table. It is a frequently used key while searching addresses for products. So I created a key to improve SQL performance.
 * **Table Design**\
 The following is the design of my database:
    * transactions: order_num, product_id(PRIMARY KEY)
    * transactions_info: order_num(PRIMARY KEY), time, price, buyer_id
    * users: id INTEGER(PRIMARY KEY), username, hash, money, image_file
    * products: id INTEGER(PRIMARY KEY), name, seller, price, description, university, type, sold, image
    * university: id(PRIMARY KEY), name, address

## Some Configuration
````
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'xxx'
````

## Technical Details
* Python(Flask)\
I used python to clean datasets. I used the web framework FLASK to build a server which receiving requests and sending relevant data for my web application.
* SQLite3\
I created a relational SQL database on disk-based SQLite using sqlite3 in Python.
* HTML\
I wrote 8 HTML documents to be display information in a web browser.
* CSS\
CSS is used to style HTML documents
* JavaScript\
I used JavaScript to dynamically change the view of the page without making a server request.
* Bootstrap\
I used the free and open-source CSS framework provided by Bootstrap to design buttons, text boxes, and others on my HTML pages.
* Jinja2\
I usd Jinja2 to write for loops, write if statement, and clarify python variable in HTML pages.
