<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="shortcut icon" href="http://www.aperturescience.com/favicon.ico" />
	<%include file="__header_data.mako"/>
  </head>
  <body>
    <%include file="__nav.mako"/>
    <div class="container">
      <div class="row">
        <h2>Servers</h2>
          <div class="span4">
            % for chan in inpss:
              ${chan}
            % endfor
          </div>
      </div>
      <hr>
      <footer>
        <%include file="__footer.mako"/>
      </footer>
    </div>
  </body>
</html>
