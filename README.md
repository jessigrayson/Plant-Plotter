# Plant-Plotter
Custom harvesting &amp; planting schedule sent to your google  
calendar based on user-created gardens and associated plants  
**Tech Stack**
* **Frontend:** HTML5, CSS, Javascript, AJAX, jQuery, Bootstrap, Bootstrap-Select
* **Backend:** Python3, Flask, PostgreSQL, SQLAlchemy, Jinja
* **API:** Google Calendar with OAuth 2.0

**Contents:**
* [Features & Screen Captures](https://github.com/jessigrayson/Plant-Plotter#features--screen-captures)
* [About the Developer](https://github.com/jessigrayson/Plant-Plotter#about-the-developer)
* [Getting Started](https://github.com/jessigrayson/Plant-Plotter#getting-started)
* [Copying Database to Production](https://github.com/jessigrayson/Plant-Plotter#copying-database-to-production)
* [Edge HTTP Server: Nginx](https://github.com/jessigrayson/Plant-Plotter#edge-http-server-nginx)  
**Phase 2**
* The next sprint will include increasing test coverage
* Implement the Nat’l Oceanic and Atmospheric Admin API to expand access for real-time  
weather analytics to to determine ideal planting timelines by user geolocation.


## Features & Screen Captures
Inspired by horrible lettuce grown in my garden because I harvested too late (even though it looked great)  
> ![Image](static/images/screenshots/PPScreenshot1.png)
> ![Image](static/images/screenshots/PPScreenshot2.png)
> ![Image](static/images/screenshots/PPScreenshot3.png)
> ![Image](static/images/screenshots/PPScreenshot4.png)
> ![Image](static/images/screenshots/PPScreenshot5.png)
> ![Image](static/images/screenshots/PPScreenshot6.png)
> ![Image](static/images/screenshots/PPScreenshot7.png)
> ![Image](static/images/screenshots/PPScreenshot8.png)
> ![Image](static/images/screenshots/PPScreenshot9.png)
> ![Image](static/images/screenshots/PPScreenshot10.png)
> ![Image](static/images/screenshots/PPScreenshot11.png)
> ![Image](static/images/screenshots/PPScreenshot12.png)
> ![Image](static/images/screenshots/PPScreenshot13.png)

## About the Developer
Jessica is a Software Engineer, Product Manager, and Business Operations Leader living in the San Francisco Bay area since Summer 2017.  
She has discovered that she can grow plants that don't die like they did in Phoenix, AZ - but she had a hard time being able to  
track and schedule her vegetable garden in an automated way, so she built Plant Plotter as her first web application. 

What you don't know from [her LinkedIn profile:](https://linkedin.com/jessicagrayson)

She is also a big fan of puzzles, beading, dogs, cheese, and wine.

Jessica has led SaaS product development and implementations most extensively in the healthcare industry. This includes developing system workflows, user interfaces based on business and operational needs, and guiding development teams.These include technological tools and programs to manage digital imaging equipment logistics and a credentialing, licensing, and permit management product that reduced excess spend by 20% and annual revenue by 5%, respectively.

## Getting Started
This project is a full-stack web app that leverages multiple technologies and frameworks.  
The instructions below act as a guide to getting a local instance of Plant Plotter up and running.

## Prerequisites
Project was written in Python3 on the backend, Flask as the web framework, then Flask-SQLAlchemy as the ORM connecting to a PostgreSQL database.

If you are running MacOS or Windows, your installation steps will be slightly different. I used a Linux environment. 

Your environment may have different requirements.

## Amazon Web Services

<div class="section" id="id2">

Get an AWS account: [http://aws.amazon.com](http://aws.amazon.com).

</div>

This process takes a few minutes. You’ll need to provide Amazon with your contact information and a valid credit card number. The type of server used in this lecture is free for the first month and $5 afterwards. Unlike some other subscription-based services, though, you really can cancel easily anytime, and you’re only charged for the time you use.

Amazon will prompt you for the level of service contract you’d like for your account. Assuming you’d like to stay in the free tier, choose “Basic”.

<div class="section" id="steps-to-create-an-aws-account">

### Steps to create an AWS account
**1.** On the [Amazon Web Services homepage](https://aws.amazon.com/), click **Sign In to the Console** in the top right-hand corner of the screen.

**2.** Enter your email address and select **I am a new user**

**3.** Enter your login credentials on the next page and click **Create account**.

**4.** Enter your contact information.

**5.** Enter payment information. AWS accounts themselves are free, but higher levels of support and various AWS services are paid. You are required to enter a valid credit card number to create an account, but you may select to remain on the basic, free tier later in this process.

**6.** AWS will confirm your identity through a phone call. Enter your phone number and click **Call me now**.

You will receive a PIN on the screen. You should soon receive an automated call from AWS and you will be prompted to enter the PIN on your keypad during the call.

After you have successfully entered the PIN during the phone call, your screen should refresh and you will see **Identity verification complete**.

**7.** Choose your support plan. Assuming you’d like to stay in the free tier, choose “Basic”.

**8.** You will be redirected back to the AWS homepage, where you should see a **Complete Sign Up** button in the top right-hand corner of the screen. Click that button to finalize your account creation.


### Cloud-Based Servers

Flexible way to get servers — popular for ease-of-setup and for scalability.

Amazon has their classic offering, “EC2” (the _Elastic Compute Cloud_), which are highly flexible cloud-based servers that you can configure in many different ways, and pay for on a per-house basis. These are very popular with many startups and enterprises.

In this demonstration, we’ll be using a different product of their, “LightSail”. This is a way to get a cloud server of the same type as Amazon EC2, but on a flat-rate per month charge and with considerably fewer complex choices for setup.

In the end, the server you get works the same, regardless of how you acquire it. If you’d like to explore the process for getting a classic EC2 instance, feel free — but do expect it to take more effort to provision.

</div>

<div class="section" id="launch-an-instance">

### Launch an Instance

[http://lightsail.aws.amazon.com](http://lightsail.aws.amazon.com)

*   **Create Instance**
*   **OS Only** → **Ubuntu 16.04**
    *   Current “LTS” _(long-term support)_ version of Ubuntu
    *   Same as used in labs and Vagrant instances

</div>

<div class="section" id="launch-script">

### Launch Script

Copy and paste the following into the “Launch Script”

<div class="highlight-bash">

<div class="highlight">

<pre><span></span>hostnamectl set-hostname aws
sed <span class="s1">'1s/$/ aws/'</span> -i /etc/hosts
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python-virtualenv
apt-get install -y build-essential python-dev
apt-get install -y postgresql postgresql-client
sudo -u postgres createuser -s ubuntu
apt-get install -y postgresql-server-dev-9.5
apt-get install -y postgresql-plpython
apt-get install -y postgresql-contrib
apt-get install -y python3.6 python3.6-dev
apt-get install -y python3-pip
<span class="nb">echo</span> <span class="nb">export</span> <span class="nv">VIRTUALENV_PYTHON</span><span class="o">=</span>/usr/bin/python3.6 > /etc/profile.d/virtualenv_python.sh
</pre>

</div>

</div>

This provides the same core software as our labs & Vagrant.

You don’t need to understand this script to use your server. However, if you’d like to understand what we’re doing here:

*   We change the nickname this server will use for itself to **aws**. This will make it easier for you to tell which computer you’re logged onto, as that name will appear in the shell prompts
*   We add the “deadsnakes” Personal Package Archive (PPA). Think of this as expanding Ubuntu’s “app store”.
*   We use `apt-get update` to update the list of available software for Ubuntu Linux.
*   We install Python and PostgreSQL using `apt-get install` (the **-y** option means “assume yes for any prompts”)
*   We add a user to the PostgreSQL cluster called **ubuntu**, since that is the default user on your new server.
*   Updating the list of packages available now that we’ve added this new PPA.
*   Installing Python 3.6, then adding an environment variable to the base shell profile to make virtualenv create a Python 3.6 environment by default.

</div>

<div class="section" id="get-your-server">

### Get Your Server

<div class="docutils container">

*   Choose your plan
    *   For almost all projects, the $5/month plan will be fine
*   Name your instance
    *   This isn’t public; it just helps you different instances straight
*   Click **Create**

</div>

This launch script will take about 5 minutes to complete. You can start other things while it runs in the background, but it may be simplest to pause

Once your server is active, click on its name to see the management page for it.

</div>

</div>

<div class="section" id="secure-shell">

## Secure Shell

<div class="section" id="id3">

We’ll use **SSH** _(the secure shell)_ to get a shell on our server.

This is how we can set up our server, run software on it, etc.

</div>

<div class="section" id="connecting-via-browser">

### Connecting Via Browser

For convenience, Lightsail lets you connect via your browser

Click <cite>Connect using SSH</cite> and you get a shell on your server!

<pre class="console literal-block">ubuntu@aws:~ $ <span class="cmd">ls -a</span>   <span class="gray"># files on my server!</span>
</pre>

<div class="docutils container">

You’re at the shell on your new server!

Your username is <cite>ubuntu</cite>

</div>

Connecting via browser is handy, but browsers aren’t great UIs for this

Let’s do it properly — via our laptop Terminal

In this demonstration, we’ll be mildly assuming your laptop runs Linux or OSX natively. For Windows users, your computer may not have the <cite>ssh</cite> program installed (it depends on your setup and version of Windows).

For Windows users, you can either:

*   do the parts marked <cite>laptop</cite> inside of your Vagrant instance, or
*   download the program [Putty](http://www.putty.org/), a free SSH program for Windows

</div>

<div class="section" id="key-file">

### Key File

<div class="docutils container">

*   Amazon made you a “key pair” for your server
    *   You’ll use this, rather than a password, to log in
*   The server has the public key installed on it
*   You should download the private key — having this proves you’re you
*   <cite>Account</cite> → <cite>Download default key</cite>

</div>

<div class="admonition note">

Make sure to include the region’s name in your SSH key

Amazon includes the region in which you created your Lightsail instance in the SSH key’s name (in our example: **us-west-2**). Make sure to double check the name of your SSH key as you go through the following steps and adjust the commands accordingly.

</div>

Let’s take a look at it:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">cat ~/Downloads/LightsailDefaultPrivateKey-us-west-2.pem</span>
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAqdfAFP8tPRdb5Yl5f2dbgEeboUFp934DvRgP0
1Cm10ZvFgj4xuZ9B0l0VYfs5SPx/riowJ6R7Xt7Clxa+UsGYn8isK
<span class="gray">...</span>
</pre>

(of course, you key will be different than this output)

</div>

<div class="section" id="move-and-protect-your-key">

### Move and Protect Your Key

Let’s move and rename that so it’s easier to remember & type:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">mv ~/Downloads/LightsailDefaultPrivateKey-us-west-2.pem ~/.ssh/aws.pem</span>
</pre>

<div class="docutils container">

SSH requires keys to be readable only by you _(not other users of your laptop)_:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">chmod a=,g=,u=rw ~/.ssh/aws.pem</span>    <span class="gray"># make readable only by you</span>
</pre>

</div>

<div class="admonition note">

chmod

Given how important it is that your private key remain a secret, the <cite>ssh</cite> program requires that the private key is readable only by you, and is unreadable to other users on your computer. By convention, private keys are stored in the .ssh directory inside your home directory (ie: ~/.ssh ).

The UNIX program <cite>chmod</cite> lets you specify the permissions for a file. We’ve specified that everyone (**a**) has no privileges for it, but that that the user (**u**) who owns the file (you) can read and write it.

You can learn more about chmod with <cite>man chmod</cite> or at [http://www.computerhope.com/uniax/uchmod.htm](http://www.computerhope.com/uniax/uchmod.htm)

</div>

</div>

<div class="section" id="ssh-onto-server">

### SSH Onto Server

<pre class="big literal-block">ssh <span class="red">-i ~/.ssh/aws.pem</span> <span class="green">ubuntu</span>@<span class="blue">1.2.3.4</span>
</pre>

<div class="docutils container">

<dl class="docutils">

<dt><span class="red">use this key</span></dt>

<dd>Tell SSH which key to use to authenticate you</dd>

<dt><span class="green">username on server</span></dt>

<dd>Log in as user <cite>ubuntu</cite> on server _(Amazon created that account)_</dd>

<dt><span class="blue">IP address of your server</span></dt>

<dd>What machine do you want to log in on?</dd>

</dl>

</div>

<div class="docutils container">

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ssh -i ~/.ssh/aws.pem ubuntu@1.2.3.4</span>
The authenticity of host ... can't be established.
ECDSA key fingerprint is SHA256:s7vcRHFe9Z3NsgMYo...
Are you sure you want to continue connecting (yes/no)? <span class="cmd">yes</span>

<span class="gray">... lots of welcome text ...</span>

<span class="tan">server</span> $
</pre>

</div>

It will only ask for that safety confirmation the first time.

Notice your prompt when you’re shelled onto server:

<pre class="big literal-block"><span class="green">ubuntu</span>@<span class="blue">aws</span>:<span class="tan">~</span>$
</pre>

<div class="docutils container">

<dl class="docutils">

<dt><span class="green">username</span></dt>

<dd>You’re logged in as the <cite>ubuntu</cite> user</dd>

<dt><span class="blue">host name</span></dt>

<dd>You’re logged into your server</dd>

<dt><span class="tan">current directory</span></dt>

<dd>This is your current directory (`<span class="pre">~</span>` is home)</dd>

</dl>

</div>

<div class="docutils container">

The prompt reminds you which computer you’re shelled in on.

</div>

</div>

<div class="section" id="logging-out-and-in">

### Logging Out and In

To log out from the server shell, type <cite>Control-D</cite>

This takes you back to your laptop shell

<div class="docutils container">

To log back into your server shell, retype

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ssh -i ~/.ssh/aws.pem ubuntu@1.2.3.4</span>
<span class="tan">server</span> $ <span class="cmd">(Control-D)</span>
<span class="tan">laptop</span> $
</pre>

</div>

<div class="docutils container">

Repeat this until it feels comfortable!

</div>

</div>

<div class="section" id="look-around">

### Look Around

Your server is set up just like Vagrant/Hackbright Lab:

*   Python 3.6
*   PostgreSQL

<div class="docutils container">

Now let’s get our project set up!

</div>

</div>

</div>

<div class="section" id="our-project">

## Our project:

<div class="section" id="id4">

What do we need for our project to work?

*   Code (from our git repo on GitHub)
*   secrets.sh (for our API keys, our Flask session key, etc)
*   Database (from a .sql or seed.py file)

</div>

</div>

<div class="section" id="make-sure-launch-script-finished">

## Make sure launch script finished

<div class="section" id="id5">

The launch script can take a couple of minutes to finish, so let’s double check that it did:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">echo $VIRTUALENV_PYTHON</span>
/usr/bin/python3.6
</pre>

If necessary, log out (with ctrl-D), wait a couple of minutes, then log back in.

</div>

</div>

<div class="section" id="flask-app">

## Flask App

<div class="section" id="id6">

Use Git clone to get our Flask app onto our server:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">git clone https://github.com/hackbrightacademy/catapp.git</span>
</pre>

You could use any Flask application; this is just a simple sample Flask app.

</div>

<div class="section" id="id7">

Our demo Flask app:

*   Database:
    *   Needs PostgreSQL database, <cite>cats</cite>
    *   Script <cite>seed.py</cite> will add starting data
*   Routes:
    *   <cite>/</cite>: homepage
    *   <cite>/cats</cite>: lists cats in database
    *   <cite>/err</cite>: page that always throws error

</div>

<div class="section" id="installing-it">

### Installing It

Installing our Flask app is the same as it would be on our laptop:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">cd catapp</span>
<span class="tan">server</span> $ <span class="cmd">virtualenv</span> <span class="cmd">env</span>
<span class="tan">server</span> $ <span class="cmd">source env/bin/activate</span>

<span class="tan">server</span> (env) $ <span class="cmd">pip3</span> <span class="cmd">install -r requirements.txt</span>
</pre>

</div>

</div>

<div class="section" id="copying-files-to-from-server">

## Copying Files To/From Server

<div class="section" id="what-do-we-need">

### What do we need?

*   secrets.sh
*   .sql file with DB structure

</div>

<div class="section" id="id8">

### Copying Files To/From Server

You can use <cite>scp</cite> (“secure copy program”) to copy across networks.

It works by using SSH, so make sure SSH works first!

<pre class="big literal-block">scp -i ~/.ssh/aws.pem <span class="green">from</span> <span class="blue">to</span>
</pre>

<dl class="docutils">

<dt><span class="green">from</span></dt>

<dd>File path (for local file) or <cite>user@server:path</cite> for remote file</dd>

<dt><span class="blue">to</span></dt>

<dd>File path (for local file) or <cite>user@server:path</cite> for remote file</dd>

</dl>

</div>

<div class="section" id="copy-from-laptop-to-server">

### Copy From Laptop To Server

Copy file named <cite>secrets.sh</cite> from laptop to home directory on server:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">scp -i ~/.ssh/aws.pem ~/src/catapp/secrets.sh ubuntu@1.2.3.4:catapp/</span>
</pre>

<div class="docutils container">

You can check that it arrived on server:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ssh -i ~/.ssh/aws.pem ubuntu@1.2.3.4</span>
<span class="tan">server</span> $ <span class="cmd">ls catapp/</span>
  ...    secrets.sh    ...
</pre>

</div>

<div class="admonition note">

Copying From Server to Laptop

Sometimes, you want to copy files from your server down to your laptop. This could be log files that you want to inspet, files that someone uploaded that are causing bugs and that you want to be able to troubleshoot with locally, etc. The following example covers copying the <cite>secrets.sh</cite> on our server back to our laptop:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">scp -i ~/.ssh/aws.pem ubuntu@1.2.3.4:catapp/secrets.sh .</span>
</pre>

You can check that it arrived on your laptop:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ls</span>
...    secrets.sh    ...
</pre>

There are lots of useful options you can learn about here — particularly the option <cite>-r</cite>, which recursively copies a folder and all its contents.

</div>

<div class="admonition note">

Your remote path must include a ‘:’ .

Whether you’re copying a file from your laptop to your server, the remote path must include a : (even if you don’t specify any actual directory). This means that, in order to copy a file from your home directory to your remote server, you will need to use a command like:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">scp -i ~/.ssh/aws.pem my_file ubuntu@1.2.3.4:</span>
</pre>

If you don’t, you will end up with a file named **my_file ubuntu@1.2.3.4** in your current directory on your laptop instead.

</div>

</div>

</div>

<div class="section" id="copying-database-to-production">

## Copying Database to Production

<div class="section" id="id9">

Our strategy:

<div class="docutils container">

1.  Dump database on laptop with <cite>pg_dump</cite>
2.  Copy this SQL dump to server with <cite>scp</cite>
3.  Read in database dump on server

<div class="docutils container">

**NOTE:** This _may_ be different for your app!

</div>

</div>

</div>

<div class="section" id="dump-database">

### Dump Database

Dump your laptop database:

<pre class="console literal-block"><span class="tan">vagrant</span> $ <span class="cmd">pg_dump --clean --no-owner cats > ~/src/cats.sql</span>
</pre>

<dl class="docutils">

<dt><cite>–clean</cite></dt>

<dd>ensures that any existing tables in the database on server will be dropped when your import this.</dd>

<dt><cite>–no-owner</cite></dt>

<dd>useful since your development-database-owner name is likely to be “Vagrant” whereas on your server it’s “ubuntu”. Using the no-owner flag changes the database dump to not include the commands to try to set the owner to the exact same thing it was in the original database.</dd>

</dl>

</div>

<div class="section" id="copy-to-server">

### Copy to Server

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">scp -i ~/.ssh/aws.pem ~/src/cats.sql ubuntu@1.2.3.4:/tmp/</span>
</pre>

</div>

<div class="section" id="make-our-database">

### Make Our Database

Let’s make the database for our app:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">createdb cats</span>
</pre>

<div class="docutils container">

Can make sure we can get in:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">psql cats</span>
</pre>

</div>

<div class="docutils container">

(<cite>Control-D</cite> to exit back to shell)

</div>

Of course, there won’t be any tables in the database yet — you just created it!

</div>

<div class="section" id="read-in-database-on-server">

### Read in Database On Server

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ssh -i ~/.ssh/aws.pem ubuntu@1.2.3.4</span>

<span class="tan">server</span> $ <span class="cmd">psql cats < /tmp/cats.sql</span>
<span class="gray">... output of SQL being read in ...</span>
</pre>

</div>

<div class="section" id="seed-database">

### Seed Database

Let’s run our database seeding script:

<pre class="console literal-block"><span class="tan">server</span> (env) $ <span class="cmd">python3</span> <span class="cmd">seed.py</span>
</pre>

</div>

</div>

<div class="section" id="bringing-up-flask-app">

## Bringing up Flask App

<div class="section" id="id10">

Source your secrets.sh file

<pre class="console literal-block"><span class="tan">server</span> (env) $ <span class="cmd">source secrets.sh</span>
</pre>

Run Flask

<pre class="console literal-block"><span class="tan">server</span> (env) $ <span class="cmd">python3</span> <span class="cmd">server.py</span>
</pre>

<div class="docutils container">

This should start your Flask app on port 5000.

</div>

<div class="docutils container">

Can’t get to it from laptop, though — Amazon firewalls off port 5000

</div>

Amazon firewalls off every port except 22 (SSH) and 80 (HTTP)

<div class="docutils container">

*   We _could_ open port 5000 on our firewall
    *   But we don’t want people to have to ask for <cite>http://oursite:5000</cite>
*   We _could_ run Flask on port 80
    *   But it’s uncommon to run an app server directly on 80
    *   Also: if had a second app, <cite>dogapp</cite>, we couldn’t run both on 80!
*   So: we’ll keep on 5000, and solve that in a minute
    *   First, let’s make sure it’s actually running :)

</div>

Open a **new, second** terminal window and shell onto server:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ssh -i ~/.ssh/aws.pem ubuntu@1.2.3.4</span>

<span class="tan">server</span> $ <span class="cmd">curl http://localhost:5000</span>
<span class="gray">... HTML of homepage ...</span>
</pre>

</div>

</div>

<div class="section" id="edge-http-server-nginx">

## Edge HTTP Server: Nginx

<div class="section" id="edge-http-server">

### Edge HTTP Server

It’s common to have a generic HTTP server talking to the internet

<div class="docutils container">

*   This server listens on port 80
*   This server passes requests to (possibly several different) applications
*   This type of server is often called an “edge” server
    *   As it’s on the “edge” of your system and the Internet

</div>

This also allows for some intermediate security/performance solutions.

We’ll use general-purpose **Nginx** HTTP server to _proxy_ to Flask on 5000:



<div class="docutils container">

Can use this to serve multiple Flask apps:


</div>

And not just Flask apps — it will proxy to _anything_ — so this could be two Flask apps, a Django app, a Ruby on Rails app, and so on.

</div>

<div class="section" id="nginx">

### Nginx

If you’re not shelled onto your server, do so:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">ssh -i ~/.ssh/aws.pem ubuntu@1.2.3.4</span>
</pre>

<div class="docutils container">

Install Nginx:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo apt install -y nginx</span>
</pre>

</div>

<pre class="big literal-block"><span class="green">sudo</span> <span class="blue">apt</span> <span class="red">install</span> <span class="tan">nginx</span>
</pre>

<div class="docutils container">

<dl class="docutils">

<dt><span class="green">sudo</span></dt>

<dd>Do rest of this line as superuser</dd>

<dt><span class="blue">apt</span></dt>

<dd>Ubuntu Linux package management program</dd>

<dt><span class="red">install</span></dt>

<dd>Action for <cite>apt</cite> (can also <cite>search</cite>, etc)</dd>

<dt><span class="tan">nginx</span></dt>

<dd>Package(s) to install</dd>

</dl>

</div>

Here, we’re using a program called <cite>apt</cite>, which is a “package manager” for Ubuntu Linux: it installs new software onto our server. The **-y** flag tells it to install the packages without prompting the user for confirmation.

Normally, only the superuser can install software — so we’re running the program apt in a special way, by prepending it with <cite>sudo</cite>. This program, sudo, stands for “Superuser, do”. It provides a way to quickly perform a task that is normally limited to the superuser: just prepend the name <cite>sudo</cite> before any command.

Of course, if everyone could just do this, it would be a terrible security hole. Amazon set up our server so that the default user, <cite>ubuntu</cite>, has the right to use <cite>sudo</cite>. Most ordinary users wouldn’t be given that right.

We can now make sure Nginx is running on 80:

[http://1.2.3.4](http://1.2.3.4)

</div>

<div class="section" id="nginx-config">

### Nginx Config

We don’t want that default Nginx site — let’s delete configuration for it

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo rm /etc/nginx/sites-enabled/default</span>
</pre>

<div class="docutils container">

Our demo app already has a configuration file we’d like to use instead:

<div class="literal-block-wrapper docutils container" id="id12">

<div class="code-block-caption"><span class="caption-text">catapp/nginx.conf</span></div>

<div class="highlight-nginx">

<div class="highlight">

<pre><span></span><span class="k">server</span> <span class="p">{</span>
  <span class="kn">listen</span> <span class="mi">80</span> <span class="s">default_server</span><span class="p">;</span>
  <span class="kn">location</span> <span class="s">/</span> <span class="p">{</span> <span class="kn">proxy_pass</span> <span class="s">http://127.0.0.1:5000</span><span class="p">;</span> <span class="p">}</span>
<span class="p">}</span>
</pre>

</div>

</div>

</div>

</div>

<div class="docutils container">

This proxies requests on port 80 at `<span class="pre">/</span>` to <cite>http://127.0.0.1:5000</cite>.

</div>

You’ll need to create this file and copy it to your server using <cite>scp</cite>. You may want to add it to your git repository as well.

<div class="admonition note">

Optional Advanced: Nginx Config

The `<span class="pre">/</span>` is interesting — we could divide a web hostname into multiple apps. For example, we could have everything on our site under the name <cite>/blog</cite> go to Flask blogging app running on 5001, and everything else go to a Flask app running on port 5000:

<div class="last highlight-nginx">

<div class="highlight">

<pre><span></span><span class="k">server</span> <span class="p">{</span>
  <span class="kn">listen</span> <span class="mi">80</span> <span class="s">default_server</span><span class="p">;</span>
  <span class="kn">location</span> <span class="s">/blog</span> <span class="p">{</span> <span class="kn">proxy_pass</span> <span class="s">http://127.0.0.1:5001</span><span class="p">;</span> <span class="p">}</span>
  <span class="kn">location</span> <span class="s">/</span> <span class="p">{</span> <span class="kn">proxy_pass</span> <span class="s">http://127.0.0.1:5000</span><span class="p">;</span> <span class="p">}</span>
<span class="p">}</span>
</pre>

</div>

</div>

</div>

</div>

<div class="section" id="telling-nginx-about-our-config">

### Telling Nginx About Our Config

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">cd ~/catapp</span>
<span class="tan">server</span> $ <span class="cmd">sudo cp nginx.conf /etc/nginx/sites-enabled/catapp.conf</span>
</pre>

</div>

<div class="section" id="reloading-nginx-configuration">

### Reloading Nginx Configuration

Any time you edit the Nginx config, you need tell Nginx to reload it:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo systemctl reload nginx</span>
</pre>

If this returns an error message, go back to editing the configuration file, double-check that file for errors, re-save and try the command above to reload Nginx.

</div>

<div class="section" id="viewing-flask-via-port-80">

### Viewing Flask Via Port 80

If you’re not running Flask in any terminal window, do so:

<pre class="console literal-block"><span class="tan">server</span> (env) $ <span class="cmd">python3</span> <span class="cmd">server.py</span>
</pre>

Now we can visit [http://1.2.3.4](http://1.2.3.4) and see your site!

</div>

<div class="section" id="proxying">

### Proxying

<div class="big highlight-default">

<div class="highlight">

<pre><span></span><span class="n">http</span><span class="p">:</span><span class="o">//</span><span class="mf">1.2</span><span class="o">.</span><span class="mf">3.4</span>
</pre>

</div>

</div>

<div class="compare docutils container">

<div class="docutils container">

*   Notice there’s no <cite>:5000</cite>
*   We’re not talking directly to Flask
    *   We can’t — it’s firewalled off!
*   Nginx talks with Flask on 5000 and relays the response to us

</div>

<div class="docutils container">


</div>

</div>

</div>

</div>

<div class="section" id="production-style-flask">

## Production-Style Flask

<div class="section" id="id11">

<div class="docutils container">

*   We don’t want our Flask app in debug mode
    *   Debug mode is a big security hole!
    *   Change `app.run(debug=True)` to `app.run()`
    *   **Note:** removing debug mode stops Flask from automatically reloading when files change
*   We don’t want Flask to just print to the terminal

</div>

</div>

<div class="section" id="running-flask-as-a-service">

### Running Flask as a Service

Why run flask as a service?

<div class="docutils container">

*   You don’t have to stay connected for Flask to run
*   The system will restart Flask automatically if your server restarts
*   It’s “The Right Way”

</div>

<div class="docutils container">

**systemd** is the way Ubuntu (and most other modern Linux distributions) manage services. You’ll often hear “service” and “daemon” used interchangeably.

</div>

</div>

<div class="section" id="service-configuration-file">

### Service configuration file

This file tells systemd how and when to run your Flask app as a service.

<div class="highlight-ini">

<div class="highlight">

<pre><span></span><span class="k">[Unit]</span>
<span class="na">Description</span><span class="o">=</span><span class="s">My Awesome Cat App</span>
<span class="na">After</span><span class="o">=</span><span class="s">network.target</span>

<span class="k">[Service]</span>
<span class="na">User</span><span class="o">=</span><span class="s">ubuntu</span>
<span class="na">Group</span><span class="o">=</span><span class="s">ubuntu</span>
<span class="na">Environment</span><span class="o">=</span><span class="s">"LANG=en_US.UTF-8"</span>
<span class="na">Environment</span><span class="o">=</span><span class="s">"LANGUAGE=en_US.UTF-8:"</span>
<span class="na">WorkingDirectory</span><span class="o">=</span><span class="s">/home/ubuntu/catapp/</span>
<span class="na">ExecStart</span><span class="o">=</span><span class="s">/bin/bash -c "source secrets.sh\</span>
<span class="na">&& source env/bin/activate\</span>
<span class="na">&& python3 server.py &>> flask.log"</span>
<span class="na">Restart</span><span class="o">=</span><span class="s">always</span>

<span class="k">[Install]</span>
<span class="na">WantedBy</span><span class="o">=</span><span class="s">multi-user.target</span>
</pre>

</div>

</div>

Let’s get our service configuration file into place: <cite>/etc/systemd/system/flask.service</cite> .

First, create it and save it on your laptop as a file named <cite>flask.service</cite>. **Make sure to update it to match your app’s directories!**

<div class="docutils container">

Copy it to your server:

<pre class="console literal-block"><span class="tan">laptop</span> $ <span class="cmd">scp -i ~/.ssh/aws.pem flask.service ubuntu@1.2.3.4:/tmp/</span>
</pre>

</div>

<div class="docutils container">

**On the server**, move it into place:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo mv /tmp/flask.service /etc/systemd/system/</span>
</pre>

</div>

<div class="docutils container">

Tell systemd that it needs to keep track of your service:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo systemctl enable flask</span>
</pre>

</div>

<div class="admonition note">

Save a copy of _flask.service_ to your repository

You may end up wanting to deploy your app somewhere else that also uses **systemd** . It’s a good idea to copy the file into your git repo, **git add** it, **git commit** and then **git push**.

</div>

</div>

<div class="section" id="a-closer-look-at-our-systemd-config-file">

### A closer look at our systemd config file

Let’s take a slightly closer look at the service config file. You probably don’t need to worry about this right now, but you may find it useful to refer to it later on.

*   [Unit]
    *   Description: What your service is.
    *   After: Wait for the network parts of system startup to finish (or the app won’t be able to start).
*   [Service]
    *   User/Group: Which user and group this service should run as
    *   Environment: When services run with systemd, they don’t get all the default shell variables you get when you log in using <cite>ssh</cite>. Here, we are making sure that the app starts up using unicode/UTF-8 by default to prevent encoding/decoding errors.
    *   EnvironmentFile: We don’t use it in our example, but it can replace your <cite>source secrets.sh</cite> command. You just need to remove the ‘export ‘ from each line in secrets.sh .
    *   WorkingDirectory: This is the equivalent to using <cite>cd</cite> to go into the specified directory. If, for example, you are writing files to disk in your app using relative paths, WorkingDirectory will ensure that your fies get saved where you expect.
    *   ExecStart: What command to run:
        *   Load secrets
        *   Activate env
        *   Start App
        *   Redirect all logs (stdout and stderr) to the flask.log file
    *   Restart: Always restart the app, even if it crashes.
*   [Install]
    *   WantedBy: When installing this service, when should it run?

</div>

<div class="section" id="starting-flask">

### Starting Flask

Use <cite>systemctl start</cite> to start your app:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo systemctl start flask</span>
</pre>

Remember to stop flask if you haven’t already.

</div>

<div class="section" id="checking-if-flask-is-up">

### Checking if Flask is up

Use <cite>systemctl status</cite> to see if your app is running:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">sudo systemctl status flask</span>
● flask.service - My Flask App
   Loaded: loaded (/etc/systemd/system/flask.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2018-07-16 20:30:34 UTC; 6s ago
 Main PID: 17876 (bash)
    Tasks: 2
   Memory: 25.5M
      CPU: 276ms
   CGroup: /system.slice/flask.service
           ├─17876 /bin/bash -c source /home/ubuntu/catapp/secrets.sh && source /home/ubuntu/catapp/env/b
           └─17880 python3 /home/ubuntu/catapp/server.py

Jul 16 20:30:34 aws systemd[1]: Started My Flask App.
</pre>

Type ‘q’ to go back to your shell.

If you get the shell prompt here, your Flask app crashed in some way on startup – look in the log file (`cat log`) for information.

We can test that it’s still working: [http://1.2.3.4](http://1.2.3.4)

</div>

<div class="section" id="checking-flask-logs">

### Checking Flask Logs

Use <cite>cat</cite>, or <cite>less</cite> see your app’s log:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">cat ~/catapp/flask.log</span>
...
127.0.0.1 - - [20/Aug/2018 17:17:16] "GET /static/cats.css HTTP/1.0" 304 -
</pre>

Use <cite>tail -f</cite> to follow your app’s log:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">tail -f ~/catapp/flask.log</span>
...
127.0.0.1 - - [20/Aug/2018 17:21:59] "GET / HTTP/1.0" 200 -
</pre>

Use <cite>grep</cite> to search your app’s log for a pattern:

<pre class="console literal-block"><span class="tan">server</span> $ <span class="cmd">grep Exception flask.log</span>
[2018-08-20 17:21:50,160] ERROR in app: Exception on /err [GET]
</pre>

</div>

<div class="section" id="stopping-flask">

### Stopping Flask

Use systemctl stop to stop your app:
```
server $ sudo systemctl stop flask
```

Directions copyright from Hackbright Academy in San Francisco, CA
