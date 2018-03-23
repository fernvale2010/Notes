import web

indexpage = """
  <html lang='fr'><head><meta http-equiv='refresh' content='60' name='viewport' content='width=device-width, initial-scale=1'/>
  <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'><script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script><script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'></script>
  <title>ESP8266 Demo - www.projetsdiy.fr</title></head><body>
  <div class='container-fluid'>
  <div class='row'>
  <div class='col-md-12'>
  <h1>Demo Webserver ESP8266 + Bootstrap</h1>
  <h3>Mini station m&eacute;t&eacute;o</h3>
  <ul class='nav nav-pills'>
  <li class='active'>
  <a href='#'> <span class='badge pull-right'>
  t
  </span> Temp&eacute;rature</a>
  </li><li>
  <a href='#'> <span class='badge pull-right'>
  h
  </span> Humidit&eacute;</a>
  </li><li>
  <a href='#'> <span class='badge pull-right'>
  p
  </span> Pression atmosph&eacute;rique</a></li>
  </ul>
  <table class='table'>
  <thead><tr><th>Capteur</th><th>Mesure</th><th>Valeur</th><th>Valeur pr&eacute;c&eacute;dente</th></tr></thead>
  <tbody>
  <tr><td>DHT22</td><td>Temp&eacute;rature</td><td>
  t
  &deg;C</td><td>
  -</td></tr>
  <tr class='active'><td>DHT22</td><td>Humidit&eacute;</td><td>
  h
  %</td><td>
  -</td></tr>
  <tr><td>BMP180</td><td>Pression atmosph&eacute;rique</td><td>
  p
  mbar</td><td>
  -</td></tr>
  </tbody></table>
  <h3>GPIO</h3>
  <div class='row'>
  <div class='col-md-4'><h4 class ='text-left'>D5 
  <span class='badge'>
  etatGpio[0]
  </span></h4></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D5' value='1' class='btn btn-success btn-lg'>ON</button></form></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D5' value='0' class='btn btn-danger btn-lg'>OFF</button></form></div>
  <div class='col-md-4'><h4 class ='text-left'>D6 
  <span class='badge'>
  etatGpio[1]
  </span></h4></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D6' value='1' class='btn btn-success btn-lg'>ON</button></form></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D6' value='0' class='btn btn-danger btn-lg'>OFF</button></form></div>
  <div class='col-md-4'><h4 class ='text-left'>D7 
  <span class='badge'>
  etatGpio[2]
  </span></h4></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D7' value='1' class='btn btn-success btn-lg'>ON</button></form></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D7' value='0' class='btn btn-danger btn-lg'>OFF</button></form></div>
  <div class='col-md-4'><h4 class ='text-left'>D8 
  <span class='badge'>
  etatGpio[3]
  </span></h4></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D8' value='1' class='btn btn-success btn-lg'>ON</button></form></div>
  <div class='col-md-4'><form action='/' method='POST'><button type='button submit' name='D8' value='0' class='btn btn-danger btn-lg'>OFF</button></form></div>
  </div>
  <br><p><a href='http://www.projetsdiy.fr'>www.projetsdiy.fr</p>
  </div></div></div>
  </body></html>
"""

urls = (
    '/', 'index'
)


app = web.application(urls, globals())
render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index()


if __name__ == "__main__":
    app.run()




# https://stackoverflow.com/questions/37446843/web-py-error-loading-multiple-html-files-via-iframes
#--------------------------------------------------------------------------------------------------
# After digging through web.py documentation, all I needed to do was to provide file name with full path of 
# html files in order to make them accessible via urls.
# 
# I thought I would post here in case anyone else runs into similar issue.
# 
# """ url definition""" 
# urls = (
#   '/path/to/files/index.html', 'do_index_frame',
#   '/path/to/files/left.html', 'do_left_frame',
#   '/path/to/files/right.html', 'do_right_frame',
#   '/path/to/files/top.html', 'do_top_frame'
# )








