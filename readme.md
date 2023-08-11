# How and why

- For this assignment and the exercise before it, I went deeper into the material than requested.
  This because I especially wanted to learn more about Flask and put it into practice right away.
  I really enjoyed working with React in the frontend course and was very curious about Flask.
  I understand that Flask and React work well together, although I lacked the time to apply it here.
- Most of the arguments to the requested functions are given via forms. I found it therefore necessary to adjust the parameters for some functions.
- All models for the different tables are in a separate file in the database folder under models.  
  I could have chosen to develop a base model that has the database in the Meta class en let all classes inherit from this base class, but I solved it this way because I prefer to have things in separate files. Maybe it is more memory expensive, in that case, please let me know.
  I did it this way to avoids large amounts of code as in the blueprints for the Flask app. Those I find less clear.
- The requested functions are in the `functions` folder under `models`
- There is a `betsy_webshop.uxf` in the `database` folder in which I drew a strip chart. You can easily view it by installing the `UMLet` extension in VS Code.

### Bonus requirements

- The search targets both the name and description. I made use of `Product.name.contains` over two table colums. You can search with a word, a letter or even een empty string if
  you wanted to. That makes up for the missing spelling error bonus ;-)

- For the index bonus I only have indexed the description field of the Product table. This is because I have already created a number of unique fields that, as far as I
  can make out in the documentation, automatically get an index. For all other fields, there could be a lot of the same data or there will not be searched on.
  When many of the same data are filled there will be low cardinality. From what I have learned creating an index on a low cardinality column is not preferable because it returns multiple records upon querying it, resulting in overall query execution time which degrades the database performance.

- I didn't make time for the spelling-error bonus. I think the idea is to create an extra table where the correctly spelled products are linked to misspelled products.
  If there is an easier way to do this i would love to hear it

### Comment

- It took me some time to figure out what you meant by: `The tags should not be duplicated`, because it wasn't referenced at all. At first I was looking for whether this meant
  the names of columns. Anyway, I'm going to assume I've implemented it correctly.

- I enjoyed doing this assignment and I assume that you have the opportunity to assess the assignment in this way. If possible, I would like to receive comments on how other
  parts of the application can be improved. Thank you in advance.

# How to use?

- copy the app directory in a new project folder
- cd into this new project folder
- install a virtual environment, when done activate the virtual environment

        python -m venv .venv

        #windows
        .venv\Scripts\activate

        #linux macOS
        .venv/bin/activate

- after that install flask and peewee

        pip install flask and peewee

        # check which packages are installed in the virual environment
        pip list

- get the app.db database up and running

        flask --app app init-db

- get the app up and running on 127.0.0.1:5000

        flask --app app run --debug

- go to the website
- register an account by clicking Register in the navbar and fill in the requested information
- log in with the form you are redirected to
- clicking the dropdown button you get the option to choose Exercise or Betsy Webshop, after which several links become available
