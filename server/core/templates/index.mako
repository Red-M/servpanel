<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="shortcut icon" href="http://www.aperturescience.com/favicon.ico" />
	<%include file="__header_data.mako"/>
  </head>
  <body>
    <%include file="__nav.mako"/>
    <div class="container">
      <div class="hero-unit">
        <h1>ServPanel</h1>
        <p><a href="http://bit.ly/QHNNMl" class="btn btn-primary btn-large">Hey. &raquo;</a></p>
      </div>
      <div class="row">
        <div class="span4">
          <h2>About</h2>
          <p>ServPanel is a python based server monitor.</p>
        </div>
        <div class="span4">
          <h2>Server Stats</h2>
          <p><a class="btn btn-danger" href="/status">View details &raquo;</a></p>
       </div>
        <div class="span4">
          <h2>Other</h2>
          <p>Version: ${version}</p>
        </div>
      </div>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
